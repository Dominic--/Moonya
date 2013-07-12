#coding:utf-8
import urllib, sys
reload(sys)
sys.setdefaultencoding('utf-8')

from xml.dom import minidom

WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?w=%d&u=c'
WEATHER_MAP = {
        '21':'阴霾漫天',
        '22':'有烟雾',
        '23':'有大风',
        '24':'有风',
        '25':'很冷',
        '26':'有很多云',
        '27':'有很多云',
        '28':'有很多云',
        '29':'有很多云',
        '30':'有很多云',
        '31':'晴朗的很',
        '32':'晴朗的很',
        '33':'晴朗的很',
        '34':'晴朗的很',
        '35':'下雨还夹雪',
        '36':'很热'
        }

def weather_for_zip(zip_code):
    url = WEATHER_URL % zip_code
    dom = minidom.parse(urllib.urlopen(url))
    node = (dom.getElementsByTagName('yweather:forecast'))[0]
    
    return {
        'low': node.getAttribute('low'),
        'high': node.getAttribute('high'),
        'code': node.getAttribute('code')
    }

def tell_weather(code):
    w = weather_for_zip(code)
    weather = ''
    if w['code'] not in WEATHER_MAP:
        weather = '巴拉巴拉'
    else:
        weather = WEATHER_MAP[w['code']]
    return '今天好像目测会%s,最高气温有%s,最低到%s。好吧，我还不够智能><,鬼知道你该多穿衣服还是少出门...不过天气预报是准的~' \
            % (weather, w['high'], w['low'])

if __name__ == '__main__':
    print weather_for_zip(12712251)
    print tell_weather(12712251)
