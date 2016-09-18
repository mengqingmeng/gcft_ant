from urllib import request
import logging,json,sys,time
logging.basicConfig(filename='C:\\Users\MQM\Desktop\example.log',level=logging.DEBUG)
#d = 'on=true&page=5021&pageSize=15&productName=&conditionType=1&applyname=&applysn='
d= ''
ISOTIMEFORMAT='%Y-%m-%d %X' 
print(time.strftime( ISOTIMEFORMAT, time.localtime() ),5)
if not d.strip():
    print("kong")
    sys.exit()
d = d.encode(encoding='utf_8', errors='strict')
#baseurl = "http://125.35.6.80:8080/ftba/itownet/fwAction.do?method=getBaNewInfoPage"
baseurl = "http://125.35.6.80:8080/ftba/itownet/fwAction.do?method=getBaInfo"
req = request.Request(baseurl,d)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
with request.urlopen(req) as f:
    print('Status:', f.status)
    returnData = f.read().decode('utf-8')
    print(returnData)
    logging.debug('Data:', json.loads(returnData))
    try:
        JsonObj = json.loads(returnData)
    except:
        logging.debug("数据为空，跳过")
    #with open('F:\JTPData\gcft_P_5021.json', 'w',errors='ignore') as f:
     #           f.write(json.dumps(JsonObj,ensure_ascii=False,indent=2))#需要加入ensure_ascii=False，不然输出\u535a\u5ba2\u56ed
                #count = count +1