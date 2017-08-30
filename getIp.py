# -*- coding: UTF-8 -*-

# 头部声明编码
import urllib2
import re
import chardet
import threading
import time
import requests


rawProxyList = []
checkedProxyList = []

# 八个目标网站
targets = ['http://www.proxy360.cn/Region/Brazil', 'http://www.proxy360.cn/Region/China',
           'http://www.proxy360.cn/Region/America', 'http://www.proxy360.cn/Region/Taiwan',
           'http://www.proxy360.cn/Region/Japan', 'http://www.proxy360.cn/Region/Thailand',
           'http://www.proxy360.cn/Region/Vietnam', 'http://www.proxy360.cn/Region/bahrein']

# 正则
retext = '''<span class="tbBottomLine" style="width:140px;">[\r\n\s]*(.+?)[\r\n\s]+</span>[\r\n\s]*'''  # ip
retext += '''<span class="tbBottomLine" style="width:50px;">[\r\n\s]*(.+?)[\r\n\s]*</span>[\r\n\s]*'''  # port
retext += '''<span class="tbBottomLine " style="width:70px;">[\r\n\s]*.+[\r\n\s]*</span>[\r\n\s]*'''     #type
retext += '''<span class="tbBottomLine " style="width:70px;">[\r\n\s]*(.+?)[\r\n\s]*</span>[\r\n\s]*''' #address
p = re.compile(retext, re.M)  #


# 获取代理的类
class ProxyGet(threading.Thread):
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target

    def getProxy(self):
        print("目标网站： " + self.target)
        req = urllib2.urlopen(self.target)
        result = req.read()
        # print chardet.detect(result)
        matchs = p.findall(result)
        # print(matchs)
        for row in matchs:
            ip = row[0]
            port = row[1]
            address = row[2].decode("utf-8").encode("gbk")
            proxy = [ip, port, address]
            # print proxy
            rawProxyList.append(proxy)

    def run(self):
        self.getProxy()


# 检验代理的类
class ProxyCheck(threading.Thread):
    def __init__(self, proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "https://www.baidu.com/"
        self.testStr = "030173"

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http": r'http://%s:%s' % (proxy[0], proxy[1])})
            # print r'http://%s:%s' %(proxy[0],proxy[1])
            opener = urllib2.build_opener(cookies, proxyHandler)
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1')]
            # urllib2.install_opener(opener)
            t1 = time.time()

            try:
                # req = urllib2.urlopen("http://www.baidu.com", timeout=self.timeout)
                req = opener.open(self.testUrl, timeout=self.timeout)
                # print "urlopen is ok...."
                result = req.read()
                # print "read html...."
                timeused = time.time() - t1
                # pos = result.find(self.testStr)
                # print "pos is %s" %pos
                # pos > -1
                if (result != None):
                    checkedProxyList.append((proxy[0], proxy[1], proxy[2], timeused))
                    # print "ok ip: %s %s %s %s" %(proxy[0],proxy[1],proxy[2],timeused)
                else:
                    continue

            except Exception, e:
                print e.message
                continue

    def sort(self):
        sorted(checkedProxyList, cmp=lambda x, y:cmp(x[3], y[3]))

    def run(self):
        self.checkProxy()
        self.sort()


def mian():
    getThreads = []
    checkThreads = []


    # 对每个目标网站开启一个线程负责抓取代理
    for i in range(len(targets)):
        t = ProxyGet(targets[i])
        getThreads.append(t)

    for i in range(len(getThreads)):
        getThreads[i].start()

    for i in range(len(getThreads)):
        getThreads[i].join()

    # 开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
    for i in range(20):
        t = ProxyCheck(rawProxyList[((len(rawProxyList) + 19) / 20) * i:((len(rawProxyList) + 19) / 20) * (i + 1)])
        checkThreads.append(t)

    for i in range(len(checkThreads)):
        checkThreads[i].start()

    for i in range(len(checkThreads)):
        checkThreads[i].join()

    print "校验代理总数目为:", len(checkedProxyList)
    # for proxy in checkedProxyList:
    #     print("checked proxy is: %s:%s\t%s\t%s\n" % (proxy[0], proxy[1], proxy[2], proxy[3]))




