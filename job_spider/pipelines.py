# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import dbtools_1 as db
import time



class JobSpiderPipeline(object):
    def __init__(self):
        self.conn = db.link('mysql')
        self.conn = self.conn.raw_connection()
        self.cursor = self.conn.cursor()
        self.table = 'qcwy_job'
        self.count = 0

    def insert(self, item):
        sql = 'INSERT IGNORE INTO ' + self.table + '('
        cols = item.fields.keys()
        for col in cols:
            sql += col + ','
        sql = sql[:-1] + ') VALUES('
        for _ in cols:
            sql += '%s,'
        sql = sql[:-1] + ')'
        self.cursor.execute(sql, tuple((item.get(i) for i in cols)))

    # 根据spider.name格式化要插入的表名
    def open_spider(self, spider):
        self.table = self.table
        print(time.strftime('%Y-%m-%d %H:%M:%S'))

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

        print(time.strftime('%Y-%m-%d %H:%M:%S'))

    def process_item(self, item, spider):
        self.insert(item)
        self.count += 1
        if self.count == 30:
            self.conn.commit()
            self.count = 0
            time.sleep(20)
