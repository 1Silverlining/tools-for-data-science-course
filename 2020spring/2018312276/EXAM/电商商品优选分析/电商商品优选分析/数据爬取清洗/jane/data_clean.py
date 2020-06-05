# !/usr/bin/env python
# -*- coding: utf-8 -*-,
# @File  : data_clean.py
# @Desc  : 
# @Author: 
# @Time  : 2020/5/12 11:30
# @Version: 1.0
# @License : Copyright(C)，Drcnet
import pymongo

cur = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = cur['jane']
jds = db['jd'].find()
for jd in jds:
    jd['_id'] = int(jd.get('_id'))
    jd['product_price'] = jd.get('product_price').split("\n")[0]
    db['clean_data'].update({'_id': jd.get('_id')}, {'$set': jd}, True)