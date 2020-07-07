import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList
from zhiHuCrawl.items import ZhihucrawlItem

class CrawledzhSpider(scrapy.Spider):
    name = 'crawledZH'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/topic/19577698/hot/']

    def parse(self, response):
        # print(type(response))  获取response的类型，结果是：scrapy.http.response.html.HtmlResponse

        # 根据下面的注释得到的结果类型我们知道了，content_block_divs是一个SelectorList类对象
        content_block_divs = response.xpath("//div[@class='List']/div/div")
        print('*' * 30)
        print(type(content_block_divs))
        print('*' * 30)
        # print('*'*30)
        # print(type(content_block_divs)) 此句打印了content_block_divs的类型，结果是：scrapy.selector.unified.SelectorList
        # print('*' * 30)

        # 根据上文的内容可知，此处的div的类型是一个Selector对象
        print('+' * 30)
        print(content_block_divs)
        for div in content_block_divs:
            author = div.xpath(".//h2[@class='ContentItem-title']/a/text()").get()
            content = div.xpath("//div[@class='AuthorInfo-content']//a[@class='UserLink-link']/text()").get()
            # content = "".join(content).strip()
            # author = "".join(content).strip()
            item = ZhihucrawlItem(author=author, content=content)
            yield item



        print('+' * 30)
