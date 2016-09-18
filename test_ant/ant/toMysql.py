#coding=utf-8
'''
Created on 2016年8月24日

@author: MQM
'''
import mysql.connector,json,logging,time,os,threading
lock = threading.Lock()
conn = mysql.connector.connect(user='root', password='', database='ant_new')
cursor = conn.cursor()

log_dest = "F:\JTPData\log\\"
ISOTIMEFORMAT='%Y-%m-%d %X'    
logging.basicConfig(filename=log_dest+'toMysql.log',level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

for value in range(1,600000):
    isExists = os.path.exists('F:\JTPData\detail\\'+str(value)+'_gcft.json')
    if not isExists:
        print("不存在",value)
        continue
    with open('F:\JTPData\detail\\'+str(value)+'_gcft.json' , 'r',encoding='utf-8',errors='ignore') as f:
        jsonData = json.load(f)
        name = jsonData["productname"]
        apply_sn = jsonData["apply_sn"]
        provinceConfirm = jsonData["provinceConfirm"] #备案日期
        state = jsonData["state"]
        enterprise_name = jsonData["scqyUnitinfo"]["enterprise_name"]#生产企业
        enterprise_address = jsonData["scqyUnitinfo"]["enterprise_address"]#生产企业地址
        enterprise_healthpermits = jsonData["scqyUnitinfo"]["enterprise_healthpermits"]#生产企业卫生许可
        sj_enterprise_name = jsonData["sjscqyList"][0]["enterprise_name"]  #实际生产企业名称
        sj_enterprise_address = jsonData["sjscqyList"][0]["enterprise_address"]#实际生产企业地址
        sj_enterprise_enterprise_healthpermits = jsonData["sjscqyList"][0]["enterprise_healthpermits"]#实际生产企业卫生许可
        remark  = jsonData["remark"]    #说明
        cks = jsonData["ck"]     #备注 集合
        processid  = jsonData["processid"]
        
        ckStr = ""
        if len(cks) > 0:
            ckList = []
            for ck in cks:
                tempStr = str(ck["checkDate"]) +"对"+str(ck["unitName"]) +"进行备案后检查，检查结果："+str(ck["remark"])
                ckList.append(tempStr) 
            ckStr = str(ckList)
            
        cursor.execute('select id from new_gcft_product t where t.name = %s', (name,))
        values = cursor.fetchall()#查询结果
        if values:#如果产品存在,
            logging.debug("产品已存在,id:%d,fileId:%d" ,values[0][0],value)
            #print("产品已存在,id,fileId",(values[0][0],value))
            continue
        #产品
        cursor.execute('insert into new_gcft_product (id,name,apply_sn,provinceConfirm,state,enterprise_name,enterprise_address,enterprise_healthpermits,sj_enterprise_name,sj_enterprise_address,sj_enterprise_enterprise_healthpermits,remark,ck,processid)'
                       'values (%s,%s,%s, %s,%s, %s,%s, %s,%s,%s,%s, %s,%s,%s)',(0,name,apply_sn,provinceConfirm,state,enterprise_name,enterprise_address,enterprise_healthpermits,sj_enterprise_name,sj_enterprise_address,sj_enterprise_enterprise_healthpermits,remark,ckStr,processid))
        
        conn.commit()
        addedProductId = int(cursor.lastrowid)
        #成分
        for cf in jsonData["pfList"]: #遍历成分
            cfid = 0
            cursor.execute('select id from new_gcft_things t where t.name = %s', (cf["cname"],))
            values = cursor.fetchall()#查询结果
            if values:#如果成分存在,
                cfid = values[0][0]
            if len(values)==0:#如果不存在，在先将数据插入数据库 ，再将id添入ids[]
                cursor.execute('insert into new_gcft_things values (%s,%s)',( 0,cf["cname"]))
                conn.commit()
                cfid = int(cursor.lastrowid)
            try:
                cursor.execute('insert into new_gcft_product_thing (productId,thingId) values (%s, %s)',(str(addedProductId),cfid))
            except:
                logging.debug("产品-成分冲突，fail: %d" ,value)
            conn.commit()
    if value%1000==0:
        print(time.strftime( ISOTIMEFORMAT, time.localtime() ),value)
    logging.debug("success: %d" ,value)
conn.close()