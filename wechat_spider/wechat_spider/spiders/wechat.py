# -*- coding: utf-8 -*-
import scrapy
from wechat_spider.items import WechatSpiderItem
import json
import re
from bs4 import BeautifulSoup
import time

class WechatSpider(scrapy.Spider):
	name = 'wechat'
	# allowed_domains = ['weixin.sogou.com/']
	headers = {'Host': 'weixin.sogou.com',
			      'Referer': 'http://weixin.sogou.com/weixin?type=2&s_from=input&query=%E6%B5%85%E5%B1%B1%E5%B0%8F%E7%AD%91&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=5109&sst0=1513697178371&lkt=0%2C0%2C0',
			      'Upgrade-Insecure-Requests': '1',
			      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

	print('''
            **************************  
            Welcome to 公众号爬虫平台          
               Created on 2017-12-21           
                 @author: 小明酱lmx                  
            **************************
	''' )
	print("1.按公众号名称搜索;2.按关键字进行搜索")
	choice = input("请输入查询模式：")
	page = 1
	def start_requests(self):
		if self.choice == '1':
			id = input("请输入你要查询的公众号id：")
			start_urls = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query='+id+'&ie=utf8&_sug_=n&_sug_type_='
			return [scrapy.Request(start_urls,callback=self.parse1)]
		
		elif self.choice == '2':
			key = input("请输入要查询的关键字：")
			maxNo = int(input('请输入查询的最大页码：'))
			return [scrapy.FormRequest(url='http://weixin.sogou.com/weixin',
                                    formdata={'type':'2',
                                            'ie':'utf8',
                                            'query':key,
                                            'tsn':'1',
                                            'ft':'',
                                            'et':'',
                                            'interation':'',
                                            'sst0': str(int(time.time()*1000)),
                                            'page': str(self.page),
                                            'wxid':'',
                                            'usip':''},
                                    method='get',
                                    meta={'key':key,'maxNo':maxNo},
                                    headers=self.headers,
                                    callback=self.parse2)]
		else:
			print('输入有误，程序退出')
			return

	def parse1(self, response):
		# 获取公众号URL
		publicUrl = response.xpath("//p[@class='tit']/a[@target='_blank']/@href").extract()[0]
		print("*********"+publicUrl+"************")
		yield scrapy.Request(publicUrl,cookies={'viewed':'"1083428"', '__utmv':'30149280.3975'},callback = self.parseArticleList)

	def parseArticleList(self,response):
		patt = re.compile(r'var msgList = (\{.*?\});')
		result = patt.search(response.text)
		url_list = json.loads(result.group(1))['list']
		for data in url_list:
			title = data['app_msg_ext_info']['title']
			article_url = data['app_msg_ext_info']['content_url']
			url = 'https://mp.weixin.qq.com' + article_url.replace(r'amp;', '')
			yield scrapy.Request(url,meta={'title':title}, callback=self.parseArticle)

	def parseArticle(self,response):
		item = WechatSpiderItem()
		item['title'] = response.meta['title']
		soup = BeautifulSoup(response.text, 'lxml')
		item['publishTime'] = soup.find('em',attrs={'class':'rich_media_meta rich_media_meta_text'}).get_text()
		item['article'] = soup.find('div', attrs={'class': 'rich_media_content '}).get_text()
		item['publicName'] = response.xpath("//a[@class='rich_media_meta rich_media_meta_link rich_media_meta_nickname']/text()").extract()[0]
		yield item
		 
	# 找到每一个文章的链接，组成一个列表，并对每一个链接实行第二个方法及爬取文章主体信息
	def parse2(self, response):
		key = response.meta['key']
		maxNo = response.meta['maxNo']
		soup = BeautifulSoup(response.text, 'lxml')
		node_soup = soup.find('ul', attrs={'class': 'news-list'})
		
		for node in node_soup.findAll('li'):
			url = node.select('div h3 a')[0]['href']
			yield scrapy.Request(url, callback=self.parseArticleBody)

		# 实现翻页爬取
		while self.page < maxNo:
        			self.page += 1
        			yield scrapy.FormRequest(url='http://weixin.sogou.com/weixin',
                           		formdata={'type': '2','ie': 'utf8','query': key,'tsn': '1','ft': '','et': '','interation': '','sst0': str(int(time.time() * 1000)),'page': str(self.page),'wxid': '','usip': ''},
				method='get',
				meta={'key':key,'maxNo':maxNo},
				headers=self.headers,
				callback=self.parse2)

	# 爬取每个文章的所需信息
	def parseArticleBody(self,response):
		item = WechatSpiderItem()
		item['title'] = response.xpath("//div[@id='img-content']/h2[@class='rich_media_title']/text()").extract()[0].strip().replace('\r','').replace('\n','').replace('\t','')
		soup = BeautifulSoup(response.text, 'lxml')
		item['publishTime'] = soup.find('em',attrs={'class':'rich_media_meta rich_media_meta_text'}).get_text()
		item['article'] = soup.find('div', attrs={'class': 'rich_media_content '}).get_text()
		item['publicName'] = response.xpath("//a[@class='rich_media_meta rich_media_meta_link rich_media_meta_nickname']/text()").extract()[0]
		yield item







		
