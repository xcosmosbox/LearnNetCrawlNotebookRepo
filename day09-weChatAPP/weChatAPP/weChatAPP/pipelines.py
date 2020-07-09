# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter

class WechatappPipeline:

    # 打开一个json文件，并预备写入操作
    def open_spider(self, spider):
        # 操作提示
        print('Spider saving data……')
        # 创建一个json文件并预备写入操作
        # 下列代码中的 ‘wb’ 是指：以二进制的形式写入，即 write_binary
        # 又因为是以'wb'的形式打开，所有不能写encoding！
        self.fp = open('wxjc.json', 'wb')

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
