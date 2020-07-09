import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from JianShu_Spider.items import JianshuSpiderItem


class JsSpiderSpider(CrawlSpider):
    name = 'JS_Spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        avatar = response.xpath("//a[@class='_1OhGeD']/img/@src").get()
        author = response.xpath("//span[@class='FxYr8x']/a/text()").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        url = response.url
        url_1 =url.split("?")[0]
        article_id = url_1.split('/')[-1]
        content = response.xpath("//article[@class='_2rhmJa']").get()

        item = JianshuSpiderItem(
            title=title,
            avatar=avatar,
            pub_time=pub_time,
            origin_url = response.url,
            article_id = article_id,
            content=content
        )
        yield item


