#-*-coding:utf-8-*-

import sys, requests
reload(sys)
sys.setdefaultencoding('utf-8')

class SimSimi:

    def __init__(self):

        self.session = requests.Session()
        self.chat_url = 'http://www.simsimi.com/func/req?lc=zh&msg=%s'
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Referer': 'http://www.simsimi.com/talk.htm?lc=zh', 
            'Accept-Encoding':'gzip, deflate', 
            'X-Requested-With':'XMLHttpRequest', 
            'Content-Type':'application/json; charset=utf-8',
            'Accept-Language' : 'en-US,en;q=0.5', 
            'Connection':'keep-alive',
            'Accept':'application/json, text/javascript, */*; q=0.01'})
        self.session.cookies = requests.utils.add_dict_to_cookiejar(self.session.cookies, {
            '__utma':'119922954.674669942.1373296655.1373296655.1373296655.1',
            '__utmb':'119922954.7.9.1373296756870',
            '__utmc':'119922954',
            '__utmz':'119922954.1373296655.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'sagree':'true',
            'JSESSIONID':'6F3B6107AA73D7B947E8B82FE4788DE6'})
    
    def chat(self, message=''):
        r = self.session.get(self.chat_url % message)
        try:
            return r.json()['response'].encode('utf-8')
        except:
            return "不明所以..."

simsimi = SimSimi()

if __name__ == '__main__':
    print simsimi.chat('你好啊')
