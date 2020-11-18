# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#  import MySQLdb

class PatftPipeline(object):
    def process_item(self, item, spider):
        #  print(item)

        return item

class InsertPipeLine(object):
    db = None

    def open_spider(self, spider):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="example")
        cursor = self.db.cursor()
        cursor.execute("DROP DATABASE patft")
        cursor.execute("CREATE DATABASE patft")
        cursor.execute("USE patft")

        cursor.execute("CREATE TABLE post_v1 (United_States_Patent varchar(20), Date varchar(255), abstract text, claim text,description text)")

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO post_v1 (United_States_Patent, Date, abstract, claim, description) VALUES ("' + item['UnitedStatesPatent'] + '", "' + item['date'] + '", "' + item['abstract'] + '", "' + item['claim'] + '", "' + item['description'] + '")')
        self.db.commit()
        #return item
