# -*- coding: UTF-8 -*-


#  http://www.gdbs.gov.cn/portal/public/home?sysMenuTab=govPublic
#  http://www.gdbs.gov.cn/portal/public/rest?listVo.adminOrgId=c37e2b7b-0042-46e8-9635-4fa563d24ad9&pageNumber=0&_=1503281345765
#  http://www.gdbs.gov.cn/portal/public/proceduresView?serviceSubjectId=10345000069645333012440000
#  http://www.gdbs.gov.cn/portal/serviceSubject/formView?serviceSubjectId=10239700069645333012440000


import html_downloader
import threading
import re
from bs4 import BeautifulSoup
import urlparse
import json

organId =  []
serviceId = []   # 事项id,  让事项成为唯一标识 最终存储在txt中
Pages = []


class HtmlParser(object):

    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()

    def parse(self,  html_doc):
        if html_doc is None:
            return

        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf8')
        self._get_new_urls(soup)

    def _get_new_urls(self,soup):

        # 要匹配的节点<a style="vertical-align: top;" href="/portal/public/procedures?orgId=6c168030-2989-45f0-a359-1786ec2d5b26"></a>
        pat = re.compile(r"/portal\/public\/procedures\?orgId=\d*")
        links = soup.find_all('a', href=pat)

        for link in links:
            new_url = link['href'] # 获得节点的href属性值, /view/2561555.htm
            # 获取organid
            organid = new_url[32:]
            organId.append(organid)

    def _get_new_serviceid(self):
        j = 0   # 获取Pages中的索引
        for id in organId:
            i=Pages[j]
            pages = []
            while(i>0):
                pages.append(i-1)
                i = i-1
            for p in pages:
                url = "http://www.gdbs.gov.cn/portal/public/rest?listVo.adminOrgId="+id + "&pageNumber="+bytes(p)
                html_doc = self.downloader.download(url)
                soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf8')
                pat = re.compile(r"/portal\/public\/proceduresView\?serviceSubjectId=\d*")
                links = soup.find_all('a', href=pat)

                for link in links:
                    new_url = link['href']  # 获得节点的href属性值, /view/2561555.htm
                    # 获取serviceid
                    serviceid = new_url[47:]
                    serviceId.append(serviceid)
            j = j + 1

class getOrganID:
    def __init__(self,url):
        self.url = url
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = HtmlParser()

    def getOrganId(self):
        html_doc = self.downloader.download(self.url)
        new_url = self.parser.parse(html_doc)

    def run(self):
        self.getOrganId()



class getServiceID:

    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = HtmlParser()
        return

    def getServiceId(self):
        for id in organId:
             self.url = "http://www.gdbs.gov.cn/portal/public/rest?listVo.adminOrgId="+id
             html_doc = self.downloader.download(self.url)
             # 解析从网络上获取的JSON数据
             jsonData = json.loads(html_doc)
             pages = jsonData["totalPages"]
             Pages.append(pages)
        self.parser._get_new_serviceid()

        return

    def run(self):
        self.getServiceId()



if __name__ == '__main__':
    url = "http://www.gdbs.gov.cn/portal/public/home?sysMenuTab=govPublic"
    oi = getOrganID(url)
    oi.run()
    si = getServiceID()
    si.run()


