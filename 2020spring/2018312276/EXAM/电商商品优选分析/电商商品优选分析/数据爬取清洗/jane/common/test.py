#!/usr/bin/env python
# -*- coding:utf-8 -*-
import xlrd
import sys
import json
import pymongo
from pymongo import MongoClient

# 连接数据库
client = MongoClient('localhost', 27017)
db = client['drcnet_xz_spider']
collection = db['port_quanqiu']

data = xlrd.open_workbook('C:/Users/liudehua/Desktop/对比结果/全球港口数据.xlsx')
table = data.sheets()[0]
# 读取excel第一行数据作为存入mongodb的字段名
rowstag = table.row_values(0)
nrows = table.nrows
# ncols=table.ncols
# print rows
returnData = {}
for i in range(1, nrows):
    item = dict()
    # 将字段名和excel数据存储为字典形式，并转换为json格式
    returnData[i] = json.dumps(dict(zip(rowstag, table.row_values(i))))
    # 通过编解码还原数据
    returnData[i] = json.loads(returnData[i])
    item['_id'] = i-1
    item['COUNTRY'] = returnData[i].get('COUNTRY')
    item['PORT_NAME'] = returnData[i].get('PORT_NAME')
    item['LAT'] = returnData[i].get('LATITUDE')
    item['LON'] = returnData[i].get('LONGITUDE')
    item['HARBORSIZE'] = returnData[i].get('HARBORSIZE')
    # print returnData[i]
    collection.insert(item)
