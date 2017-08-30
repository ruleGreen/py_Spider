py_Spider
======
一个使用代理ip的简单爬虫，每一个线程使用一个代理ip进行爬取数据，并且在遇到封锁的情况下将当前
线程自动暂停一定的时间，随后从停止的位置开始接着爬，爬取的数据使用列表存储，并提供两种方式进
行本地存储。一是以txt格式进行输入，二是使用数据库操作类将爬取出来的数据进行存储在数据库中，
数据库选取Mysql,Oracle均可。


getIp.py
----
本文件自动爬取第三方网站上的代理ip并进行验证，将验证通过的代理ip存储在checkedProxyList当中

使用的第三方网站：


                                * http://www.proxy360.cn/Region/Brazil
                                * http://www.proxy360.cn/Region/China
                                * http://www.proxy360.cn/Region/America
                                * ......
由于目标网站数目过多（防止数目太少爬取不到相应规模的代理ip），所以采用python的多线程处理，同时
开启20个线程进行爬取
