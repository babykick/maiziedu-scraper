#coding=utf-8
 
from scrapy.exceptions import IgnoreRequest
from scrapy.conf import settings
from scrapy import Request
from scrapy.http import Response

class LimitFileSizeDownloaderMiddleware(object):
    """ Use headers to limit the file size
    """
    MAX_SIZE = 10000000
    
    def process_request(self, request, spider):
        # file_size = request.headers
        # print "In middleware", file_size
        # if file_size > MAX_SIZE:
        #     raise scrapy.ignore
        if 'mp4' not in request.url: return None
        print 'mp4-----------------------------------'
        return Request(request.url, method="HEAD", cookies=settings["COOKIES"],
                         dont_filter=True, callback=self.parse_it)
        
    def parse_it(self, response):
        print response.headers
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    
    # def process_response(self, request, response, spider):
    #     file_size = request.headers
    #     print "In middleware", file_size
    # 


class CookiesCarryMiddleware(object):
    """ Add cookies to all requests
    """
    def process_request(self, request, spider):
        request.cookies = settings["COOKIES"]
    