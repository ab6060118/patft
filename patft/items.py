# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PatftItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    claim = scrapy.Field()
    date = scrapy.Field()
    abstract = scrapy.Field()
    UnitedStatesPatent = scrapy.Field()
