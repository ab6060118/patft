# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class PatftPipeline(object):
    def process_item(self, item, spider):
        #  print(item)

        return item

class InsertPipeLine(object):
    db = None

    def open_spider(self, spider):
        self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="example")
        cursor = self.db.cursor()
        cursor.execute("DROP DATABASE patft")
        cursor.execute("CREATE DATABASE patft")
        cursor.execute("USE patft")

        cursor.execute("CREATE TABLE post_v1 (United_States_Patent varchar(20), Date varchar(255), abstract longtext, claim longtext, current_international_class text, current_us_class varchar(255), description longtext, title text)")

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        command = 'INSERT INTO post_v1 (United_States_Patent, Date, abstract, claim, current_international_class, current_us_class, description, title) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(command, (
            item['UnitedStatesPatent'],
            item['date'],
            item['abstract'],
            item['claim'],
            item['current_international_class'],
            item['current_us_class'],
            item['description'],
            item['title']
        ))
        self.db.commit()
        #return item
