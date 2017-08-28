# -*-coding:utf-8 -*-
# !/usr/bin/python
import urlparse
import urllib2
import socket
import time
from datetime import datetime, timedelta

DEFAULT_DELAY = 1
DEFAULT_TIMEOUT = 60
DEFAULT_RETRIES = 5
DEFAULT_DOWNLOAD_ECHO = not True
DEFAULT_HEADER = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.qiushibaike.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/56.0.2924.87 Safari/537.36'
        }


class Downloader:
    """the class for downloader 
    """
    def __init__(self, delay=DEFAULT_DELAY, header=DEFAULT_HEADER, num_retries=DEFAULT_RETRIES
                 , timeout=DEFAULT_TIMEOUT, opener=None):

        self.throttle = Throttle(delay)  # 设置延时,避免爬的太快对服务器造成太大的影响而被封禁
        socket.setdefaulttimeout(timeout)  # 设置socket的超时时间，来控制下载内容时的等待时间。
        self.header = header              # 设置请求头
        self.num_retries = num_retries    # 设置 5XX 错误重新下载的尝试次数
        self.opener = opener              # urllib2.build_opener()　默认设为　None 就好，反正我不想像自己在创建一个
        self.code = None

    def __call__(self, url):
        self.throttle.wait(url)
        headers = self.header                                               # 请求头设置
        result = self.download(url, headers, num_retries=self.num_retries)  # 下载网页
        return result if result else None

    def download(self, url, headers, num_retries, data=None):
        if DEFAULT_DOWNLOAD_ECHO:
            print 'Downloading:', url
        request = urllib2.Request(url, data, headers or {})
        opener = self.opener or urllib2.build_opener()
        try:
            response = opener.open(request)
            html = response.read()
            # print html
            self.code = response.code
        except Exception as e:
            # print 'Download error:', str(e)
            html = ''
            if hasattr(e, 'code'):
                self.code = e.code
                if num_retries > 0 and 500 <= self.code < 600:
                    return self.download(url, headers, num_retries-1, data)  # _get() 错误返回值，默认为 None
            else:
                self.code = None
        return html

    def download2(self, url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'pic.qiushibaike.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/56.0.2924.87 Safari/537.36'
        }
        req = urllib2.Request(url, headers=headers)

        response = urllib2.urlopen(req, timeout=20).read()

        return response


# 实现了下载延时
class Throttle:
    def __init__(self, delay):
        """
        :param delay:  delay between downloads for each domain
        """
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        """Delay if have accessed this domain recently
        :param url: the url for domain
        """
        domain = urlparse.urlsplit(url).netloc
        # 主要是分析urlstring，返回一个包含5个字符串项目的元组：协议、位置、路径、查询、片段,这里返回 位置
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()

if __name__ == '__main__':
    url = 'http://pic.qiushibaike.com/system/pictures/11844/118445785/medium/app118445785.jpg'
    download = Downloader()
    html = download.download2(url)
    print html
    print download.code