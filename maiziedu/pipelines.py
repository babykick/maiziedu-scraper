# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re, os
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from scrapy.conf import settings

class MaizieduPipeline(FilesPipeline):
    def clean_file_name(self, s):
        return re.sub('[\*\?\\/<>"]', "", s)
    
    def file_path(self, request, response=None, info=None):
        """ 按 "课程系列/课程/章节" 组织目录
        """
        item = request.meta['item']
        ext = item['file_urls'][0].split('.')[-1]
        fpath = os.path.join(self.clean_file_name(item['serial_name']),
                             self.clean_file_name(item['course_name']),
                             self.clean_file_name(item['title'] + '.' + ext))
        
        return fpath.encode('gb2312', 'ignore')
      
    
    def get_media_requests(self, item, info):
        print info
        for url in item['file_urls']:
            yield Request(url=url, meta={'item':item}, cookies=settings["COOKIES"],
                          dont_filter=False)
     
 