#coding=utf-8

from scrapy.core.downloader.webclient import ScrapyHTTPClientFactory, ScrapyHTTPPageGetter

MAX_RESPONSE_SIZE = 1048576 # 1Mb

class LimitSizePageGetter(ScrapyHTTPPageGetter):
    def handleHeader(self, key, value):
        ScrapyHTTPPageGetter.handleHeader(self, key, value)
        if key.lower() == 'content-length' and int(value) > MAX_RESPONSE_SIZE:
            self.connectionLost('oversized')
            
            
class LimitSizeHTTPClientFactory(ScrapyHTTPClientFactory):
     protocol = LimitSizePageGetter