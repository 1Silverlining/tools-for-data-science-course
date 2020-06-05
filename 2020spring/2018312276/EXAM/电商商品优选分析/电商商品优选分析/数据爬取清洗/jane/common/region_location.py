# -*- coding: utf-8 -*-
'''
author:lianpengtao
date:2019-01-21
explain:根据城市code ,获得省份编码和名称
'''
import json
import dbconf
from dbconf import *
from DBMYSQL import *
import math
import numpy as np
from matplotlib.path import Path
class RegionLocation:
    def __init__(self,mysql=None,table=None):


        if not mysql:
            self.mysql = MyPymysqlPool("local_bmap",mysql_bmap_info)
        else:
            self.mysql = mysql

        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.pi = 3.1415926535897932384626  # π
        self.a = 6378245.0  # 长半轴
        self.ee = 0.00669342162296594323  # 扁率
            
    def location_province(self,code=0):
        """
            根据经纬度，判断是否省份内，获得所有省份的 location
        """
        sql = """
                    select a.`name`,a.`code`,b.region from cn_area as a 
                    INNER JOIN cn_area_region as b
                    on a.`code`=b.`code`
                    where a.parent_id=%s order by a.`code`

        """ %(code)
        print (sql)
        regions = {}
        for d in self.mysql.getAll(sql):
            code ="%s|%s"%(str(d['code']),str(d['name'],encoding='utf-8')) 
            if code not in regions:
                regions[code] = []
            regions[code].append(json.loads(str(d['region'],encoding='utf-8')))
        return regions

    
    def location_state(self,lat,lng,result = {}):
        """
            定位状态
        """
        result = {"province_code":0,"province_name":"","city_code":0,"city_name":"","district_code":0,"district_name":""}
        a1 = self.bd09togcj02(lng,lat)
        if a1:
            a2 = self.gcj02towgs84(a1[0],a1[1])
            if a2:
                lat = a2[1]
                lng = a2[0]
                # 获得在那个省份
                province_code = 0
                province_name = ""
                city_code = 0 
                city_name = ""
                district_code = 0
                district_name = ""
                #provinces_regions = self.location_province()
                # 判断省份
                province = self.location_contains(self.location_province(),lat,lng)
                if province:
                    province_code =province.split("|")[0]
                    province_name =province.split("|")[1]
                    #print ("vvv>>>>>>>>>>",province_code,province_name,type(province_code))
                    if province_code in ['110000','120000','310000','500000']:
                        city_code = province_code
                        city_name = province_name

                        province_code = province_code[0:3] +"100"
                        district = self.location_contains(self.location_province(province_code),lat,lng)
                        if district:
                            district_code = district.split("|")[0]
                            district_name = district.split("|")[1]
                        province_code = city_code
                    
                    else:

                        #如果判断出在那个省份，然后获得改省份所有的 市的范围,判断在那个市
                        city = self.location_contains(self.location_province(province_code),lat,lng)
                        if city:
                            city_code =  city.split("|")[0]
                            city_name =  city.split("|")[1]
                            # 如果判断出在那个市，根据获得的城市，判断在哪个区
                            district = self.location_contains(self.location_province(city_code),lat,lng)
                            if district:
                                district_code = district.split("|")[0]
                                district_name = district.split("|")[1]
        result = {"province_code":province_code,"province_name":province_name,"city_code":city_code,"city_name":city_name,
                    "district_code":district_code,"district_name":district_name}
        return result

        # 


    def location_contains(self,regions_result,lat,lng):
        result = None
        #state = False
        for k,v in regions_result.items():
            #print (k,len(v))
            
            for regions in v:
                lats = []
                lngs = [] 
                for region in regions['region'].split(","):
                    #for e in l.split(' '):
                    lats.append(region.split(' ')[1])
                    lngs.append(region.split(' ')[0])
                xc = np.array(lats)
                yc = np.array(lngs)
                xycrop=np.vstack((xc,yc)).T
                pth=Path(xycrop,closed=False)
                mask=pth.contains_points([[lat,lng]])
                #print (k,mask)
                if mask:
                    if mask[0]:
                        result = k
                        #state = True
                        return result
        return result



    def get_code(self,name):
        """
            根据 name 查询城市列表，获得城市6位编码 
        """
        sql = "select area_code from citys where area_name like '%"+name+"%'"
        data = self.mysql_bmap.getAll(sql)
        code = 0
        if data:
            if len(data)== 1:
                code = data[0]['area_code']
        return code
    def bd09togcj02(self,bd_lon, bd_lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)
        百度——>谷歌、高德
        :param bd_lat:百度坐标纬度
        :param bd_lon:百度坐标经度
        :return:转换后的坐标列表形式
        """
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.x_pi)
        gg_lng = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return [gg_lng, gg_lat]
    def gcj02towgs84(self,lng, lat):
        """
        GCJ02(火星坐标系)转GPS84
        :param lng:火星坐标系的经度
        :param lat:火星坐标系纬度
        :return:
        """
        if self.out_of_china(lng, lat):
            return lng, lat
        dlat = self.transformlat(lng - 105.0, lat - 35.0)
        dlng = self.transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) *self.pi )
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [lng * 2 - mglng, lat * 2 - mglat]

    def out_of_china(self,lng, lat):
        """
        判断是否在国内，不在国内不做偏移
        :param lng:
        :param lat:
        :return:
        """
        if lng < 72.004 or lng > 137.8347:
            return True
        if lat < 0.8293 or lat > 55.8271:
            return True
        return False
    def transformlat(self,lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat +   0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 *
                math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 *
                math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def transformlng(self,lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 *
                math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 *
                math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret


mysql = MyPymysqlPool("local",mysql_info)
rl = RegionLocation(mysql)


address = rl.location_state(29.787036,106.395816)
print (address)
mysql.dispose()
