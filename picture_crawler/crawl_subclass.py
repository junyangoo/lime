# -*-coding:utf-8 -*-
# !/usr/bin/python
import hbase_mar
import mysql_mar
import downloader
import abc


class crawler_subclass(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        print "world"
        self.download = downloader.Downloader()
        self.db_manager = mysql_mar.DbManager()
        self.hbase_manager = hbase_mar.HbaseClient()

    @abc.abstractmethod
    def crawl_page(self):
        pass

    @abc.abstractmethod
    def crawl_image(self):
        pass

