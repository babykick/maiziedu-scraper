#coding=utf-8
from maiziedu import COOKIES
from scrapy.exceptions import IgnoreRequest
from scrapy.conf import settings

class LimitFileSizeDownloaderMiddleware(object):
    """ Use headers to limit the file size
    """
    MAX_SIZE = 10000000
    
    def process_request(self, request, spider):
        file_size = request.headers
        if file_size > MAX_SIZE:
            raise scrapy.ignore


class CookiesCarryMiddleware(object):
    """ Add cookies to all requests
    """
    def process_request(self, request, spider):
        request.cookies = settings["COOKIES"]
    