# Scrapy settings for zhiHuCrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhiHuCrawl'

SPIDER_MODULES = ['zhiHuCrawl.spiders']
NEWSPIDER_MODULE = 'zhiHuCrawl.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhiHuCrawl (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Content-Type':'text/html; charset=utf-8',
    'Referer':'https://www.zhihu.com/topic/19577698/hot',
    'Cookie':'SESSIONID=6URHwILcybpRw6I0QVjCHrrXmTtEXwotqkulpz2hwgm; JOID=V18RAUoN4aiSw-12PwqHt6UtC_gvLMGNsuTMVhoqwIi348pXH3A7r8rF7HM6SA0aCczIeFI9XNfl4waYcm_p4Js=; osd=UFEQAU8K76mSxup4PgqCsKssC_0oIsCNt-PCVxovx4a2489QEXE7qs3L7XM_TwMbCcnPdlM9WdDr4gaddWHo4J4=; SESSIONID=mHDGLsqwGEHoknTY2APVU3O13Wx7sDldE7lhTmEUSy9; JOID=W1ocAU5eBHSaazadaFUTr-ASCxN5dixcvkQetUBxLFyyTxm1QFAye85sNp1krv7c03jQGEhek07jpM20ZliOotI=; osd=U14WAkhWAH6ZbT6ZYlYVp-QYCBVxciZfuEwav0N3JFi4TB-9RFoxfcZoPJ5ipvrW0H7YHEJdlUbnrs6yblyEodQ=; _zap=0a72c541-7f12-431d-8d4c-0f6904b72b1a; _xsrf=giFyjBU3haRqYA8lLPZcXZQQwkSaeVxn; d_c0="AKDhKszR3g-PTkMIIV5QxWeYmyByvhuH3iM=|1565431202"; __utmv=51854390.100--|2=registration_date=20170719=1^3=entry_date=20170719=1; _ga=GA1.2.361522463.1566720057; z_c0="2|1:0|10:1582989635|4:z_c0|92:Mi4xaXBkNUJRQUFBQUFBb09FcXpOSGVEeVlBQUFCZ0FsVk5RODlIWHdEM3JfZVl6SUJHRHFjeEFyMzFmTkNnemtVOXhn|652a57673aa274717fec2b18d49118b787a1946356a47c8395f72623ccfbbaba"; __utma=51854390.361522463.1566720057.1583037962.1583040747.5; __utmz=51854390.1583040747.5.4.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/40282843; q_c1=a5da9dd1bd7b4dd195c1c8eff1613475|1592026350000|1565431664000; _gid=GA1.2.243219722.1593942284; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1594022699,1594022700,1594022707,1594022710; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1594045978; KLBRSID=d1f07ca9b929274b65d830a00cbd719a|1594048778|1594045959'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhiHuCrawl.middlewares.ZhihucrawlSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhiHuCrawl.middlewares.ZhihucrawlDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'zhiHuCrawl.pipelines.ZhihucrawlPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
