# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WechatSpiderItem(scrapy.Item):
	# 文章标题
	title = scrapy.Field()
	# 发布时间
	publishTime = scrapy.Field()
	# 文章内容
	article = scrapy.Field()
	# 公众号名字
	publicName = scrapy.Field()


