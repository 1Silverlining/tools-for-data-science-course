# -*- coding: utf-8 -*- 
import  xdrlib ,sys
import xlrd
import datetime
import json
import re
import os


def open_excel(file= 'file.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (str(e))

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数 
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

def getdate(date,stype=0):
    try:
        if stype == 1:
            d = xlrd.xldate.xldate_as_datetime(date,0)
            return d
        else:
            __s_date = datetime.date (1899, 12, 31).toordinal() - 1
            if isinstance(date , float ):
                date = int(date )
            d = datetime.date.fromordinal(__s_date + date )
            return d
    except:
        return date