#-*- coding:utf-8 -*-
import json
import itertools
import re
import time
# mongo 模糊查询字符处理
def transfer_str(str):
    new_str = u""
    special = [u'/',u'^',u'$',u'*',u'+',u'?',u'.',u'(',u")",u"[",u"]"]
    for c in str:
        if c in special:
            new_str += u'\\'
        new_str += c
    return new_str

#判断两个用","分开的string 是否相同
def str_same(old,new):
    if type(old) == list:
        old = ",".join(old)
    if type(new) == list:
        new = ",".join(new)
    state = False
    old_data = old.split(",")
    new_data = new.split(",")
    for d in old_data:
        if d in new:
            state = True
    if not state:
        for d in new_data:
            if d in old:
                state = True
    return state

#判断两个list 是否有交集
def list_same(old,new):
    samea = list((set(old).union(set(new)))^(set(old)^set(new)))
    return samea

# 判断seq 中是否包含 aset中的内容
def containsAny(seq, aset):
    """
        seq  list
        aset 文本
    """
    specialist_lable = []
    for c in filter(aset.__contains__, seq):
        specialist_lable.append(c)
    return specialist_lable

# 取值限制
def state_distance(count,w_num):
    state = False
    if count <=1000 and w_num<=1000:
        state = True
    elif 1000<count <=2000 and w_num<=500:
        state = True
    elif 2000<count <=3000 and w_num<=650:
        state = True
    elif count > 3000 and w_num<= int(count*0.3):
        state = True
    return state

#正则提取
def abstract(re_list,texts):
    d = []
    for res in re_list:
        ret = re.findall(res,texts)
        if ret:
            if re.findall('[“,"]',ret[0]):
                if "“" in ret[0] and "”" not in ret[0]:
                    continue
            if len(ret[0])>3:
                d.append({"str":ret[0],"re":res})
    return d

# 对文章进行分段and 分句
def paragraph_sentence(texts):
    """
        texts 文章
        return {1:[],2:[],3:[]}  num 表示段落，句子为list
    """
    result = {}
    p_num = 0 # 段落
    contents =texts.split('\n')
    for content in contents:
        result[p_num] = content #front_sentence(content)
        p_num += 1
    return result

# 倒叙查询，得到此句前半句
def front_sentence(texts,num=0):
    sentences = []
    punt_list='.!?。！？。'.decode('utf8')
    start = 0
    i = 0 # 每个字符的位置
    punt_list = list(punt_list)
    l = []
    texts = list(texts)
    num = len(texts)-1
    while num:
        #print texts[num]
        if texts[num] not in punt_list:
            d =  texts[num]
            l.append(d)
        else:
            break
        num-=1
    return "".join(l[::-1])

# 插入mongo
def insert_mongo(data,table,db):
    state = 0
    data['create_time'] = int(time.time())
    if "url" in data and table not in  ['hbase_viewpoint_db','viewPoint_analyze','viewPoint_analyze_error',"soshoo_book_details_info_error","soshoo_book_details_info_2006"]:
        retData = db[table].find_one({'url':data['url']})
    else:
        retData = None
    #print 33333333333,table
    if retData:
        state = 2
    else:
        data['_id'] = getSoleID(table,db)
        db[table].insert(data)
        state = 1
    return state

# 查询
def select_mongo(table,url,db,title=None):
    #print "44444cccc",table#,db[table].find_one({"url":"http://weekly.caixin.com/2015-01-02/100770259.html"})
    if title:
        retData = db[table].find_one({'title':title})
    else:
        retData = db[table].find_one({'url':url})
    if retData:
        return retData
    else:
        return {}

        
def getSoleID(col_name, db):
    ID = db['index_rule'].find_and_modify(query={u'_id':col_name},update={"$inc":{u'currentIdVal':1}}, upsert=True)['currentIdVal']
    return int(ID)

def filter_tags(htmlstr):
    re_table=re.compile('<\s*table(?:(?!<\/table>)[\s\S])*<\s*\/\s*table\s*>',re.I) #匹配CDATA
    re_meta=re.compile('<\s*meta[^>]*\s*>',re.I)#meta
    re_style=re.compile('<\s*style(?:(?!<\/style>)[\s\S])*<\s*\/\s*style\s*>',re.I)#style

    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    tables = re_table.findall(htmlstr)
    for table in tables:
        
        if re.findall("<\s*img\s*src",table):
            pass
        else:
            htmlstr=htmlstr.replace(table,"")
    #s=re_table.sub('',htmlstr)#去掉CDATA
    htmlstr=re_meta.sub('',htmlstr) #去掉SCRIPT
    htmlstr=re_style.sub('',htmlstr)#去掉style
    htmlstr=re_comment.sub('',htmlstr)#去掉HTML注释
    return htmlstr

# 时间格式化
def date_formatting(date):
    data_format = "%Y-%m-%d"
    date = date.replace(u"年",'-').replace(u"月",'-').replace(u"日",'')
    ret = re.findall(u"(\d+)分钟前",date)
    if ret:
        minute = int(ret[0])
        day_int = int(time.time()) - minute*60
        return date_str(day_int,data_format)
    ret = re.findall(u"(\d+)小时前",date)
    if ret:
        hour = int(ret[0])
        day_int = int(time.time()) - hour*60*60
        return date_str(day_int,data_format)
    ret = re.findall(u"(\d+)天前",date)
    if ret:
        day = int(ret[0])
        day_int = int(time.time()) - day*24*60*60
        return date_str(day_int,data_format)
    ret = re.findall(u"\d{4}-\d{1,2}-\d{1,2}",date)
    if ret:
        day = ret[0]
        return date_str( time.mktime(time.strptime(day,data_format)),data_format )

    ret = re.findall(u"\d{4}-\d{1,2}-\d{1,2}",date)
    if ret:
        day = ret[0]
        #print 33333333333333333333333333,
        return date_str( time.mktime(time.strptime(day,data_format)),data_format )

    ret = re.findall(u"\d{1,2}-\d{1,2}",date)
    if ret:
        day = ret[0]
        year = str(time.strftime("%Y", time.localtime()))
        day = "%s-%s" %(year,day)
        return date_str( time.mktime(time.strptime(day,data_format)),data_format )
    
    ret = re.findall(u"\d{1,2}/\d{1,2}",date)
    if ret:
        day = ret[0]
        year = str(time.strftime("%Y", time.localtime()))
        day = "%s/%s" %(year,day)
        return date_str( time.mktime(time.strptime(day,data_format)),data_format )
        #day_int =

    return date
def date_str(date_int,format):
    data_format = "%Y%m%d"
    #转换成localtime
    time_local = time.localtime(int(date_int))
    #print "bbbbbbb",date_int,format,time_local
    #转换成新的时间格式(2016-05-05)
    dt = str(time.strftime(data_format,time_local))
    return dt