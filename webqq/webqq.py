#!/usr/bin/python2.7
#coding=utf-8

# @author Dominic
# @email linheng_mail@126.com
# @home http://www.ccpt.cc

# Script for login webqq & keepalive & receive message, login can be completed by following steps:
# 1.Check
#   Check if can login without verifycode
# 2.GetImage of verfiycode
# 3.Login
#   Input password, and hash(password, verifycode1, verifycode2), request ptwebqq from server
# 4.Login2
#   It is a post process, tell server you get the ptwebqq & uin

# After Login, we should get the friends information, create three dict:
# 1.id2cat
#   qq -> friend categories
# 2.id2name
#   qq -> friend nickname or markname(if exist)
# 3.name2id
#   friend markname -> qq

# Then we keeping request poll2 to keepalive, and get new message from server, put it to queue
# There is a thread to deal with all the messsage

# More details can be found @home http://www.ccpt.cc

# -------------------------------------------------------------------------------------- #

import urllib2, re, random, cookielib, json, threading
from lib.tools import QQmd5, QQhash, request
from lib import settings, urls


# Derived from Thread, we will not set resource lock for using queue
# which support multithread by applying simple api
class webqq(threading.Thread):
    def __init__(self, user, pwd, msg_queue):
        threading.Thread.__init__(self)

        # Read cookies from cookie file
        self.cookies = cookielib.MozillaCookieJar()
        try:
            self.cookies.load(settings.loginCookie)
            self.cookies.load(settings.login2Cookie)
            self.cookies.load(settings.getFriendCookie)
        except Exception as e:
            print str(e)

        # Init opener
        self.opener = urllib2.build_opener(urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(self.opener)

        # QQ
        self.user = user

        # Password
        self.pwd = pwd

        # Random clientid, although it is random, it should be consistent
        self.clientid = str(random.randint(10000000, 99999999))

        # Receive message queue
        self.rece_msg_queue = msg_queue

        # QQ -> categories
        self.id2cat = dict()

        # Markname -> QQ
        self.name2id = dict()

        # QQ -> Markname/Nickname
        self.id2name = dict()


    # Check & GetImage(if need)
    def check(self):
        # Request
        url = urls.checkUrl % (self.user, str(random.random()))
        req = request(url)

        # Parse response
        verifycode = re.search(r"'(\d)','(.+)','(.+)'", req.read())
        retcode = verifycode.group(1)
        self.verifycode1 = verifycode.group(2)
        self.verifycode2 = verifycode.group(3)

        # if recode == 0, we can login without verifycode
        # otherwise, we should get image from server
        if retcode == "1":
            url = urls.getimageUrl % (self.user, str(random.randint(10, 99)))

            # Save to local
            with open(settings.verifyImg, "wb") as f:
                f.write(request(url).read())
            f.close()

            # Read & Input verifycode
            self.verifycode1 = raw_input("verifer:")

    # Login
    def login(self):
        # Calculate hash & request
        p = str(QQmd5(self.pwd, self.verifycode1, self.verifycode2))
        url = urls.loginUrl % (self.user, p, self.verifycode1, urls.loginProxy)
        request(url, referer = urls.loginReferer)

        # Set Cookies Value & Save
        try:
            for cookie in self.cookies:
                if cookie.name == 'ptwebqq':
                    self.ptwebqq = cookie.value
                elif cookie.name == 'uin':
                    self.uin_user = cookie.value
        except Exception as e:
            print e
            self.login()
        self.cookies.save(settings.loginCookie)

    # Login2
    def login2(self):
        try:
            # Request
            url = urls.login2Url
            data = urls.login2Data % (self.ptwebqq, self.clientid, self.clientid)
            req = request(url, data = data, referer = urls.login2Referer)
            self.result = json.load(req)
            
            # recode == 0, login successfully
            if self.result['retcode'] != 0:
                return False

            # Save cookies
            self.cookies.save(settings.login2Cookie)
        except Exception as e:
            print 'Login Failed...'

    # Get Friend information
    def getFriend(self):
        try:
            # post and parse response
            url = urls.getFriendUrl
            cnt = 1
            while self.uin_user[cnt] == '0':
                cnt += 1
            ptwebqq_hash = QQhash(self.uin_user[cnt:], self.ptwebqq)
            data = urls.getFriendData % (ptwebqq_hash, self.result['result']['vfwebqq'])
            req = request(url, data = data, referer = urls.getFriendReferer)
            sets = json.load(req)

            # qq -> categories
            for friend in sets['result']['friends']:
                self.id2cat[friend['uin']] = friend['categories']

            # qq -> nickname or markname
            for info in sets['result']['info']:
                self.id2name[info['uin']] = info['nick']

            # markname -> qq
            for marknames in sets['result']['marknames']:
                self.name2id[marknames['markname']] = marknames['uin']
                self.id2name[marknames['uin']] = marknames['markname']

            # write to friends information cookie
            self.cookies.save(settings.getFriendCookie)

            print 'Login Successfully'
        except Exception as e:
            print 'Get friend information failed'
        else:
            pass

    # Poll2, keepalive
    def poll2(self):
        try:
            # Request
            url = urls.poll2Url
            data = urls.poll2Data % (self.clientid, self.result['result']['psessionid'], \
                    self.clientid, self.result['result']['psessionid'])
            result = json.load(request(url, data = data, referer = urls.poll2Referer))

            # If useful message exists
            if int(result['retcode']) == 0:
                for res in result['result']:
                    try:
                        # content including font, color information
                        content = ''
                        for i in res['value']['content'][1:]:
                            content += str(i)

                        # we only care message, not including group message
                        if res['poll_type'] == 'message':
                            self.rece_msg_queue.put( (self.id2name[res['value']['from_uin']], content, res['value']['from_uin'], res['value']['time']))
                        else:
                            pass
                    except:
                        pass
            
            # Ptwebqq time out
            elif int(result['retcode']) == 116:
                self.ptwebqq = result['p']

            # Logout
            elif int(result['retcode']) == 121:
                print 'logout'
        except Exception as e:
            print e

    # Send message, support face!
    def sendMsg(self, uin, msg, face=None):
        try:
            uin = str(uin)
            url = urls.sendUrl
            if face is None:
                data = urls.sendData % (uin, urls.nofaceData % msg, self.clientid, \
                        self.result['result']['psessionid'], self.clientid, self.result['result']['psessionid'])
            else:
                data = urls.sendData % (uin, urls.faceData % (msg, str(face)), self.clientid, \
                        self.result['result']['psessionid'], self.clientid, self.result['result']['psessionid'])
            request(url, data = data, referer = urls.sendReferer).read()
        except Exception as e:
            print e

    # Overide run function
    def run(self):
        self.check()
        self.login()
        self.login2()
        self.getFriend()
        while True:
            self.poll2()

