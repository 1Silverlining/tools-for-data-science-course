# -*- coding: utf-8 -*-
'''
author:lianpengtao
date:2019-01-21
explain:百度地图api 根据经纬度,获得区域的基本信息
'''

import requests
import dbconf
import json
class BaiduApiInverseGeocoder:
    def __init__(self):
        self.url = "http://api.map.baidu.com/geocoder/v2/?location=%s,%s&output=json&latest_admin=1&pois=0&"+"ak=%s"% 'sg93Gv0LtQXMZosU7E7pTUGLZnG7xaPO'
        self.url_latlng = "http://api.map.baidu.com/place/v2/search?query=%s&region=%s&output=json&"+"ak=%s"% 'sg93Gv0LtQXMZosU7E7pTUGLZnG7xaPO'
    def baiduaddress(self,lat,lng):
        url = self.url %(lat,lng)
        print (url)
        address_data = None
        try:
            t = requests.get(url)
            address_data = json.loads(t.text)
            if address_data['status'] == 0:
                address_data = address_data['result']
            else:
                address_data = None
        except:
            pass
        return address_data

    def baiduaddress_latlng(self,name,city):
        url = self.url_latlng %(name,city)
        address_data = None
        lat = 0
        lng = 0
        try:
            t = requests.get(url)
            address_data = json.loads(t.text)
            
            for d in address_data['results']:
                if d['name'] == name:
                    lat = d['location']['lat']
                    lng = d['location']['lng']
        except:
           pass
        return {"lat":lat,"lng":lng}

#bdigeo = BaiduApiInverseGeocoder()
#address = bdigeo.baiduaddress('39.090729','117.37258')
