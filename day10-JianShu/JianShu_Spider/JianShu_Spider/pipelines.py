# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class JianshuSpiderPipeline:
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'port':'3306',
            'user':'root',
            'password':'root',
            'database':'jianshu',
            'charset':'utf8'

        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['title'],item['content'],item['author'],item['avatar'],item['pub_time'],item['origin_url'],item['article_id'],))
        self.conn.commit()
        return item



    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,avatat,pub_time,origin_url,article_id) values(null,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


