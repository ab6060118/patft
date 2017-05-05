# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PatftItem(scrapy.Item):
    date = scrapy.Field()
    UnitedStatesPatent = scrapy.Field()
    CurrentUSClass = scrapy.Field()
    CurrentInternationalClass = scrapy.Field()
    RelatedUSPatentDocuments = scrapy.Field()
    USPatentDocuments = scrapy.Field()
    ForeignPatentDocuments = scrapy.Field()
    OtherReferences = scrapy.Field()
