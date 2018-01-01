import urllib.request
from bs4 import BeautifulSoup
import re
import time
import random



# -------------------------------------------------------公用方法----------------------------------------------------
class CommanCalss:
    def __init__(self):
        self.header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        self.testurl="www.baidu.com"

    def getresponse(self,url):
        req = urllib.request.Request(url, headers=self.header)
        resp = urllib.request.urlopen(req, timeout=5)
        content = resp.read()
        return content

    def _is_alive(self,proxy):
        try:
            resp=0
            for i in range(3):
                proxy_support = urllib.request.ProxyHandler({"http": proxy})
                opener = urllib.request.build_opener(proxy_support)
                urllib.request.install_opener(opener)
                req = urllib.request.Request(self.url, headers=self.header)
                # 访问
                resp = urllib.request.urlopen(req, timeout=5)
            if resp == 200:
                return True
        except:
            return False



 # -------------------------------------------------------代理池----------------------------------------------------
class ProxyPool:
    def __init__(self,proxy_finder):
        self.pool=[]
        self.proxy_finder=proxy_finder
        self.cominstan=CommanCalss()

    def get_proxies(self):
        self.pool=self.proxy_finder.find()
        for p in self.pool:
            if self.cominstan._is_alive(p):
                continue
            else:
                self.pool.remove(p)

    def get_one_proxy(self):
        return random.choice(self.pool)

    def writeToTxt(self,file_path):
        try:
            fp = open(file_path, "w+")
            for item in self.pool:
                fp.write('"'+'http://'+str(item)+'"' + '\n')
            fp.close()
        except IOError:
            print("fail to open file")


#-------------------------------------------------------获取代理方法----------------------------------------------------
#定义一个基类
class IProxyFinder:
    def __init__(self):
        self.pool = []

    def find(self):
        return

#西祠代理爬取
class XiciProxyFinder(IProxyFinder):
    def __init__(self, url):
        super(XiciProxyFinder,self).__init__()
        self.url=url
        self.cominstan = CommanCalss()

    def find(self):
        for i in range(1, 10):
            content = self.cominstan.getresponse(self.url + str(i))
            soup = BeautifulSoup(content,'lxml')
            ips = soup.findAll('tr')
            for x in range(2, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                if tds == []:
                    continue
                ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
                self.pool.append(ip_temp)
        time.sleep(1)
        return  self.pool

#-------------------------------------------------------测试----------------------------------------------------
if __name__ == '__main__':
    finder = XiciProxyFinder("http://www.xicidaili.com/wn/")
    ppool_instance = ProxyPool(finder)
    ppool_instance.get_proxies()
    ppool_instance.writeToTxt("proxy.txt")
