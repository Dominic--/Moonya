#coding=utf-8
import urllib

# Check
checkUrl = 'https://ssl.ptlogin2.qq.com/check?uin=%s&appid=1003903&r=%s'

# Getimage
getimageUrl = 'https://ssl.captcha.qq.com/getimage?&uin=%s&aid=1002101&0.45644426648505%s'

# Login
loginProxy = str(urllib.quote('http://web2.qq.com/loginproxy.html?login2qq=1&webqq_type=10')).replace('/', '%2f')

loginUrl = 'https://ssl.ptlogin2.qq.com/login?u=%s&p=%s&verifycode=%s&webqq_type=10&remember_uin=1' \
        + '&login2qq=1&aid=1003903&u1=%s&h=1&ptredirect=0&ptlang=2052&from_ui=1&pttype=1&dumy=' \
        + '&fp=loginerroralert&action=2-14-32487&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10015' \
        + '&login_sig=0ihp3t5ghfoonssle-98x9hy4uaqmpvu*8*odgl5vyerelcb8fk-y3ts6c3*7e8-'

loginReferer = 'https://ui.ptlogin2.qq.com/cgi-bin/login?target=self&style=5&mibao_css=m_webqq&appid=1003903' \
        + '&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fweb.qq.com%2Floginproxy.html&f_url=loginerroralert&strong_login=1' \
        + '&login_state=10&t=20121029001'

# Login2
login2Url = 'http://d.web2.qq.com/channel/login2'

login2Referer = 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2'

login2Data = 'r=%%7B%%22status%%22%%3A%%22online%%22%%2C%%22ptwebqq%%22%%3A%%22%s%%22%%2C%%22passwd_sig%%22%%3A%%22%%22%%2C%%22clientid%%22%%3A%%22' \
        + '%s%%22%%2C%%22psessionid%%22%%3Anull%%7D&clientid=%s&psessionid=null'

# GetFriend
getFriendUrl = 'http://s.web2.qq.com/api/get_user_friends2'

getFriendData = 'r=%%7B%%22h%%22%%3A%%22hello%%22%%2C%%22hash%%22%%3A%%22%s%%22%%2C%%22vfwebqq%%22%%3A%%22%s%%22%%7D'

getFriendReferer = 'http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=1'

# Poll2
poll2Url = 'http://d.web2.qq.com/channel/poll2'

poll2Data = 'r=%%7B%%22clientid%%22%%3A%%22%s%%22%%2C%%22psessionid%%22%%3A%%22%s%%22%%2C%%22'\
        + 'key%%22%%3A0%%2C%%22ids%%22%%3A%%5B%%5D%%7D&clientid=%s&psessionid=%s' 

poll2Referer = 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=3'

# SendMessage
sendUrl = 'http://d.web2.qq.com/channel/send_buddy_msg2'

nofaceData = r'":"[\"%s\",[\"font\",{\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]","'

faceData = r'":"[\"%s\", [\"face\",%s],[\"font\",{\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]","'

sendData = 'r=%%7B%%22to%%22%%3A%s%%2C%%22face%%22%%3A237%%2C%%22content%smsg_id%%22%%3A13190001%%2C%%22clientid%%22%%3A%%22%s' \
        + '%%22%%2C%%22psessionid%%22%%3A%%22%s%%22%%7D&clientid=%s&psessionid=%s'

sendReferer = 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2'
