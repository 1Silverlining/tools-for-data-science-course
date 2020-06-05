# !/usr/bin/env python
# -*- coding: utf-8 -*-,
# @File  : proxies.py
# @Desc  : 
# @Author:
# @Time  : 2019/10/25 16:42
# @Version: 1.0
# @License : Copyright(C)，Drcnet

import json
import random

import pymongo
import redis
import requests

# from port_data import settings


class ProxyMiddleware(object):
    def __init__(self):
        # self.ip_db = pymongo.MongoClient('mongodb://218.246.21.207:10002')
        pass

    def get_ip(self):
        url = 'http://218.246.21.207:10002/'
        res = requests.get(url).text
        res = [i for i in json.loads(res).values()]
        ip = random.choice(res)
        return ip

    def process_request(self, request, spider):
        ip = self.get_ip()
        print(ip)
        if 'https' in request.url:
            request.meta['proxy'] = 'https://{}'.format(ip)
        else:
            request.meta['proxy'] = 'http://{}'.format(ip)

# class ProxyMiddleware(object):
#     """
#         代理中间件
#     """
#     def __init__(self):
#         self.redisdb = redis.Redis(host='172.16.0.8', port=6380, db=0)
#
#     def get_ip(self):
#         proxies_name = 'proxies'
#         # print(self.redisdb.smembers(proxies_name))
#         if self.redisdb.smembers(proxies_name):
#             ip = str(self.redisdb.srandmember(proxies_name, 1)[0],encoding='utf8')
#             return ip
#
#     def process_request(self, request, spider):
#         if settings['PROXIES']:
#             proxies_name = settings['PROXIES']
#             # print(self.redisdb.smembers(proxies_name))
#             if self.redisdb.smembers(proxies_name):
#                 ips = str(self.redisdb.srandmember(proxies_name, 1)[0],encoding='utf8')
#                 # print(ips, 'ip---------')
#                 if 'https' in request.url:
#                     request.meta["proxy"] = "https://%s" % (ips)
#                 else:
#                     request.meta['proxy'] = 'http://%s' % (ips)
#
