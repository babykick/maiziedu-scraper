# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from maiziedu.items import MaiziSectionItem 
import urlparse
from maiziedu import COOKIES



class CourseSpider(scrapy.Spider):
    name = "course_spider"
    #allowed_domains = ["maiziedu.com"]
    home_page = 'http://www.maiziedu.com/'
    start_urls = ( 'http://www.maiziedu.com/course/',
                  )
     
    
    def __init__(self, serial=None, courses=None, *args, **kwargs):
        super(CourseSpider, self).__init__(*args, **kwargs)
        self.serial = serial
        self.courses = courses
        # serial为一个系列名称
        if self.serial is not None:
            self.serial = self.serial.decode('gb2312').strip()
          
        # courses为一个课程名list
        if self.courses is not None:
            self.courses = self.courses.decode('gb2312').strip().split(',')
         
             
     
    def parse(self, response):
        """ 抓取所有系列 
        """
        self.log('parse course serials')
        for ele in response.xpath('//ul[contains(@class, "course_list")]/li'):
            url = ele.xpath("./a/@href").extract_first()
            url = urlparse.urljoin(self.home_page, url)
            serial_name = ele.xpath('./a/@title').extract_first().strip()
            # 过滤需要爬取的系列，按名称 unicode
            if self.serial is not None and serial_name != self.serial: continue
            #print serial_name
            yield Request(url=url, callback=self.parse_course_list,
                          meta={'serial':serial_name},
                          dont_filter=True)
            
    def parse_course_list(self, response):
        """ 抓取该系列下所有课程链接
        """
        self.log('parse courses')
        for ele in response.xpath('//article/div/a'):
            rurl = ele.xpath('./@href').extract_first()
            course_name = ele.xpath('./@title').extract_first().strip()
            course_url = urlparse.urljoin(self.home_page, rurl)
    
            # 过滤需要爬取的课程，按名称 unicode
            if self.courses is not None and course_name not in self.courses:
                   continue
            #print course_name
            yield Request(url=course_url, callback=self.parse_course,
                          meta={'course_name':course_name,
                                'course_url':course_url,
                                'serial':response.meta['serial']},
                          cookies=COOKIES,
                          dont_filter=True)
    
    
    def parse_course(self, response):
        """ 抓取一个课程所有章节
        """
        self.log('parse out course all sections')
        # item['course_name'] = response.xpath('//dl[@class="course-lead"]/dt/text()').extract_first()
        for ele in response.xpath('//div[contains(@class, "playlist")]/ul/li/a'):
            item = MaiziSectionItem()
            lesson_url  = ele.xpath('./@href').extract_first()
            item['course_url'] = response.meta['course_url']
            item['course_name'] = response.meta['course_name']
            item['serial_name'] = response.meta['serial']
            item['url']= urlparse.urljoin(self.home_page, lesson_url)
            item['title'] = ele.xpath('./text()').extract_first()
            yield Request(url=item['url'], meta={'item':item},
                          callback=self.parse_lesson, cookies=COOKIES,
                          dont_filter=True)
            
            
    def parse_lesson(self, response):
        """ 解析课程章节页面，生成包含视频下载链接的item
        """
        self.log('parse lesson')
        item = response.meta['item']
        src = response.xpath('//video/source/@src')
        if src:
            src = src.extract_first()
            item['file_urls'] = [src]
            yield item
                                  
            
