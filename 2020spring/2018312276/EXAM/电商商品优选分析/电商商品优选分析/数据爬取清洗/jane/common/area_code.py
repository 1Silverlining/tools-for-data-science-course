# -*- coding: utf-8 -*-
'''
author:lianpengtao
date:2019-01-21
explain:根据城市code ,获得省份编码和名称
'''

import common.dbconf
from common.dbconf import *
from common.DBMYSQL import *
class AreaCode:
    def __init__(self,mysql_bmap=None,table=None):
        self.table = table
        if not mysql_bmap:
            self.mysql_bmap = MyPymysqlPool("local_bmap", mysql_transportation)
        else:
            self.mysql_bmap = mysql_bmap
    
    def get_province(self,code,pid=0):
        """
            根据code 获得省份id和名称
        """
        if not pid:
            sql = "select area_code,area_name,parent_id from citys where area_code = %s"
            data = self.mysql_bmap.getOne(sql,code)
        else:
            sql = "select area_code,area_name,parent_id from citys where id = %s"
            data = self.mysql_bmap.getOne(sql,pid)
        if data:
            if data['parent_id'] == 0:
                d = {"province_code":data['area_code'],"province_name":str(data['area_name'],encoding='utf8')}
                return d
            else:
                return self.get_province(data['area_code'],data['parent_id'])
        else:
            return {"province_code":0,"province_name":""}

    def get_parent(self,code,result={"provinces_name":'',"provinces_code":0,"city_name":'',"city_code":0,"district_name":'','district_code':0}):
        # 根据code 获得他的名称和编码  和他父级的名称和编码
        if code:
            sql = "select * from  `%s`"% self.table+" where  `code`=%s"
            data = self.mysql_bmap.getOne(sql,(code,))
            if data:
                if data['level'] == 3:
                    result['district_name'] = data['name']
                    result['district_code'] = data['code']
                elif data['level'] == 2:
                    result['city_name'] = data['name']
                    result['city_code'] = data['code']
                if data['level'] == 1:
                    result['provinces_name'] = data['name']
                    result['provinces_code'] = data['code']

                if data['parent_id'] != 0:
                    return self.get_parent(data['parent_id'],result)
                else:
                    return result
        else:
            return None



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

#areacode = AreaCode()
#address = areacode.get_province('110000')
#print (address)
