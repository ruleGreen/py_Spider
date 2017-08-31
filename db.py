# -*- coding: UTF-8 -*-

import pyodbc



class DB:
    def __init__(self,data1,data2):
        self.pro = data1
        self.view = data2
        return

    def createTable(self):
        # conn_info = ('Driver={MySQL ODBC 5.1 Driver};Server=%s;Port=%s;Database=%s;User=%s; Password=%s;Option=3;' % (
        # host, port, database, user, pwd))
        # conn = pyodbc.connect(conn_info)
        conn = pyodbc.connect('DSN=gdxx;PWD=gdxx')
        cursor = conn.cursor()
        #cursor = conn.cursor()
        sql = "drop table szsx_procedure"
        cursor.execute(sql)
        # 42502 代表无权限 42s02代表错误 不可以duplicate插入
        sql = "create table if not exists szsx_procedure" \
              "(" \
              "sxbm   varchar(64) primary key not null," \
              "fbjg   text not null ," \
              "sxmc   text not null," \
              "sxxz   text not null," \
              "zgbm   text not null," \
              "sljg   text not null" \
              ") ;"
        # print(sql)
        cursor.execute(sql)
        sql = "drop table szsx_form_view"
        cursor.execute(sql)
        sql = "create table if not exists szsx_form_view" \
              "(" \
              "sxbm  varchar(64) primary key," \
              "bldx  text," \
              "bltj  text," \
              "sxcl  text," \
              "blsx  text," \
              "bsck  text," \
              "sfbz  text," \
              "blyj  text," \
              "wssbxc text," \
              "cnqx  text," \
              "bz    text" \
              ");"
        cursor.execute(sql)
        cursor.close()
        conn.close()

    def InsertIntoMysql(self):
        conn = pyodbc.connect('DSN=gdxx;PWD=gdxx')
        cursor = conn.cursor()
        sql = "DELETE FROM szsx_procedure"
        cursor.execute(sql)
        sql = "DELETE FROM szsx_form_view"
        cursor.execute(sql)
        for data in self.pro:
            # print(data[1])  # 中文
            # print(type(data[1]))  # <class 'bs4.element.NavigableString'>
            # print(data[1].encode('unicode-escape'))
            # data[5]会出现None的情况
            for i in range(len(data)):
                if(data[i]==None):
                    data[i]=u'无'
            sql = "insert into szsx_procedure(sxbm,fbjg,sxmc,sxxz,zgbm,sljg) values('"+data[0]+"','"+data[1]+"','"\
                  +data[2]+"','"+data[3]+"','"+data[4]+"','"+data[5]+"');"
            cursor.execute(sql)
            cursor.commit()
        for data in self.view:
            sql = "insert into szsx_form_view(sxbm,bldx,bltj,sxcl,blsx,bsck,sfbz,blyj,wssbxc,cnqx,bz) values('" + data[0] +"','" + data[1] + "','" \
                  + data[2] + "','" + data[3] + "','" + data[4] + "','" + data[5] + "','"+data[6]+"','"+\
                  data[7] + "','"+data[8]+"','"+data[9]+"','"+data[10]+"');"
            cursor.execute(sql)
            cursor.commit()   # 漏掉的话插入之后再次联接查询不到
        cursor.close()
        conn.close()


    def SelectData(self):
        conn = pyodbc.connect('DSN=gdxx;PWD=gdxx')
        cursor = conn.cursor()
        # sql = "insert into szsx_procedure(sxbm,fbjg,sxmc,sxxz,zgbm,sljg) values('10300100170769356812440000',\
        # '\u5e7f\u4e1c\u7701\u673a\u6784\u7f16\u5236\u59d4\u5458\u4f1a\u529e\u516c\u5ba4',\
        # '\u4e8b\u4e1a\u5355\u4f4d\u6cd5\u4eba\u53d8\u66f4\u767b\u8bb0','\u884c\u653f\u8bb8\u53ef\u4e8b\u9879',\
        # '\u5e7f\u4e1c\u7701\u673a\u6784\u7f16\u5236\u59d4\u5458\u4f1a\u529e\u516c\u5ba4',\
        # '\u5e7f\u4e1c\u7701\u4e8b\u4e1a\u5355\u4f4d\u6539\u9769\u670d\u52a1\u5c40');"
        # sql= "insert into szsx_procedure(sxbm,fbjg,sxmc,sxxz,zgbm,sljg) values(" \
        #      "'20328001400693975612440000', '\u5e7f\u4e1c\u7701\u53d1\u5c55\u548c\u6539\u9769\u59d4\u5458\u4f1a',\
        #       '\u7701\u6709\u7ebf\u7535\u89c6\u7f51\u57fa\u672c\u6536\u89c6\u7ef4\u62a4\  '广东省发展和改革委员会','广东省发展和改革委员会');"
        # cursor.execute(sql)
        sql = "select * from szsx_procedure"
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(len(rows))
        # for row in rows:
        #     print(row)
        cursor.close()
        conn.close()

#
# db = DB([],[])
# # db.createTable()
# db.SelectData()
# u =  '\u5e7f\u4e1c\u7701\u53d1\u5c55\u548c\u6539\u9769\u59d4\u5458\u4f1a'
# print(u.decode('unicode-escape')) #广东省发展和改革委员会
# u = u'\u5e7f\u4e1c\u7701\u53d1\u5c55\u548c\u6539\u9769\u59d4\u5458\u4f1a'
# print(u)   # 广东省发展和改革委员会
# print(u.encode('unicode-escape'))  #\u5e7f\u4e1c\u7701\u53d1\u5c55\u548c\u6539\u9769\u59d4\u5458\u4f1a


