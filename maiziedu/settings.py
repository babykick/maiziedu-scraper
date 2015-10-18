# -*- coding: utf-8 -*-

# Scrapy settings for maiziedu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'maiziedu'

SPIDER_MODULES = ['maiziedu.spiders']
NEWSPIDER_MODULE = 'maiziedu.spiders'


# Custom settings
COOKIES = dict(line.split('\t')[0:2] for line in open('./cookies_dump.txt'))
STR_COOKIES = ";".join(k+"="+v for k, v in COOKIES.items()) 
# DOWNLOAD_MAXSIZE = 100000000
#DOWNLOADER_HTTPCLIENTFACTORY = 'maiziedu.downloader.LimitSizeHTTPClientFactory'
DOWNLOAD_TIMEOUT = 180
DOWNLOAD_WARNSIZE = 200000000 # 200M
CONCURRENT_ITEMS = 100 # Maximum number of concurrent items (per response) to process in parallel in the Item Processor (Pipeline)
CONCURRENT_REQUESTS = 10 # 同时并发下载数目, 内存不够的情况下，小并发可以减小内存消耗，减少内存错误发生几率


# Breath-first order
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'maiziedu (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'maiziedu.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'maiziedu.middlewares.LimitFileSizeDownloaderMiddleware': 560,
   #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None, # disable default
   #'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 1, # default include
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'maiziedu.pipelines.SomePipeline': 300,
#}

ITEM_PIPELINES = {
                  'maiziedu.pipelines.MaizieduPipeline': 200,
                  'maiziedu.pipelines.CurlDownloadPipeline':100,
                  }

FILES_STORE = 'g:\\lessons'


#FILES_EXPIRES = 0
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
