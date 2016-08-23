#coding=utf-8
'''
Created on 2016年8月18日

@author: MQM
'''
from openpyxl import Workbook
from openpyxl import load_workbook
import json

wb = Workbook() #新建文档
ws = wb.active
#workSheet = wb.create_sheet("sheet2")   #新建一页，名字“sheet2” 
#workSheet.title = "new sheet2"    #更改sheet 名字

#ws3 = wb["New Title"]    获取sheet，两种方式
#ws4 = wb.get_sheet_by_name("New Title")
ws['A1'] = "id"
ws['B1'] = "名称"
ws['C1'] = "备案编号"
ws['D1'] = "备案日期"
ws['E1'] = "备案状态"
ws['F1'] = "企业名称"
ws['G1'] = "企业地址"
ws['H1'] = "卫生许可"
ws['I1'] = "说明"
ws['J1'] = "processid"

for value in range(1,600000):
    with open('F:\JTPData\detail\\'+str(value)+'_gcft.json' , 'r',encoding='utf-8',errors='ignore') as f:
        jsonData = json.load(f)
        name = jsonData["productname"]
        apply_sn = jsonData["apply_sn"]
        provinceConfirm = jsonData["provinceConfirm"] #备案日期
        state = jsonData["state"]
        enterprise_name = jsonData["scqyUnitinfo"]["enterprise_name"]
        enterprise_address = jsonData["scqyUnitinfo"]["enterprise_address"]
        enterprise_healthpermits = jsonData["scqyUnitinfo"]["enterprise_healthpermits"]
        remark  = jsonData["scqyUnitinfo"]["remark"]
        processid  = jsonData["processid"]
        
        ws['A'+str(value-998)] = str(value-999)
        ws['B'+str(value-998)] = name
        ws['C'+str(value-998)] = apply_sn
        ws['D'+str(value-998)] = provinceConfirm
        ws['E'+str(value-998)] = state
        ws['F'+str(value-998)] = enterprise_name
        ws['G'+str(value-998)] = enterprise_address
        ws['H'+str(value-998)] = enterprise_healthpermits
        ws['I'+str(value-998)] = remark
        ws['J'+str(value-998)] = processid
wb.save("F:\JTPData\detail\\test.xlsx")