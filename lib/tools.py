#coding=utf-8
import hashlib, urllib2

# calculate md5
def QQmd5(pwd, verifyCode1, verifyCode2):
    pwd_1 = hashlib.md5(pwd).digest()
    pwd_2 = hex_md5hash(pwd_1 + hexchar2bin(verifyCode2))
    pwd_final = hex_md5hash(pwd_2 + verifyCode1.upper())
    return pwd_final

def hex_md5hash(s):
    return hashlib.md5(s).hexdigest().upper()

def hexchar2bin(uin):
    uin_final = ""
    uin = uin.split('\\x')
    for i in uin[1:]:
        uin_final += chr(int(i, 16))
    return uin_final

# calculate hash for get_usr_friends2, copy from "atupal"
def QQhash(b, i):
    a = str(i) + "password error"
    s = ""
    while 1:
        if len(s) <= len(a):
            s += str(b)
            if len(s) == len(a):
                break
        else:
            s = s[0:len(a)]
            break
    j = [0 for i in xrange(len(s))]

    for d in xrange(len(s)):
        j[d] = ord(s[d]) ^ ord(a[d])

	aa = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
	ss = ""
    for d in xrange(len(j)):
        ss += aa[j[d] >> 4 & 15]
        ss += aa[j[d] & 15]
    return ss

# Package request
def request(url, methods = ['GET', 'POST'], data = None, referer = None, user_agent = None, origin = None, host = None):
    req = urllib2.Request(url)
    if data:
        req.add_data(data)
    if referer:
        req.add_header('Referer', referer)
    if user_agent:
        req.add_header('User-Agent', user_agent)
    if origin:
        req.add_header('Origin', origin)
    if host:
        req.add_header('Host', host)
    return urllib2.urlopen(req)
