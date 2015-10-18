# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re, os
import sys
reload(sys)
sys.setdefaultencoding('gb2312')
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
        return re.sub(u'[\*\?\\/<>"]', "", s.strip())
    
    
    def process_item(self, item, spider):
        if int(item['size']) > 100000000 : # 大于100M用curl下载
            ext = item['file_urls'][0].split('.')[-1]
            folder = os.path.join(settings['FILES_STORE'],
                                 self.clean_file_name(item['serial_name']),
                                 self.clean_file_name(item['course_name']),
                                 )
            # 目标文件夹不存在则创建
            if not os.path.exists(folder):
                os.makedirs(folder)    
            fpath = os.path.join(folder, self.clean_file_name(item['title'] + '.' + ext)).encode('gb2312','ignore')
            # 如存在同名文件，认为已经下载过了，忽略
            if os.path.exists(fpath):
                raise DropItem("Duplicated item, file already downloaded, ignore")  
            #script = u'curl %s -o ' %  item['file_urls'][0] + '"' + fpath + '"'
            script = u'curl --cookie "%s" %s -o "%s"' % (settings['STR_COOKIES'], item['file_urls'][0] + '?wsiphost=local', fpath)
            print script
            subprocess.Popen(script)    #.wait() 测试wait会阻塞所以不用
            raise DropItem("oversized, passed to curl to download")
        return item
        
        