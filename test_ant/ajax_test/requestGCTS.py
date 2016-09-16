##coding=utf-8
'''
Created on 2016年9月14日

@author: MQM
'''
import json,logging,threading,os,sys,time,io
from urllib import request,parse
from imp import reload
from bs4 import BeautifulSoup
from PIL import Image,ImageEnhance,ImageFilter
from pytesseract import image_to_string

lock = threading.Lock()
log_dest = "F:\JTPData\gcts\\"
result_dest ="F:\JTPData\gcts\html\\"

ISOTIMEFORMAT='%Y-%m-%d %X'    
logging.basicConfig(filename=log_dest+'product_detail_debug.log',level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
lock.acquire()
def getData(fromIndex,toIndex,tName):
    for id in range(fromIndex,toIndex):
        baseurl = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp"
        param = parse.urlencode([("tableId","68"),("tableName","TABLE68"),("tableView","国产特殊用途化妆品"),("Id",str(id))])
        req = request.Request(baseurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        with request.urlopen(req,data = param.encode('utf-8')) as f:
            returnData = f.read().decode('utf-8')
            #print('Data:', returnData)
            
            #保存html
            detailHref = saveHtml(returnData,id,tName)
            
            getVeriCode()
            
            #请求成分数据

lock.release()


def saveHtml(hData,index,tName):
    soup = BeautifulSoup(hData,'html.parser')
    detailHref = soup.find_all('a')[0].get("href")
    #for link in soup.find_all('a'):
    #   print(link.get("href"))
    with open(result_dest+str(index)+'.html', 'w',errors='ignore') as f:
        f.write(hData)
        logging.debug("success: %d %s" ,index,tName)
        
    return detailHref


# 二值化  
threshold = 140  
table = []  
for i in range(256):  
    if i < threshold:  
        table.append(0)  
    else:  
        table.append(1)  
  
#由于都是数字  
#对于识别成字母的 采用该表进行修正  
rep={'O':'0',  
    'I':'1','L':'1',  
    'Z':'2',  
    'S':'8'  
    }; 
    
#识别二维码
def getVeriCode():
    url = "http://123.127.80.6/servlet/GetImageServlet?sn=randomImage";
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')

    with request.urlopen(req) as f:
        returnData = f.read()
        #print(returnData)
        image = Image.open(io.BytesIO(returnData))
        #im = image.filter(ImageFilter.MedianFilter())
        #enhancer = ImageEnhance.Contrast(im)
        #im = enhancer.enhance(2)
        #im = im.convert('1')
        imgry = image.convert('L')
        out = imgry.point(table,'1')
        text = image_to_string(out)
        print(text)