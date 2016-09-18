##coding=utf-8
'''
Created on 2016年9月14日

@author: MQM
'''
import json,logging,threading,os,sys,time,io,mysql.connector,socket
from urllib import request,parse
from imp import reload
from bs4 import BeautifulSoup
from PIL import Image,ImageEnhance,ImageFilter
from pytesseract import image_to_string
lock = threading.Lock()
log_dest = "F:\JTPData\gcts\\"
result_dest ="F:\JTPData\gcts\html\\"

conn = mysql.connector.connect(user='root', password='Meng@1992', database='ant_new')
cursor = conn.cursor()
socket.setdefaulttimeout(60)
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
        print(id)
        param = parse.urlencode([("tableId","68"),("tableName","TABLE68"),("tableView","国产特殊用途化妆品"),("Id",str(id))])
        req = request.Request(baseurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        try:
            with request.urlopen(req,data = param.encode('utf-8')) as f:
                returnData = f.read().decode('utf-8')
                #print('Data:', returnData)

                #保存html
                pid = saveHtml(returnData,id,tName)
                
                #请求成分数据
                getDetail(id,pid,5,tName)
                
        except Exception as err:
            print(err)
            logging.debug("fail: %d %s" ,id,err)


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
    cursor.execute('select id from gcts_product where id = %s', (str(index),))
    values = cursor.fetchall()#查询结果
    if values:#如果产品存在,
        logging.debug("产品已存在,id:%d" ,index)
        #print("产品已存在:" ,index)
    else:
        cursor.execute('insert into gcts_product (id,name,clazz,enterprise_name,enterprise_address,approval_number,approval_state,approval_date,approval_years,healthpermits,nameremark,remark)'
                       'values (%s,%s,%s, %s,%s, %s,%s, %s,%s,%s,%s,%s)'
                       ,(index,str(name),str(clazz),str(enterprise_name),str(enterprise_address),str(approval_number),str(approval_state),str(approval_date),
                         str(approval_years),str(healthpermits),str(nameremark),str(remark)))
        conn.commit()
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
    req.add_header('Cookie', 'JSESSIONID=71A31F29CFDF050352799CD454245161')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')

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
def getDetail(id,pid,count,tName):
    code = "alert('验证码错误，请重新输入！');"
    while count > 0:
        #获取验证码
        veriCode = getVeriCode()
        url = detailurl + "?PID=" + str(pid) + "&randomInt=" + str(veriCode) + "&process=showNew"
        req = request.Request(url)
        req.add_header('Cookie', 'JSESSIONID=71A31F29CFDF050352799CD454245161')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
        with request.urlopen(req) as f:
            returnData = f.read()
            soup = BeautifulSoup(returnData,'html.parser')
            if code in str(soup):
                logging.debug("验证码错误")
                print("验证码错误")
                count = count - 1
                getDetail(id, pid, count,tName)
            else:
                count = -1
            with open(result_dest+str(id)+'D.html', 'w',errors='ignore') as f:
                f.write(returnData.decode('gbk'))
                logging.debug("detail_success: %d,%s" ,id,tName)
lock.release()