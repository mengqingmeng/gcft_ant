# -*- coding: UTF-8 -*-
'''
Created on 2016年8月17日

@author: MQM
'''
import urllib,json,time,codecs,threading
from ant import requestGCTS
#import requestData
ISOTIMEFORMAT='%Y-%m-%d %X'
print("begin",time.strftime( ISOTIMEFORMAT, time.localtime() ))
# t1 = threading.Thread(target=requestGCTS.getData, args=(3146,15000,"T1"))
# t2 = threading.Thread(target=requestGCTS.getData, args=(15000,29530,"T2"))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
#4929-29531
t1 = threading.Thread(target=requestGCTS.getData, args=(12764,29531,"main"))
t1.start()
t1.join()
print("end",time.strftime( ISOTIMEFORMAT, time.localtime() ))