# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class PatftPipeline(object):
    def process_item(self, item, spider):
        item['date'] = item['date'].strip()

        if item['CurrentInternationalClass']:
            item['CurrentInternationalClass'].replace('&nbsp', ' ')
        else:
            item['CurrentInternationalClass'] = "None"

        return item

class InsertPipeLine(object):
    db = None

    def open_spider(self, spider):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="user")
        cursor = self.db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS patft")
        cursor.execute("USE patft")

        cursor.execute("DROP TABLE IF EXISTS post")
        cursor.execute("CREATE TABLE IF NOT EXISTS post (United_States_Patent varchar(20), Date varchar(30), Current_US_Class text, Current_International_Class text)")

        cursor.execute("DROP TABLE IF EXISTS Related_US_Patent_Documents")
        cursor.execute("CREATE TABLE IF NOT EXISTS Related_US_Patent_Documents (United_States_Patent varchar(20), Application_Number varchar(30), Filing_Date varchar(30))")

        cursor.execute("DROP TABLE IF EXISTS US_Patent_Documents")
        cursor.execute("CREATE TABLE IF NOT EXISTS US_Patent_Documents (United_States_Patent varchar(20), first varchar(30), second varchar(30), third varchar(30))")

        cursor.execute("DROP TABLE IF EXISTS Foreign_Patent_Documents")
        cursor.execute("CREATE TABLE IF NOT EXISTS Foreign_Patent_Documents (United_States_Patent varchar(20), first varchar(30), second varchar(30), third varchar(30))")

        cursor.execute("DROP TABLE IF EXISTS Other_References")
        cursor.execute("CREATE TABLE IF NOT EXISTS Other_References (United_States_Patent varchar(20), data text)")

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO post (United_States_Patent, Date, Current_US_Class, Current_International_Class) VALUES ("' + item['UnitedStatesPatent'] + '", "' + item['date'] + '", "' + item['CurrentUSClass'] + '", "' + item['CurrentInternationalClass'] + '")')
        self.db.commit()

        if item['RelatedUSPatentDocuments']:
            data = ''
            for item1 in item['RelatedUSPatentDocuments']:
                data = ''.join([data, '("' + item['UnitedStatesPatent'] + '", "' + item1['Application Number'] + '", "' + item1['Filing Date'] + '")'])
            data = data.replace(')(', '), (')

            cursor.execute('INSERT INTO Related_US_Patent_Documents (United_States_Patent, Application_Number, Filing_Date) VALUES ' + data)
            self.db.commit()

        if item['USPatentDocuments']:
            data = ''
            for item1 in item['USPatentDocuments']:
                data = ''.join([data, '("' + item['UnitedStatesPatent'] + '", "' + item1['first'] + '", "' + item1['second'] + '", "' + item1['third'] + '")'])
            data = data.replace(')(', '), (')

            cursor.execute('INSERT INTO US_Patent_Documents (United_States_Patent, first, second, third) VALUES ' + data)
            self.db.commit()

        if item['ForeignPatentDocuments']:
            data = ''
            for item1 in item['ForeignPatentDocuments']:
                data = ''.join([data, '("' + item['UnitedStatesPatent'] + '", "' + item1['first'] + '", "' + item1['second'] + '", "' + item1['third'] + '")'])
            data = data.replace(')(', '), (')

            cursor.execute('INSERT INTO Foreign_Patent_Documents (United_States_Patent, first, second, third) VALUES ' + data)
            self.db.commit()

        if item['OtherReferences']:
            data = ''
            for item1 in item['OtherReferences']:
                data = ''.join([data, '("' + item['UnitedStatesPatent'] + '", "' + MySQLdb.escape_string(item1) + '")'])
            data = data.replace(')(', '), (')

            cursor.execute('INSERT INTO Other_References (United_States_Patent, data) VALUES ' + data)
            self.db.commit()

        #return item
