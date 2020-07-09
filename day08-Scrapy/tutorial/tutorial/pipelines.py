# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exporters import JsonItemExporter,JsonLinesItemExporter

class TutorialPipeline:
    """版本三：以JsonLinesItemExporter的形式生成导出器，优点是自动开启自动关闭，并且是一个字典占一行，不会出现所有字典挤在json文件中一行的情况。在保证了输出形式的同时也保证了运行性能和规范化"""
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


"""版本二：JsonItemExporter的方式，缺点是，所有的字典都被挤到了json文件中的一行

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



"""











"""版本一：最原始的方式
#####  以下代码是由我们手动创建json文件并写入，但实际上scrapy提供了导出器供使用者使用，所有以下代码仅作为练习，上面的代码才是用导出器实现的。
#####
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
"""