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
from ajax_test.export_excel_test import enterprise_name

lock = threading.Lock()
log_dest = "F:\JTPData\gcts\\"
result_dest ="F:\JTPData\gcts\html\\"

#url
baseurl = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp"
vericodeurl = "http://123.127.80.6/servlet/GetImageServlet?sn=randomImage"
detailurl = "http://123.127.80.6/sfda/ShowJSYQAction.do"

ISOTIMEFORMAT='%Y-%m-%d %X'    
logging.basicConfig(filename=log_dest+'product_detail_debug.log',level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
lock.acquire()

def getData(fromIndex,toIndex,tName):
    for id in range(fromIndex,toIndex):
        param = parse.urlencode([("tableId","68"),("tableName","TABLE68"),("tableView","国产特殊用途化妆品"),("Id",str(id))])
        req = request.Request(baseurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        with request.urlopen(req,data = param.encode('utf-8')) as f:
            returnData = f.read().decode('utf-8')
            #print('Data:', returnData)
            
            #保存html
            pid = saveHtml(returnData,id,tName)
            
            #请求成分数据
            getDetail(id,pid,5)

lock.release()


def saveHtml(hData,index,tName):
    soup = BeautifulSoup(hData,'html.parser')
    detailHref = soup.find_all('a')[0].get("href")
    #for link in soup.find_all('a'):
    #   print(link.get("href"))
    with open(result_dest+str(index)+'.html', 'w',errors='ignore') as f:
        f.write(hData)
        logging.debug("success: %d %s" ,index,tName)
    
    #存储信息
    name = soup.find("td",text="产品名称").find_next("td").string
    clazz = soup.find("td",text="产品类别").find_next("td").string
    enterprise_name = soup.find("td",text="生产企业").find_next("td").string
    enterprise_address = soup.find("td",text="生产企业地址").find_next("td").string
    approval_number = soup.find("td",text="批准文号").find_next("td").string
    approval_state = soup.find("td",text="批件状态").find_next("td").string
    approval_date = soup.find("td",text="批准日期").find_next("td").string
    approval_years = soup.find("td",text="批件有效期").find_next("td").string
    healthpermits = soup.find("td",text="卫产许可证号").find_next("td").string
    nameremark = soup.find("td",text="产品名称备注").find_next("td").string
    remark = soup.find("td",text="备注").find_next("td").string
    print(name)
    #获取pid    
    pidIndex = str(detailHref).find('=')
    #print(detailHref[pidIndex+1:])
    return detailHref[pidIndex+1:]
    
    
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
    req = request.Request(vericodeurl)
    req.add_header('Cookie', 'JSESSIONID=8250B1C1D664C4F335297194289F0989')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')

    with request.urlopen(req) as f:
        returnData = f.read()
        #print(returnData)
        image = Image.open(io.BytesIO(returnData))
        #im = image.filter(ImageFilter.MedianFilter())
        #enhancer = ImageEnhance.Contrast(im)

        #im = im.convert('1')
        imgry = image.convert('L')
        out = imgry.point(table,'1')
        #out.show()
        text = image_to_string(out)
        return text

#请求详细信息
def getDetail(id,pid,count):
    code = "alert('验证码错误，请重新输入！');"
    while count > 0:
        #获取验证码
        veriCode = getVeriCode()
        url = detailurl + "?PID=" + str(pid) + "&randomInt=" + str(veriCode) + "&process=showNew"
        param = parse.urlencode([("PID",str(pid)),("randomInt",str(veriCode)),("process","showNew")])
        req = request.Request(url)
        req.add_header('Cookie', 'JSESSIONID=8250B1C1D664C4F335297194289F0989')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        with request.urlopen(req) as f:
            returnData = f.read()
            soup = BeautifulSoup(returnData,'html.parser')
            #print(soup)
            if code in str(soup):
                print("验证码错误")
                count = count - 1
                getDetail(id, pid, count)
