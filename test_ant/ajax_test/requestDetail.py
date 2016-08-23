#coding=utf-8
'''
Created on 2016年8月17日

@author: MQM
'''
import json,logging,threading,os,sys,time
from urllib import request
from _ast import Str

lock = threading.Lock()
pidAddress ="F:\JTPData\processIds.txt"
#pidAddress ="/usr/gcft_ant/processids.txt"
log_dest = "F:\JTPData\log\\"
#log_dest = "/usr/gcft_ant/log/"
result_dest ="F:\JTPData\detail\\"
#result_dest ="/usr/gcft_ant/detail/"


ISOTIMEFORMAT='%Y-%m-%d %X'    
logging.basicConfig(filename=log_dest+'product_detail_debug.log',level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
lock.acquire()
def getDetail(fromProduct,toProduct,tName):
    with open(pidAddress, 'r',encoding='utf-8') as f:
        pIndex = fromProduct
        for id in f.readlines()[fromProduct:toProduct]:
            print("line number:",pIndex,tName)
            if not id.strip():
                continue
            d= 'processid=' + id
            d = d.encode(encoding='utf_8', errors='strict')
            baseurl = "http://125.35.6.80:8080/ftba/itownet/fwAction.do?method=getBaInfo"
            req = request.Request(baseurl,d)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
            with request.urlopen(req) as f:
                #print('Status:', f.status)
                returnData = f.read().decode('utf-8')
                #print(returnData)
                #logging.debug('Data:', json.loads(returnData))
                try:
                    JsonObj = json.loads(returnData)
                except:
                    logging.debug("数据为空，跳过:%d",id)
                with open(result_dest+str(pIndex)+'_gcft'+'.json', 'w',errors='ignore') as f:
                            f.write(json.dumps(JsonObj,ensure_ascii=False,indent=2))#需要加入ensure_ascii=False，不然输出\u535a\u5ba2\u56ed
                            logging.debug("success: %d %s" ,pIndex,tName)

            pIndex +=1
lock.release()