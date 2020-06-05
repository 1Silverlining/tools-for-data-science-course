import time
import requests
from pymongo import MongoClient
from scrapy import Selector
from common.DBMYSQL import MyPymysqlPool
from common.dbconf import mysql_transportation


class Method(object):

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
        self.connection = MongoClient('127.0.0.1', 27017)
        self.db = self.connection['jane']

    def requests_build(self, url):
        """
        包装requests请求
        :param url:
        :return:
        """
        time.sleep(5)
        res = requests.get(url, headers=self.headers)
        # response = Selector(text=res.content.decode('utf-8', errors='ignore'))
        return res

    def data_storage_mysql(self, data, sheet_name):
        """
        mysql存储
        :param data:
        :return:
        """
        mysql = MyPymysqlPool("local", mysql_transportation)
        update_time = data.get('update_time')
        sql_tag = "SELECT * FROM {} WHERE update_time=%s and data_tag='{}'".format(sheet_name, data.get('data_tag'))
        tag = mysql.getAll(sql_tag, [update_time])
        if not tag:
            keys = list()
            values = list()
            for k, v in data.items():
                keys.append('`%s`' % k)
                values.append(v)
            sql = "insert into {}".format(sheet_name) + " ( %s ) values (%s) " % (",".join(keys), ','.join(['%s'] * len(keys)))
            mysql.insert(sql, values)
            mysql.dispose()

    def data_storage_mongodb(self, data):
        """
        mongodb存储
        :return:
        """
        self.db[data.get('cn')].update({'_id': data.get('_id')}, {'$set': data}, True)