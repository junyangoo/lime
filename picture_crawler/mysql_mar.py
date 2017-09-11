
# _*_ coding: UTF-8 _*_
# !/usr/bin/python

import time
import MySQLdb


class DbManager:
    def __init__(self):
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='qiushi', charset='utf8')

    def db_insert(self, *args):  # 数据库qiushi_table表操作
        url = args[0]
        image_title = args[1]
        name = args[2]
        content = args[3]
        good = args[4]
        comment = args[5]
        url_status = 'False'
        cur = self.conn.cursor()
        sql = "INSERT INTO qiushi_table (id, url,image_title, user_name, content, good, comment, url_status) " \
              "VALUES(NULL,'%s', '%s', '%s', '%s','%s', '%s', '%s')" % (url, image_title, name, content,
                                                                        good, comment, url_status)
        cur.execute(sql)
        self.conn.commit()
        cur.close()

    def db_select(self):  # 查询qiushi_table表中信息页面未爬去
        cur = self.conn.cursor()
        sql = "SELECT id,url,image_title FROM qiushi_table WHERE url_status = 'False'"
        cur.execute(sql)
        result = cur.fetchall()
        self.conn.commit()
        cur.close()
        return result

    def db_update(self, url):  # qiushi_table表中信息页面已爬取更新状态
        cur = self.conn.cursor()
        sql = 'UPDATE qiushi_table SET url_status= "True" WHERE url="%s"' % url
        cur.execute(sql)
        self.conn.commit()
        cur.close()

    def close(self):
        self.conn.close()








