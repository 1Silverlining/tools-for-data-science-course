# -*- coding: utf-8 -*-
'''
author:lianpengtao
date:2019-01-21
explain:高德地图api 根据经纬度,获得区域的基本信息
'''

import requests
import dbconf
import json

class GaoDInverseGeocoder:
    def __init__(self,ak_name = None):        
        self.gaode_ak = dbconf.gaodekeys
        self.gaode_ak = dbconf.gaodekeys[ak_name]

    def poi(self,query,lat,lng,page_num,radius):
        '''
            根据经纬度 获得 该经纬度附近poi的信息
            @query 检索关键字
            @lat 纬度值
            @lng 经度
            @page_num 页数
            @radius 范围
        '''
        
        url = "https://restapi.amap.com/v3/place/around?keywords=%s&location=%s,%s&radius=%s&key=%s&page=%s&extensions=all&offset=25"
        # print (url %(query,lng,lat,radius,self.gaode_ak,page_num))
        result = {"total":0,'list':[]}
        url = url %(query,lng,lat,radius,self.gaode_ak,page_num)
        t = requests.get(url)
        poidata = json.loads(t.text)
        if poidata:
            if poidata:
                if poidata['status'] == '1':
                    result['total'] = int(poidata['count'])
                    result['list'] = poidata['pois']
                else:
                    result = {"total":-1,'list':[]}
        return result
#bdigeo = BaiduApiInverseGeocoder()
#address = bdigeo.baiduaddress('39.090729','117.37258')
