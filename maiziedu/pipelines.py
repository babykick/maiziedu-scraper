# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re, os
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from scrapy.conf import settings
import subprocess
from scrapy.exceptions import DropItem

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
        url = item['file_urls'][0] 
        yield Request(url=url, meta={'item':item}, cookies=settings["COOKIES"],
                      dont_filter=False )
        
         

     
class CurlDownloadPipeline(object):
    """ Use curl to download file
    """
   
    def clean_file_name(self, s):
        return re.sub(u'[\*\?\\/<>"]', "", s)
    
    
    def process_item(self, item, spider):
        if int(item['size']) > 100 : # 大于100M用curl下载
            ext = item['file_urls'][0].split('.')[-1]
            fpath = os.path.join(settings['FILES_STORE'],
                                 self.clean_file_name(item['serial_name']),
                                 self.clean_file_name(item['course_name']),
                                 )
            if not os.path.exists(fpath): os.makedirs(fpath)
            fpath = os.path.join(fpath, self.clean_file_name(item['title'] + '.' + ext))
            fpath =  fpath.encode('gb2312', 'ignore').decode('gb2312', 'ignore')
            print fpath
            prefix = u'curl --cookie %s %s -o ' % (settings['STR_COOKIES'], item['file_urls'][0])
            print prefix
            subprocess.Popen(prefix +  fpath)
            # subprocess.call('curl --cookie %s --cookie-jar cookies.txt %s -o %s' % (settings["STR_COOKIES"],
            #                                                                         item['file_urls'][0], item[''],
            #                                                                         fpath))
            raise DropItem("oversized, passed to curl to download")
        return item
        
        