#-*- coding:utf-8 -*-
import json
import itertools
import re
import time
import datetime
import math
class UtilsInfo:
    def __init__(self):
        pass

    def filter_tags(self,htmlstr):
        #先过滤CDATA
        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
        re_br=re.compile('<br\s*?/?>')#处理换行
        re_h=re.compile('</?\w+[^>]*>')#HTML标签
        re_comment=re.compile('<!--[^>]*-->')#HTML注释
        s=re_cdata.sub('',htmlstr)#去掉CDATA
        s=re_script.sub('',s) #去掉SCRIPT
        s=re_style.sub('',s)#去掉style
        s=re_br.sub('\n',s)#将br转换为换行
        s=re_h.sub('',s) #去掉HTML 标签
        s=re_comment.sub('',s)#去掉HTML注释
        #去掉多余的空行
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s=self.replaceCharEntity(s)#替换实体
        return s
    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES={'nbsp':' ','160':' ',
            'lt':'<','60':'<',
            'gt':'>','62':'>',
            'amp':'&','38':'&',
            'quot':'"','34':'"',}

        re_charEntity=re.compile(r'&#?(?P<name>\w+);')
        sz=re_charEntity.search(htmlstr)
        while sz:
            entity=sz.group()#entity全称，如>
            key=sz.group('name')#去除&;后entity,如>为gt
            try:
                htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
                sz=re_charEntity.search(htmlstr)
            except KeyError:
                #以空串代替
                 htmlstr=re_charEntity.sub('',htmlstr,1)
                 sz=re_charEntity.search(htmlstr)
        return htmlstr

    def dateformat(self,d,oldtypes,newtypes):
        otherStyleTime = None
        try:
            timeArray = time.strptime(d,oldtypes)
            otherStyleTime = str(time.strftime(newtypes, timeArray))
        except:
            pass
        return otherStyleTime

    def deg2rad(self,deg):
        return deg*(math.pi/180)

    def twopoint_distance(self,lat1,lng1,lat2,lng2):
        """
            根据两个经纬度 计算距离
        """
        R=6371.393
        dlat=self.deg2rad(lat2-lat1)
        dlon=self.deg2rad(lng2-lng1)
        a=math.sin(dlat/2)**2+math.cos(self.deg2rad(lat1))*math.cos(self.deg2rad(lat2))*math.sin(dlon/2)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        return float(R*c)*1000

