# -*- coding: UTF-8 -*-
'''
Created on 2016年8月17日

@author: MQM
'''
import urllib,json,time,codecs,threading
#from ajax_test import requestDetail
import requestDetail

ISOTIMEFORMAT='%Y-%m-%d %X'    
print("begin",time.strftime( ISOTIMEFORMAT, time.localtime() ))
#requestDetail.getDetail(15,600000)
#t1 = threading.Thread(target=requestDetail.getDetail, args=(239982,240000,"thread1"))
#t2= threading.Thread(target=requestDetail.getDetail, args=(282969,300000,"thread2"))
#t3 = threading.Thread(target=requestDetail.getDetail, args=(358850,400000,"thread3"))
#t4 = threading.Thread(target=requestDetail.getDetail, args=(485137,500000,"thread4"))
t5= threading.Thread(target=requestDetail.getDetail, args=(596804,597804,"thread5"))
t6= threading.Thread(target=requestDetail.getDetail, args=(597804,598804,"thread6"))
t7= threading.Thread(target=requestDetail.getDetail, args=(598804,600000,"thread7"))


#t1.start()
#t2.start()
#t3.start()
#t4.start()
t5.start()
t6.start()
t7.start()
#t1.join()
#t2.join()
#t3.join()
#t4.join()
t5.join()
t6.join()
t7.join()

print("end",time.strftime( ISOTIMEFORMAT, time.localtime() ))
