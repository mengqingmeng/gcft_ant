# -*- coding: UTF-8 -*-
'''
Created on 2016年8月16日
@author: MQM
'''
from urllib import request,parse
import urllib,json,time,codecs,threading,logging
from urllib.error import URLError, HTTPError
logging.basicConfig(filename='/usr/gcft_ant/product_detail_debug.log',level=logging.DEBUG)
#pageCount = 40662
lock = threading.Lock()
lock.acquire()
def getData(fromPage,toPage):
    #count = 0
    for i in range(fromPage,toPage):
        d = 'on=true&page='+str(i)+'&pageSize=15&productName=&conditionType=1&applyname=&applysn='
        d = d.encode(encoding='utf8', errors='strict')
        baseurl = "http://125.35.6.80:8080/ftba/itownet/fwAction.do?method=getBaNewInfoPage"
        req = request.Request(baseurl,d)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        try:
            f = request.urlopen(req,timeout=300)
            #print('Status:', f.status, f.reason)
            if f.status == 200:
                returnData = f.read().decode('utf-8')
                #print('Data:', returnData)
                try:
                    JsonObj = json.loads(returnData)
                except:
                    logging.debug("数据为空，跳过",i)
                    continue
            #print(JsonObj["list"])
            with open('/usr/gcft_ant/step1_json.json', 'a',errors='ignore') as f:
                f.write(json.dumps(JsonObj,ensure_ascii=False,indent=2))#需要加入ensure_ascii=False，不然输出\u535a\u5ba2\u56ed
                if i<toPage-1 :
                    f.write(",")
                #count = count +1
        except URLError as e:
            logging.debug(e)
        logging.debug(i)
    return
lock.release()