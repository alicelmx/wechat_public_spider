# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from pymysql import connections

class WechatSpiderPipeline(object):
	def __init__(self):
		# 连接数据库
		self.conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='bamajie521mysql',db='alicelmx',charset='utf8mb4')
		self.cursor = self.conn.cursor() 

	def process_item(self, item, spider):
		
		# 向表中插入数据
		title= item['title']
		publishTime = item['publishTime']
		article = item['article']
		publicName = item['publicName']
		
		# 查询是否有标题和公众号名称相同的元组
		self.cursor.execute("select title from wechatArticle;")
		titleList = self.cursor.fetchall()
		titleStr = ''.join(map(str,titleList))
		
		self.cursor.execute("select publicName from wechatArticle;")
		nameList = self.cursor.fetchall()
		nameStr = ''.join(map(str,nameList))

		if titleStr.find(title) == -1 and nameStr.find(publicName) == -1:
			# 插入的sql语句
			sql="""INSERT INTO wechatArticle 
			         (title,publishTime,article,publicName) 
			         VALUES 
			         (%s,%s,%s,%s)
			     """
			self.cursor.execute(sql,(title,publishTime,article,publicName))
			self.conn.commit()
		else:
			print("该文章已经存在在数据库中！")
		return item
   
	def close_spider(self,spider):
		self.conn.close()
