# coding utf8
'''
Created on 2016年8月16日
@author: MQM
'''
from urllib import request,parse
import urllib
import json 

 
d = 'on=false&page=2&pageSize=15&productName=&conditionType=1&applyname=&applysn='
d = d.encode(encoding='utf_8', errors='strict')
baseurl = "http://125.35.6.80:8080/ftba/itownet/fwAction.do?method=getBaNewInfoPage"
req = request.Request(baseurl,d)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
f = request.urlopen(req)
print('Status:', f.status, f.reason)
if f.status == 200:
    returnDate = f.read().decode('utf-8')
    print('Data:', returnDate)
    JsonDate = json.loads(returnDate)
    print('JSON:', JsonDate)

