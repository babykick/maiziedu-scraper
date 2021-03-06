# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from maiziedu.items import MaiziSectionItem 
import urlparse
from scrapy.conf import settings

COOKIES = settings["COOKIES"]

 
class CourseSpider(scrapy.Spider):
    name = "course_spider"
    #allowed_domains = ["maiziedu.com"]
    home_page = 'http://www.maiziedu.com/'
    start_urls = ( 'http://www.maiziedu.com/course/',
                  )
     

    def __init__(self, serial=None, courses=None, course_url=None, *args, **kwargs):
        super(CourseSpider, self).__init__(*args, **kwargs)
        self.serial = serial
        self.courses = courses
        self.course_url = course_url
        
    
    def start_requests(self):
        if self.course_url is not None:  # 指定单一课程的url
            yield Request(self.course_url, callback=self.parse_course, meta={'serial': self.course_url.rstrip('/').split('/')[-1]})
        else:    
            # serial为一个系列名称
            self.serial = self.serial.decode('gb2312').strip() if self.serial is not None else self.serial
            # courses为一个课程名list
            self.courses = self.courses.decode('gb2312').strip().split(',') if self.courses is not None else self.courses
            for url in self.start_urls:
                yield Request(url, callback=self.parse)
              
         
     
    def parse(self, response):
        """ 抓取所有企业直通班系列 
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
                          meta={#'course_name':course_name,
                                #'course_url':course_url,
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
            lesson_url = ele.xpath('./@href').extract_first()
            item['course_url'] = response.url #.meta['course_url']
            item['course_name'] = response.css('.course-lead').xpath('./dt/text()').extract_first().strip() # .meta['course_name']
            item['serial_name'] = response.meta['serial']
            item['url']= urlparse.urljoin(self.home_page, lesson_url)
            item['title'] = ele.xpath('./text()').extract_first().replace(u"\xa0","").strip()
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
            yield Request(src, method="HEAD", meta={'item':item}, cookies=settings["COOKIES"],
                         dont_filter=True, callback=self.parse_item)
            
            
    def parse_item(self, response):
        content_type = response.headers['Content-Type']
        size = response.headers['Content-Length']
        item = response.meta['item']
        item['size'] = size
        item['content_type'] = content_type
        yield item
                                  
            
