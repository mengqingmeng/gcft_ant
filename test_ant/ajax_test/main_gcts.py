# -*- coding: UTF-8 -*-
'''
Created on 2016年8月17日

@author: MQM
'''
import urllib,json,time,codecs,threading
from ajax_test import requestGCTS
#import requestData

ISOTIMEFORMAT='%Y-%m-%d %X'
print("begin",time.strftime( ISOTIMEFORMAT, time.localtime() ))
#requestData.getData(2,4)
t1 = threading.Thread(target=requestGCTS.getData, args=(1,2,"T1"))
#t2 = threading.Thread(target=requestGCTS.getData, args=(5,10,"T2"))
t1.start()
#t2.start()
t1.join()
#t2.join()
print("end",time.strftime( ISOTIMEFORMAT, time.localtime() ))