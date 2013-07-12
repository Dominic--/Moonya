#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# User should define
qq = '38910267'
ps = '3893b5elh'

# GoodNight
# [user, timezone, zipcode, sleeptime, saygoodnight, tellweather]
friends = [[u'CPT', 8, 12712251, 23, True, True],[u'二儿子', 8, 2161838, 23, True, True], [u'小儿子', 8,  12712251, 23, True, True], [u'大儿子', 8, 2151849, 23, True, True]]
#friends = [['大', 8, 12712251, 23, True, True]]

# System define
loginCookie = 'cookie/loginGet.cookie'
login2Cookie = 'cookie/loginPost.cookie'
getFriendCookie = 'cookie/getFriend.cookie'
verifyImg = 'captcha/verifyImg.jpg'
