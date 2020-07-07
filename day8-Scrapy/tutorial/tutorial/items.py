# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    '''
        根据scrapy框架源码`item.py`中的代码 ‘class Field(dict):’ 可知：我们创建了一个字典模型
        下面是规定的作者和作者内容的scrapy.Field类
    '''
    author = scrapy.Field()
    content = scrapy.Field()
