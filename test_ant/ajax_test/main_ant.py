# -*- coding: UTF-8 -*-
'''
Created on 2016年8月17日

@author: MQM
'''
import urllib,json,time,codecs,threading
from ajax_test import requestData
#import requestData

ISOTIMEFORMAT='%Y-%m-%d %X'
#with open('F:\JTPData\step1_json.json', 'a',errors='ignore') as f:
with open('/usr/gcft_ant/step1_json.json', 'a',errors='ignore') as f:
    f.write("[")
    
print("begin",time.strftime( ISOTIMEFORMAT, time.localtime() ))
#requestData.getData(2,4)
t1 = threading.Thread(target=requestData.getData, args=(1,20400))
t2 = threading.Thread(target=requestData.getData, args=(20400,40801))
t1.start()
t2.start()
t1.join()
t2.join()
print("end",time.strftime( ISOTIMEFORMAT, time.localtime() ))

with open('/usr/gcft_ant/step1_json.json', 'a',errors='ignore') as f:
    f.write("]")