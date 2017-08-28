# -*-coding:utf-8 -*-
# !/usr/bin/python
import re
import urllib

import hbase_mar
import mysql_mar
import downloader


class crawler:
    def __init__(self):
        self.download = downloader.Downloader()
        self.db_manager = mysql_mar.DbManager()
        self.hbase_manager = hbase_mar.HbaseClient()

    def crawl_page(self):
        judge = True
        page_number = 1
        repeat = 0  # 数据库重复个数
        while judge:
            print page_number
            url = 'https://www.qiushibaike.com/imgrank/page/%s/' % page_number
            html = self.download(url)
            # 正则提取链接,等信息
            result_url = re.compile('<img src="(//.*?\.jpg)"\salt="(.*?)"').findall(html)
            result_name = re.compile('<img src=".*?" alt=.*?>.*?<h2>(.*?)</h2>', re.S).findall(html)
            result_content = re.compile('<div class="content">.*?<span>(.*?)</span>.*?</div>', re.S).findall(html)
            result_good = re.compile('<span class="stats-vote"><i class="number">(.*?)</i> 好笑</span>').findall(html)
            result_comment = re.compile('<i class="number">(.*?)</i> 评论').findall(html)
            # 判断下一页是否存在
            judge_page_exist = re.compile('<span class="next">.*?下一页.*?</span>', re.S).findall(html)
            for i in range(len(result_url)):
                image_url = 'http:'+str(result_url[i][0])
                image_title = result_url[i][1]
                print image_url
                try:
                    self.db_manager.db_insert(image_url, image_title, result_name[i], result_content[i]
                                              , result_good[i], result_comment[i])
                except Exception as e:
                    print e
                    repeat += 1
                # urllib.urlretrieve("http:"+str(result[i][0]), '/home/junyang/Desktop/image/%s.jpg' % result[i][1])
            if repeat >= 10:
                break
            if not judge_page_exist:
                break
            page_number += 1

    def crawl_image(self):
        while True:
            try:
                image_url_title = self.db_manager.db_select()
            except Exception as e:
                print 'crawl_image_hbase db_select error:', e
                break
            if not image_url_title:
                print 'mysql empty'
                break
            id = image_url_title[0][0]
            url = image_url_title[0][1]
            title = image_url_title[0][2]
            print url
            try:
                image_source = self.download.download2(url)
            except Exception as e:
                print 'download2 error'
                break
            try:
                self.hbase_manager.put(str(id), {'page:url': url, 'page:title': title,
                                                 'page:source': image_source})
            except Exception as e:
                print 'crawl_image_hbase hbase error', e
                break
            try:
                self.db_manager.db_update(url)
            except Exception as e:
                print 'crawl_image_hbase db_select error:', e

a = crawler()
a.crawl_page()
# a.crawl_image()