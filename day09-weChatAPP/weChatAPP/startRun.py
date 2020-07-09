from scrapy import cmdline

#利用这一行指令去调用控制台，scrapy框架下的爬虫不能简单的通过main函数调用（因为真正的mian函数隐藏在scrapy框架的源代码中），需要我们通过控制台去调用框架引擎，引擎来调用我们写的爬虫
cmdline.execute("scrapy crawl wxapp_spider".split())