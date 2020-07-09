#导包
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList
from tutorial.items import TutorialItem

#这个类会被 Scrapy 的引擎调用
class Tutorialdemo1Spider(scrapy.Spider):
    name = 'tutorialDemo1'
    #用于确定被爬取的域名范围
    allowed_domains = ['qiushibaike.com']
    #从以下url开始爬取
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    #自动爬取下一页时，使用这个基础域名加下一页的后缀，组合成下一页的url
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        '''功能区一：爬取网页上所有的作者以及作者的内容'''
        # print(type(response))  获取response的类型，结果是：scrapy.http.response.html.HtmlResponse
        #根据下面的注释得到的结果类型我们知道了，content_block_divs是一个SelectorList类对象
        content_block_divs = response.xpath("//div[@class='col1 old-style-col1']/div")
        # print('*'*30)
        # print(type(content_block_divs)) 此句打印了content_block_divs的类型，结果是：scrapy.selector.unified.SelectorList
        # print('*' * 30)

        #根据上文的内容可知，此处的div的类型是一个Selector对象
        for div in content_block_divs:
            #爬取作者名字
            author = div.xpath(".//h2/text()").get().strip()
            #爬取对应作者的内容
            content = div.xpath(".//div[@class='content']//text()").getall()
            #将对应作者的内容以str的类型存储，并利用 strip() 消除前后空格
            content = "".join(content).strip()

            # 将存储在 `items.py` 中的字典模型拉取到本地， 并按要求录入指定的数据
            # 之所以使用模型区创建字典，一个是创建跟简单，另一个是利用这样指针的方式创建，耦合度更低
            item = TutorialItem(author=author,content=content)
        #########################################################################

            '''功能区二：将功能区一中爬取到的所有内容存储到json文件中'''
            #根据scrapy框架的原理，我们需要将存储的信息放在’pipeline.py‘中
            # yield的作用是把一个普通的函数变成一个生成器，当遍历生成器时，它会将里面的内容一个一个的返回去。
            # yield 返回的是一个 `item` 的 `迭代器` 对象，返回给了Scrapy引擎中，引擎会将这个迭代器传给`pipeline.py`进行处理
            yield item
            #########################################################################

            '''功能区三：自动请求下一个页面并爬取，且能在最后一页停止爬取'''
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url,callback=self.parse)











