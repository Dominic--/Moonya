#coding:utf-8

# @author Dominic
# @email linheng_mail@126.com
# @home http://www.ccpt.cc

# --------------------------------------------------------------------- #

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from plugin.simsimi import SimSimi

def deal(msg):
    if msg.startswith('@weather'):
        return msg.split('@weather ')[1]
    elif msg.startswith('@dict'):
        return msg.split('@dict ')[1]
    elif msg.startswith('@help'):
        return '目前可选特殊命令: @help, @weahter, @dict...'
    else:
        return SimSimi().chat(msg)
