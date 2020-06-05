#! _*_ coding:utf-8 _*_

import pymssql


class MSSQL:
    """
    使用该库时，需要在Sql Server Configuration Manager里面将TCP/IP协议开启
    """

    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.__GetConnect()
        cur.executemany(sql)
        resList = cur.fetchall()
        #查询完毕后必须关闭连接
        self.conn.close()
        return resList
    def __getInsertId(self, cur):
        """
        获取当前连接最后一次插入操作生成的id, 如果没有则为０
        """
        cur.execute("SELECT @@IDENTITY AS id")
        result = cur.fetchall()
        return result[0][0]

    def ExecNonQuery(self,sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        rid = self.__getInsertId(cur)
        self.conn.commit()
        self.conn.close()
        return rid

    def insertSingle(self, sql, value=[], conn=None):
        """
        @param sql:要插入的SQL格式
        @param value:要插入的记录数据tuple
        """
        cur = self.__GetConnect()
        cur.execute(sql,value)
        rid = self.__getInsertId(cur)
        self.conn.commit()
        self.conn.close()
        return rid
    '''
    def insertAffair(self,,sql):
        """
        使用事务插入
        @param sql : 要插入的sql 格式 {"sql":tuple}

        """
        cur = self.__GetConnect()
        cur.execute(sql,value)
        #rid = self.__getInsertId(cur)
        #if rid:
    '''



def main():
    #"""
    ms = MSSQL(host="localhost",user="sa",pwd="lian",db="DRCNet_XiZhang")
    #resList = ms.ExecQuery("SELECT  convert(varchar(max),Content) as Content FROM DF_DocContent")
    #print 6666666,resList
    '''
    insert_sql = """
            INSERT INTO [DF_DocContent]
                   ([DocId]
                   ,[Content]
                   ,[PageNo]
                   ,[Recordstatus]
                   ,[LastUpdateDate]
                   ,[IsDRCNet])
             VALUES(%s,%s,%s,%s,%s,%s) 
    """
    d = {"DocId":2,"Content":"xxx","PageNo":2,"Recordstatus":1,"LastUpdateDate":'2017-11-29',"IsDRCNet":1}
    b = ms.insertSingle(insert_sql,(1,'ccccc',1,1,'2017-11-28',1))
    print "2?>>>>",b
    #b = ms.insertSingle(insert_sql,d)
    #print b,"eeeeeeeeeee"
    #for (id,weibocontent) in resList:
    #    print str(weibocontent).decode("utf8")
    '''
    insert_sql = """

       INSERT INTO [DF_docMain] ( [ContentSource],[Author],[CreateDate],[Summary],[Source],[Recordstatus],[LastUpdateDate],[IsDRCNet],[UserId],[Keywords],[CensorCompany],[Subject] ) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )
    """
    v = ('xa', None, '2017-11-29 13:02:09', 0, 'bbb', 0, '2017-11-29 13:02:09', 1, 0, '', 'xa', 'aaa')

    
    b = ms.insertSingle(insert_sql,v)
    #print "ccccccccccc>>>>",b
    
if __name__ == '__main__':
    main()