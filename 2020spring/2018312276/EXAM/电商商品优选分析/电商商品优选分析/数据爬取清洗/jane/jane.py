# !/usr/bin/env python
# -*- coding: utf-8 -*-,
# @File  : jane.py
# @Desc  : 
# @Author: 
# @Time  :
# @Version: 1.0
# @License : Copyright(C)，Drcnet
import json
import re
from jane import md
from scrapy import Selector
from pymongo import MongoClient


class Jane(object):

    def get_info(self, url, category, type):
        """
        请求并解析数据
        :param url:
        :return:
        """
        res = md.requests_build(url)
        response = Selector(text=res.content.decode('utf-8', errors='ignore'))
        product_li_s = response.xpath('//div[@id="J_goodsList"]/ul/li')
        for product_li in product_li_s:
            item = dict()
            item['product_price'] = product_li.xpath('.//div[@class="p-price"]//text()').extract()
            item['product_price'] = ''.join(item['product_price']).strip() if item['product_price'] else ''
            item['product_id'] = product_li.xpath('./@data-sku').extract_first()
            item['product_img'] = product_li.xpath('.//div[@class="p-img"]//img//@src').extract_first()
            item['product_detail_url'] = product_li.xpath('.//div[@class="p-img"]//a//@href').extract_first()
            item['product_shop_name'] = product_li.xpath('.//a[@class="curr-shop hd-shopname"]//@title').extract_first()
            item['product_shop_url'] = product_li.xpath('.//a[@class="curr-shop hd-shopname"]//@href').extract_first()
            item['product_detail'] = product_li.xpath('.//div[@class="p-name p-name-type-2"]//text()').extract()
            item['product_detail'] = ''.join(item['product_detail']).strip() if item['product_detail'] else ''
            item['product_category'] = category
            item['type'] = type
            item['cn'] = 'jd'
            item['_id'] = item.get('product_id')
            print(item)
            md.data_storage_mongodb(item)

    def run(self):
        """
         程序入口
        :return:
        """
        goods_dict = {
            '美妆': ['口红', '粉底', '眉笔', '眼影', '遮暇'],
            '食品': ['辣条', '鸭脖', '薯片', '可乐', '瓜子'],
            '电子产品': ['手机', '耳机', '平板', '笔记本电脑', '音响'],
            '家电': ['冰箱', '空调', '洗衣机', '电视', '扫地机器人'],
            '包': ['行李箱', '双肩包', '挎包', '钱包', '电脑包']
        }
        for goods_cat, goods_list in goods_dict.items():
            for goods in goods_list:
                url = 'https://search.jd.com/Search?keyword={}'.format(goods)
                self.get_info(url, goods, goods_cat)


if __name__ == "__main__":
    vu = Jane()
    vu.run()
