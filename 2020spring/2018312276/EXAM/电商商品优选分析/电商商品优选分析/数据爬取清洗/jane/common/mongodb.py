#! _*_ coding:utf-8 _*_

import pymongo
from pymongo import MongoClient


class MongoDBUtils(object):
    """ 
    连接 MongoDB
    """
    def __init__(self, ip, port=27017, db_name="", user="", password=""):
        #print 'init mongodb.....'
        self.db_name = db_name
        self.connection = MongoClient(ip,port)
        db_auth = self.connection.admin
        db_auth.authenticate(user, password)
        self.db = self.connection[db_name]


    def getSoleID(self,col_name, db):
        ID = db['index_rule'].find_and_modify(query={u'_id':col_name},\
                update={"$inc":{u'currentIdVal':1}}, upsert=True)['currentIdVal']
        #print ">>>>>>>>>>>",ID
        return int(ID)