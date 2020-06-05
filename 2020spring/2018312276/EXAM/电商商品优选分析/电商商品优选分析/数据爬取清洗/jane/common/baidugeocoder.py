# -*- coding: utf-8 -*-
'''
author:lianpengtao
date:2019-01-21
explain:百度地图api 根据经纬度,获得区域的基本信息
'''

import requests
import dbconf
import json

class BaiduInverseGeocoder:
    def __init__(self,ak_name = None):
        
        self.baidu_ak = dbconf.baidu_key
        if ak_name:
            self.baidu_ak = dbconf.baidukeys[ak_name]
        self.url = "http://api.map.baidu.com/geocoder/v2/?location=%s,%s&output=json&latest_admin=1&pois=0&"+"ak=%s"% self.baidu_ak
    def geocoder(self,lat,lng,url=None):
        """
            根据经纬度或者区域信息
        """
        if url:
            url = url + "&ak=%s"% self.baidu_ak
            #print ("b>>>>>>>>>>>",url)
        else:
            url = self.url %(lat,lng)
        result = None
        try:
            t = requests.get(url)
            result = json.loads(t.text)
            if result['status'] == 0:
                result = result
            else:
                result = None
        except:
            pass
        return result

    def getlocation_address(self,address):
        """
            根据地址获得经纬度和城市编码
        """
        location_data = {'province_code':0, #省份编码',
                        'province_name':'', #省份名称',
                        'city_code':0, #城市名',
                        'city_name':'', #城市名称',
                        'district_code':0, #区编码',
                        'district_name':'', #区名称',
                        "lat":'',
                        'lng':'',
                        'town':"",
                        'street':"",
                        'street_number':"",
        }
        url = dbconf.baidu_address %(address)
        cdata = self.geocoder(0,0,url)
        if cdata:
            if "result" in cdata:
                if "location" in cdata['result']:
                    location_data['lat'] = cdata['result']['location']['lat']
                    location_data['lng'] = cdata['result']['location']['lng']
                    # 根据经纬度获得 地址
                    url = dbconf.baidu_latlng %(location_data['lat'],location_data['lng'])
                    idata = self.geocoder(0,0,url)
                    if idata:
                        if "result" in idata:
                            if "addressComponent" in idata['result']:
                                location_data['province_code'] = idata['result']['addressComponent']['adcode'][0:2] +"0000"
                                location_data['province_name'] = idata['result']['addressComponent']['province']
                                #print (location_data['province_name'])
                                if ("北京" in location_data['province_name'] ) or ("上海" in location_data['province_name'])  or ("天津" in location_data['province_name']) or ("重庆" in location_data['province_name']):
                                    location_data['city_code'] = location_data['province_code']
                                    location_data['city_name'] = location_data['province_name']
                                else:
                                    location_data['city_code'] = idata['result']['addressComponent']['adcode'][0:4] +'00'
                                    location_data['city_name'] = idata['result']['addressComponent']['city']

                                location_data['district_code'] = idata['result']['addressComponent']['adcode']
                                location_data['district_name'] = idata['result']['addressComponent']['district']

                                if "town" in idata['result']['addressComponent']:
                                    location_data['town'] =  idata['result']['addressComponent']['town']
                                if "street" in idata['result']['addressComponent']:
                                    location_data['street'] =  idata['result']['addressComponent']['street']
                                if "street_number" in idata['result']['addressComponent']:
                                    location_data['street_number'] =  idata['result']['addressComponent']['street_number']


        return location_data

    def getlocation_latlng(self,lat,lng):
        """
            根据经纬度 获得城市地区信息
        """
        location_data = {'province_code':0, #省份编码',
                        'province_name':'', #省份名称',
                        'city_code':0, #城市名',
                        'city_name':'', #城市名称',
                        'district_code':0, #区编码',
                        'district_name':'', #区名称',
                        "lat":lat,
                        'lng':lng,
                        'town':"",
                        'street':"",
                        'street_number':"",
        }
        # 根据经纬度获得 地址
        url = dbconf.baidu_latlng %(lat,lng)
        idata = self.geocoder(0,0,url)
        if idata:
            if "result" in idata:
                if "addressComponent" in idata['result']:
                    if idata['result']['addressComponent']['adcode']!='0':
                        location_data['province_code'] = idata['result']['addressComponent']['adcode'][0:2] +"0000"
                        location_data['province_name'] = idata['result']['addressComponent']['province']
                        #print (location_data['province_name'])
                        if ("北京" in location_data['province_name'] ) or ("上海" in location_data['province_name'])  or ("天津" in location_data['province_name']) or ("重庆" in location_data['province_name']):
                            location_data['city_code'] = location_data['province_code']
                            location_data['city_name'] = location_data['province_name']
                        else:
                            location_data['city_code'] = idata['result']['addressComponent']['adcode'][0:4] +'00'
                            location_data['city_name'] = idata['result']['addressComponent']['city']

                        location_data['district_code'] = idata['result']['addressComponent']['adcode']
                        location_data['district_name'] = idata['result']['addressComponent']['district']

                        if "town" in idata['result']['addressComponent']:
                            location_data['town'] =  idata['result']['addressComponent']['town']
                        if "street" in idata['result']['addressComponent']:
                            location_data['street'] =  idata['result']['addressComponent']['street']
                        if "street_number" in idata['result']['addressComponent']:
                            location_data['street_number'] =  idata['result']['addressComponent']['street_number']


        return location_data

    def poi(self,query,lat,lng,page_num,radius):
        '''
            根据经纬度 获得 该经纬度附近poi的信息
            @query 检索关键字
            @lat 纬度值
            @lng 经度
            @page_num 页数
            @radius 范围
        '''
        url = "http://api.map.baidu.com/place/v2/search?query=%s&location=%s,%s&page_num=%s&page_size=20&radius=%s&output=json&ak=%s"
        result = {"total":0,'list':[]}
        url = url %(query,lat,lng,page_num,radius,self.baidu_ak)
        #print (url)
        t = requests.get(url)
        poidata = json.loads(t.text)
        if poidata:
            if poidata['message'] == '天配额超限，限制访问':
                print (poidata)
                time.sleep(10)
            if poidata['status'] == 0:
                result['total'] = poidata['total']
                result['list'] = poidata['results']
        return result

    def poi1(self,query,lat,lng,page_num,radius,ak):
        '''
            根据经纬度 获得 该经纬度附近poi的信息
            @query 检索关键字
            @lat 纬度值
            @lng 经度
            @page_num 页数
            @radius 范围
        '''
        url = "http://api.map.baidu.com/place/v2/search?query=%s&location=%s,%s&page_num=%s&page_size=20&radius=%s&output=json&ak=%s"
        result = {"total":-1,'list':[]}
        url = url %(query,lat,lng,page_num,radius,ak)
        #print (url)
        t = requests.get(url)
        poidata = json.loads(t.text)
        if poidata:
            if poidata['message'] == '天配额超限，限制访问':
                return result
            if poidata['status'] == 0:
                result['total'] = poidata['total']
                result['list'] = poidata['results']
        return result
#bdigeo = BaiduApiInverseGeocoder()
#address = bdigeo.baiduaddress('39.090729','117.37258')
