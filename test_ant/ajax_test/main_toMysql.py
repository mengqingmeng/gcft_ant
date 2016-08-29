# -*- coding: UTF-8 -*-
'''
Created on 2016年8月17日

@author: MQM
'''
import urllib,json,time,codecs,threading,mysql.connector
from ajax_test import toMysql
#import requestData

ISOTIMEFORMAT='%Y-%m-%d %X'
print("begin",time.strftime( ISOTIMEFORMAT, time.localtime() ))

t1 = threading.Thread(target=toMysql.toMysqlFunc, args=(1,3,"thread1"))
t2= threading.Thread(target=toMysql.toMysqlFunc, args=(3,5,"thread2"))
t1.start()
t2.start()
t1.join()
t2.join()
print("end",time.strftime( ISOTIMEFORMAT, time.localtime() ))
