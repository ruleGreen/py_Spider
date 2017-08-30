py_Spider
======
一个使用代理ip的简单爬虫，每一个线程使用一个代理ip进行爬取数据，并且在遇到封锁的情况下将当前
线程自动暂停一定的时间，随后从停止的位置开始接着爬，爬取的数据使用列表存储，并提供两种方式进
行本地存储。一是以txt格式进行输入，二是使用数据库操作类将爬取出来的数据进行存储在数据库中，
数据库选取Mysql,Oracle均可。
<br><br>
getIp.py
----
本文件自动爬取第三方网站上的代理ip并进行验证，将验证通过的代理ip存储在checkedProxyList当中

使用的第三方网站：


                                * http://www.proxy360.cn/Region/Brazil
                                * http://www.proxy360.cn/Region/China
                                * http://www.proxy360.cn/Region/America
               
<br>由于目标网站数目过多（防止数目太少爬取不到相应规模的代理ip），所以采用python的多线程处理，同时
开启20个线程进行爬取,再分别进行验证，最终得到可用的代理ip
<br><br>
main.py
----
本文件主要通过浏览器渲染页面时的加载json文件爬取相应的事项编码，对于不同的部门来说事项在一个page页
无法全部显示，所以需要爬取json数据里面的totalpage一栏得知所有的page数目，根据所得的page数目迭代
爬取所有的事项编码
<br><br>
getData.py
----

