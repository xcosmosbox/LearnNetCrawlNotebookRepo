# WebSpider HighLevel

## 1.Scrapy框架

### Scrapy框架介绍：

写一个爬虫需要做很多事情。比如：发送网络请求，数据解析、数据存储、反反爬虫机制（ip代理、设置请求头等等）、异步请求等。这些工作如果每次都从头开始写，就比较浪费时间。因此`Scrapy`把一些基础的东西封装好了，在此基础上写爬虫会更加的高效（爬取效率和开发效率）。

### Scrapy架构图：

#### 1.流程图

![14946794-c32c1356bb94c85c](https://upload-images.jianshu.io/upload_images/14946794-c32c1356bb94c85c.jpg)



#### 2.框架原理图

![58f497eb07a387c7ef891805ea07add3](https://img-blog.csdn.net/20180502174530976)



### Scrapy框架模块功能：

1. `Scrapy Engine`：`Scrapy`框架的核心部分。负责在`Spider`和`ItemPipeline`、`Downloader`、`Scheduler`中间通信、传递数据等。
2. `Spider`：发送需要爬取的链接给引擎，最后引擎把其它模块请求回来的数据再发送给爬虫，爬虫就去解析想要的数据。这个部分需要开发者自己手写，因为要爬取那些链接，页面中的那些是我们需要的，都是由程序员自己决定的。
3. `Scheduler`：负责接收引擎发送过来的请求，并按照一定的方式进行排列和整理，负责调度请求的顺序等等。
4. `Downloader`：负责接收引擎传过来的下载请求，然后去网络上下载对应的数据再交还给引擎。
5. `Item Pipeline`：负责将`Spider`传递过来的数据进行保存。具体保存在哪里，需要看开发者自己的需求。
6. `Downloader Middlewares`：可以扩展下载器和引擎之间通信功能的中间件。
7. `Spider Middlewares`：可以扩展引擎和爬虫之间通信功能的中间件。



### 创建项目和爬虫：

1. 创建项目：`scrapy startproject [projectName]`
2. 创建爬虫：进入到项目所在的路径，执行命令：`scrapy genspider [spiderName] {spiderURL}`。注意，爬虫名字不能和项目名称一致。



### 项目目录结构：

1. `items.py`：用来保存爬取下来数据的容器。
2. `middlewares.py`：用来保存各种中间件的文件
3. `pipelines.py`：用来将items的容器存储到本地的磁盘中
4. `settings.py`：爬虫的一些配置信息（比如请求头、多久发送一次请求、ip代理池等等）
5. `scrapy.cfg`：项目的配置文件
6. `spiders package`：以后所有的爬虫，都可以存放到这个里面



### 框架练习

#### 源代码

```python
#tutorial
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
```



```python
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json

class TutorialPipeline:
    #打开一个json文件，并预备写入操作
    def open_spider(self,spider):
        #操作提示
        print('Spider saving data……')
        #创建一个json文件并预备写入操作
        self.fp = open('saveContentData.json','w',encoding='utf-8')

    #向json中写入数据
    #item来自scrapy引擎从爬虫中获取的迭代器
    def process_item(self, item, spider):
        #将传入的字典数据包装在一个json对象中
        #ensure_ascii=False的作用是为了能够正常显示中文
        item_json = json.dumps(dict(item),ensure_ascii=False)
        #将json对象中的数据写入json文件中
        self.fp.write(item_json+'\n')
        return item

    #关闭json文件
    def close_spider(self,spider):
        # 操作提示
        print('Saving data success!')
        #关闭json文件的写入通道
        self.fp.close()
```



#### 练习笔记

1. `response`是一个`scrapy.http.response.html.HtmlResponse`对象。可以执行`xpath`和`css`语法来提取数据

2. 提取出来的数据，是一个`Selector`或者是一个`SelectorList`对象。如想要获取其中的字符串，那么需要执行`getall`或者`get`方法

   1. `getall`：获取`Selector`中的所有文本。返回的是一个列表。
   2. `get`：获取的是`Selector`中的第一个文本。返回的是一个string类型

3. 如果数据解析回来，要传给`pipelines`处理，那么可以使用`yield`来返回（返回给引擎，引擎传输给`pipelines`）一个迭代器`item`

4. `item`：在`items.py`中定义好模型。以后就不需要手动定义了，降低了耦合度

5. `pipelines`：专门用来保存数据的。其中有三个常用方法：

   1. `open_spider(self,spider)`：当爬虫被打开的时候执行。
   2. `process_item(self, item, spider)`：当爬虫有item传过来的时候会被调用。
   3. `close_spider(self,spider)`：当爬虫关闭的时候会被调用。

6. 要激活`pipelines`，需要提前在`settings.py`中，将`ITEM_PIPELINES`激活（将其从注释状态改成代码状态），示例如下：

   ```python
   ITEM_PIPELINES = {
      'tutorial.pipelines.TutorialPipeline': 300,
   }
   ```

7. 例如`User-Agent`等也需要在`settings.py`中，将`DEFAULT_REQUEST_HEADERS`激活（将其从注释状态改成代码状态），示例如下：

   ```python
   DEFAULT_REQUEST_HEADERS = {
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Language': 'en',
     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
   }
   ```

   



### ⭐yield语句详解：

#### 1.初步了解功能

在外面还没有完全明白之前，我们首先把yield看做“return”，这个是最直观的，它首先是个return，return是什么意思，就是在程序中返回某个值，返回之后程序就**不再往下运行了**。看做return之后再把它看做一个是生成器（generator）的一部分（带yield的函数才是真正的迭代器），为了弄明白yield真正的作用，下述代码将会展示：

```python
def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)
g = foo()
print(next(g))
print("*"*20)
print(next(g))

>>> 结果：
starting...
4
********************
res: None
4
```

***代码解释：***

1. 程序开始执行以后，因为foo函数中有yield关键字，所以foo函数并不会真的执行，而是先得到一个生成器g(相当于一个对象)
2. 直到调用next方法，foo函数正式开始执行，先执行foo函数中的print方法，然后进入while循环
3. 程序遇到yield关键字，然后把yield想想成return,return了一个4之后，程序停止，并没有执行赋值给res操作，此时next(g)语句执行完成，所以输出的前两行（第一个是while上面的print的结果,第二个是return出的结果）是执行print(next(g))的结果。
4. 程序执行print("*"*20)，输出20个*
5. 又开始执行下面的print(next(g)),这个时候和上面那个差不多，不过不同的是，这个时候是从刚才那个next程序停止的地方开始执行的，也就是要执行res的赋值操作，这时候要注意，这个时候赋值操作的右边是没有值的（因为刚才那个是return出去了，并没有给赋值操作的左边传参数），所以这个时候res赋值是None,所以接着下面的输出就是res:None
6. 程序会继续在while里执行，又一次碰到yield,这个时候同样return 出4，然后程序停止，print函数输出的4就是这次return出的4.

到这里就明白yield和return的关系和区别了，带yield的函数是一个生成器，而不是一个函数了，这个生成器有一个函数就是next函数，next就相当于“下一步”生成哪个数，这一次的next开始的地方是接着上一次的next停止的地方执行的，所以调用next的时候，生成器并不会从foo函数的开始执行，只是接着上一步停止的地方开始，然后遇到yield后，return出要生成的数，此步就结束。（总的来说，yield就是一个每一次执行都会暂停的return，并且下次执行是从暂停的位置开始，而不是从方法的最前面开始）。

#### 2.举例练习：

```python
def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)
g = foo()
print(next(g))
print("*"*20)
print(g.send(7))

>>> 结果：
starting...
4
********************
res: 7
4
```

***代码解释：***先大致说一下send函数的概念：此时你应该注意到上面那个的紫色的字，还有上面那个res的值为什么是None，这个变成了7，到底为什么，这是因为，send是发送一个参数给res的，因为上面讲到，return的时候，并没有把4赋值给res，下次执行的时候只好继续执行赋值操作，只好赋值为None了，而如果用send的话，开始执行的时候，先接着上一次（return 4之后）执行，先把7赋值给了res,然后执行next的作用，遇见下一回的yield，return出结果后结束。

1. 程序执行g.send(7)，程序会从yield关键字那一行继续向下运行，send会把7这个值赋值给res变量
2. 由于send方法中包含next()方法，所以程序会继续向下运行执行print方法，然后再次进入while循环
3. 程序执行再次遇到yield关键字，yield会返回后面的值后，程序再次暂停，直到再次调用next方法或send方法。

#### 3.使用yield的原因：

使用yield就是使用一个生成器，之所以使用生成器而不是列表，是因为列表会占用大量的空间，例如：

```python
for n in range(1000):
    a=n
```

这个时候range(1000)就默认生成一个含有1000个数的list了，所以很占内存。（此点在py3之后已被优化，但这仅仅是被官方优化的一个常见类型，在实际开发中，我们需要自己对所需要的信息进行创建生成器，例如上一节中的爬虫实例，通过生成器去迭代网页中所有的作者名和内容，并传递给`pipelines`）



### 优化数据存储

`JsonItemExporter`和`JsonLinesItemExporter`

1. `JsonItemExporter`：这个是每次把数据添加到内存中。最后统一写入磁盘中，好处是存储的数据是一个满足json规则的数据。坏处是如果数据量太大，那么比较耗内存。

   ```python
       # 打开一个json文件，并预备写入操作
       def open_spider(self, spider):
           # 操作提示
           print('Spider saving data……')
           # 创建一个json文件并预备写入操作
           # 下列代码中的 ‘wb’ 是指：以二进制的形式写入，即 write_binary
           # 又因为是以'wb'的形式打开，所有不能写encoding！
           self.fp = open('saveContentData.json', 'wb')
   
           #利用 JsonItemExporter 创建导出器
           self.exporter = JsonItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
   
           #开始执行导出器
           self.exporter.start_exporting()
   
       # 向json中写入数据
       # item来自scrapy引擎从爬虫中获取的迭代器
       def process_item(self, item, spider):
           self.exporter.export_item(item)
           return item
   
       # 关闭json文件
       def close_spider(self, spider):
           #完成导入
           self.exporter.finish_exporting()
   
           # 关闭json文件的写入通道
           self.fp.close()
   
           # 操作提示
           print('Saving data success!')
   ```

   

2. `JsonLinesItemExporter`：这个是每次调用`export_item`的时候就把item存储到磁盘中。坏处是每一个字典是一行，整个文件不是一个完全满足json格式的文件。好处是处理数据的时候就直接存储到了磁盘中，这样不耗费内存，数据比较安全。

   ```python
       # 打开一个json文件，并预备写入操作
       def open_spider(self, spider):
           # 操作提示
           print('Spider saving data……')
           # 创建一个json文件并预备写入操作
           # 下列代码中的 ‘wb’ 是指：以二进制的形式写入，即 write_binary
           # 又因为是以'wb'的形式打开，所有不能写encoding！
           self.fp = open('saveContentData.json', 'wb')
   
           #利用 JsonLinesItemExporter 创建导出器
           self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
   
       # 向json中写入数据
       # item来自scrapy引擎从爬虫中获取的迭代器
       def process_item(self, item, spider):
           self.exporter.export_item(item)
           return item
   
       # 关闭json文件
       def close_spider(self, spider):
           # 关闭json文件的写入通道
           self.fp.close()
   
           # 操作提示
           print('Saving data success!')
   ```

   

### 一次性爬取多个页面

```python
            '''功能区三：自动请求下一个页面并爬取，且能在最后一页停止爬取'''
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url,callback=self.parse)
```



### CrawlSpider

有时我们需要爬虫以某种指定的规则爬取url，只要那个url满足我们指定的条件，就将其内容爬取下来。那么这是我们就可以通过`CrawlSpider`来完成了。`CrawlSpider`继承自`Spider`，只不过是在之前的基础上增加了新的功能，可以定义爬虫的url规则，以后scrapy碰到满足条件的url都进行爬取，而不需要我们手动`yield Request`了。

需要使用`LinkExtractor`和`Rule`这两个东西决定爬虫给的具体走向：

1. allow设置规则的方法：要能够限制在我们想要的url上面，不要跟其他url产生相同的正则表达式即可。
2. 什么情况下使用follow:如果在爬取页面的时候，需要将满足当前条件的url再进行跟进，那么就设置为True。否则设置为False.
3. 什么情况下该指定callback:如果这个url对应的页面，只是为了获取更多的url，并不需要里面的数据，那么可以不指定callback。如果想要获取url对应的页面中的数据，那么就需要指定一个callback来进行数据的处理，储存等。

#### 创建CrawlSpider

如果想要创建`CrawlSpider`，那么需要通过以下指令：

```shell
scrapy genspider -t crawl [spiderName] [url]
```



#### LinkExtractors链接提取器

使用`LinkExtractors`可以不用程序员自己提取想要的url，然后发送请求。这些工作都可以交给`LinkExtractors`，他会在所有爬的页面这种找到满足规则的url，实现自动爬取。

```python
class scrapy.linkextractors.LinkExtractor(
	allow=(),    #允许的url  所有满足这个正则表达式的url都会被提取
    deny=(),	#禁止的urkl  所有满足这个正则表达式的url都不会被提取
    allow_domains(),  #允许的域名  只有在这个里面指定的域名的url才会被提取
    deny_extensions=None, 
    restrict_xpaths=(),  #严格的xpath和allow共同过滤链接
    tahs=('a','area'),
    attrs=('herf'),
    unique=True,
    process_value=None
)
```

主要参数讲解：

- allow：运行的url。所有满足这个正则表达式的url都会被提取。
- deny：禁止的url。所有满足这个正则表达式的url都不会被提取。
- allow_domains：允许的域名。只有在这个里面指定的url才会被提取。
- deny_domians：禁止的域名。所有在这个里面指定的域名的url都不会被提取。
- restrict_xpaths：严格的xpath。和allow共同过滤链接。



#### Rule规则类：

定义爬虫的规则类。以下对这个类做一个简单介绍：

```python
class scrapy.spiders.Rule(
link_extractor,
    callback=None, #满足这个规则的url就应该执行哪个回调函数.因为CrawlSpider使用了parse作为回调函数,因此不要副高parse作为回调函数自己的回调函数
    cb_kwargs=None, 
    follow=None,   # 是否需要跟进默认True
    process_links=None,   # 从link_extractor中获取到连接后会传递给这个函数,用来过滤不需要爬取的连接
    process_request=None  
)
```

主要参数讲解：

- link_extractor：一个`LinkExtractors`对象，用于定义爬取规则。
- callback：满足这个规则的url，应该要执行那个回调函数。因为`CrawlSpider`使用了`parse`作为回调函数，因此不要覆盖`parse`作用回调函数自己的函数。
- follow：指定根据该规则从response中提取的链接是否需要跟进。
- process_links：从`link_extractor`中获取到链接后会传递这个函数，用来过滤不需要爬取的链接。



### Request和Response对象

1. Request对象

   ```python
   class Request(object_ref):
   
       def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                    cookies=None, meta=None, encoding='utf-8', priority=0,
                    dont_filter=False, errback=None, flags=None, cb_kwargs=None):
   
           self._encoding = encoding  # this one has to be set first
           self.method = str(method).upper()
           self._set_url(url)
           self._set_body(body)
           assert isinstance(priority, int), "Request priority not an integer: %r" % priority
           self.priority = priority
   
           if callback is not None and not callable(callback):
               raise TypeError('callback must be a callable, got %s' % type(callback).__name__)
           if errback is not None and not callable(errback):
               raise TypeError('errback must be a callable, got %s' % type(errback).__name__)
           self.callback = callback
           self.errback = errback
   
           self.cookies = cookies or {}
           self.headers = Headers(headers or {}, encoding=encoding)
           self.dont_filter = dont_filter
   
           self._meta = dict(meta) if meta else None
           self._cb_kwargs = dict(cb_kwargs) if cb_kwargs else None
           self.flags = [] if flags is None else list(flags)
   
   
   ```

   Request对象在我们写爬虫，爬取一页的数据需要重新发送一个请求的时候调用。这个类需要传递一些参数，其中比较常用的参数有：

   1. `url`:这个request对象发送请求的url。
   2. `callback`:在下载器下载完相应的数据后执行的回调函数。
   3. `method`:请求的方法。默认为GET方法，可以设置为其他方法。
   4. `headers`:请求头，对于一些固定的设置，放在settings.py中指定就可以了。对于那些非固定的，可以在发送请求的时候指定
   5. `meta`:比较常用。用于在不同的请求之间传递数据用的。
   6. `encoding`:编码，默认的为utf-8,使用默认的就可以了
   7. `dont_filter`:表示不由调度器过滤，在执行多次重复的请求的时候用得比较多。比如验证码。
   8. `errback`:在发生错误的时候执行的函数

   

2. Response对象

   Response对象一般是有scrapy给你自动构建的。因此开发者不需要关心如何创建response对象，而且如何使用他。response对象有很多属性，可以用来提取数据的。主要有以下属性：

   1. `meta`：从其他请求传过来的`meta`属性，可以用来保持多个请求之间的数据连接。
   2. `encoding`：返回当前字符串编码和解码的格式
   3. `text`:将返回的数据作为`unicode`字符串返回
   4. `body`：将返回来的数据作为`bytes`字符串返回
   5. `xpath`：xpath选择器
   6. `css`：css选择器

   发送POST请求：

   如果需要post请求的话，就需要使用`Request`的子类`FormRequest`来实现，如果想要在爬虫一开始的时候就发送给`POST`请求的话，那么需要在爬虫类中重写`start_requests(self)`方法，并且不再调用`start_urls`里的`url`.



















