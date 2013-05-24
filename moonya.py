#!/usr/bin/python2.7
#coding=utf-8

# @author Dominic
# @email linheng_mail@126.com
# @home http://www.ccpt.cc

# Main script for Moonya, create four threads:
# 1. QQ-Thread: 
#    login webqq & poll2 for keepalive & check if new message exist, put it to rece_msg_queue
# 2. Rece-Thread: 
#    call ai module dealing with msg in rece_msg_queue, put response to send_msg_queue
# 3. Send-Thread: 
#    send msg in send_msg_queue
# 4. Generate-Thread: 
#    generate some special message and put it to send_msg_queue, such as goodnight

# More details can be found @home http://www.ccpt.cc

# ---------------------------------------------------------------------------------------------- #

import threading, Queue, sys, time

# We are chinese, we speak chinese ><
reload(sys)
sys.setdefaultencoding('utf-8')

from webqq.webqq import webqq
from lib import settings
from ai import ai

# Receive message queue & Send message queue
rece_msg_queue = Queue.Queue()
send_msg_queue = Queue.Queue()

# Receive thread
class rece_msg_thread(threading.Thread):
    def __init__(self, rece_queue, send_queue, qq):
        threading.Thread.__init__(self)
        self.rece_queue = rece_queue
        self.send_queue = send_queue
        self.qq = qq

    def run(self):
        while True:
            # Print Message for debug
            msg = self.rece_queue.get()
            t = time.strftime("%Y-%m-%d %X", time.localtime(float(msg[3])))
            print '%s %s:\n%s' % (msg[0], t, msg[1])
            self.rece_queue.task_done()

            # Log
            self.log = open('message/%s.dat' % msg[0], 'aw')
            self.log.write('%s %s:\n%s\n' % (msg[0], t, msg[1]))
            self.log.close()
            
            # Call ai to deal with the message
            self.send_queue.put((msg[2], ai.deal(msg[2])))

# Send thread
class send_msg_thread(threading.Thread):
    def __init__(self, send_queue, qq):
        threading.Thread.__init__(self)
        self.send_queue = send_queue
        self.qq = qq

    def run(self):
        while 1:
            # Send message
            msg = self.send_queue.get()
            self.qq.sendMsg(msg[0], msg[1])
            self.send_queue.task_done()

            # Log
            t = time.strftime("%Y-%m-%d %X", time.localtime(time.time()))
            self.log = open('message/%s.dat' % self.qq.id2name[int(msg[0])], 'aw')
            self.log.write('Moonya %s:\n%s\n' % (t, msg[1]))
            self.log.close()



# Generate special message
class generate_msg_thread(threading.Thread):
    def __init__(self, send_queue, qq):
        threading.Thread.__init__(self)
        self.send_queue = send_queue
        self.qq = qq

    def run(self):
        # Just a simple example, say goodnight to dear friends
        goodnight = True
        while 1:
            time.sleep(10)
            try:
                if goodnight and 'CPT' in self.qq.name2id:
                    self.send_queue.put((str(self.qq.name2id['CPT']), '晚安'))
                    goodnight = False
            except Exception as e:
                pass
            

# ---- Main ---- #
if __name__ == "__main__":

    # SetDaemon true for debug, i.e. the subprocess will quit when the father process quit
    
    qq = webqq(settings.qq, settings.ps, rece_msg_queue)
    qq.setDaemon(True)
    qq.start()

    rece = rece_msg_thread(rece_msg_queue, send_msg_queue, qq)
    rece.setDaemon(True)
    rece.start()

    send = send_msg_thread(send_msg_queue, qq)
    send.setDaemon(True)
    send.start()

    gene = generate_msg_thread(send_msg_queue, qq)
    gene.setDaemon(True)
    gene.start()
    
    # Processing will not quit
    while  1:
        time.sleep(10)
