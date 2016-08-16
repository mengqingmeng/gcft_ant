from urllib import request
d = '{on:true,page:1,pageSize:15,productName:"",conditionType:1,applyname:"",applysn:""}'
d = d.encode(encoding='utf_8', errors='strict')
baseurl = "http://125.35.6.80:8080/ftba/itownet/fwAction.do?method=getBaNewInfoPage"
req = request.Request(baseurl,d)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))