# !/usr/bin/env python
# -*- coding: utf-8 -*-,
# @File  : jane_data.py
# @Desc  : 
# @Author: 
# @Time  : 2020/5/11 13:21
# @Version: 1.0
# @License : Copyright(C)，Drcnet
import json
import re
from jane import md
from scrapy import Selector
from pymongo import MongoClient


class Jane(object):

    def __init__(self):
        self.connection = MongoClient('127.0.0.1', 27017)
        self.db = self.connection['jane']

    def get_info(self, products_list):
        """
        请求并解析数据
        :param url:
        :return:
        """
        base_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery7867308&_=1589159681401'
        products_args = [','.join(products_list[:len(products_list)//2]), ','.join(products_list[len(products_list)//2:])]
        len_num = len(products_list)//100
        # for products_arg in products_args:
        for i_num in range(len_num):
            products_arg = ','.join(products_list[i_num*100: (i_num+1)*100])
            url = base_url.format(products_arg)
            res = md.requests_build(url)
            datas = re.findall(r'({.*})', res.text)
            datas = json.loads(datas[0]) if datas else ''
            print(datas)
            CommentsCount = datas.get('CommentsCount')
            for CommentCount in CommentsCount:
                item = CommentCount
                item['_id'] = item.get('SkuId')
                item['cn'] = 'jd_data'
                print(item)
                md.data_storage_mongodb(item)
        products_arg = ','.join(products_list[len_num*100:])
        url = base_url.format(products_arg)
        res = md.requests_build(url)
        datas = re.findall(r'({.*})', res.text)
        datas = json.loads(datas[0]) if datas else ''
        print(datas)
        CommentsCount = datas.get('CommentsCount')
        for CommentCount in CommentsCount:
            item = CommentCount
            item['_id'] = item.get('SkuId')
            item['cn'] = 'jd_data'
            print(item)
            md.data_storage_mongodb(item)

    def run(self):
        """
         程序入口
        :return:
        """
        product_id_list = self.db['jd'].distinct('_id')
        self.get_info(product_id_list)


if __name__ == "__main__":
    vu = Jane()
    vu.run()
