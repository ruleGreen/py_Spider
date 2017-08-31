# coding=utf-8
import urllib2
import random
import time


class HtmlDownloader(object):
    def __init__(self):
        self.proxys = []

    def getProxy(self,proxylist):
        self.proxys  = proxylist
        # 选取随机的代理ip
        i = random.randint(0,len(self.proxys)-1)
        self.ip = self.proxys[i][0]
        self.port = self.proxys[i][1]


    def download(self, url):
        if url is None:
            return

        # 使用代理ip

        # proxy = urllib2.ProxyHandler({'https': '36.25.58.171:24164'})
        proxy = urllib2.ProxyHandler({'https': self.ip+':'+self.port})
        opener = urllib2.build_opener(proxy)
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')]
        # urllib2.install_opener(opener)
        try:
            response = opener.open(url)
        except urllib2.URLError:
            print("urlerror.please wait.....")
            time.sleep(20)
            try:
                response = opener.open(url)
            except urllib2.HTTPError:
                print("url.httperror,please wait......")
                return


        # headers = {'User-Agent': 'Mozilla/5.0 (Windows;U;Windows NT 6.1;en-US;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        # request = urllib2.Request(
        #     url=url,
        #     headers=headers
        # )

        # response = urllib2.urlopen(request)

        if response.getcode() != 200:
            return None

        return response.read()