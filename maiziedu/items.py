# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

 
class MaiziSectionItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()       # 章节url
    title = scrapy.Field()      # 章节名
    course_name = scrapy.Field() # 课程名
    course_url = scrapy.Field()  # 课程url
    serial_name = scrapy.Field()
    file_urls = scrapy.Field()  # 下载文件地址
    size = scrapy.Field()
    content_type = scrapy.Field()