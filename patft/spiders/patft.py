import scrapy
import re

from ..items import PatftItem
from scrapy.http import FormRequest

class Patft(scrapy.Spider):
    name = "patft"
    currentPage = 0
    maxPage = 10000
    start_urls=['http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&co1=AND&d=PTXT&s1=%40PD%3E%3D20150101%3C%3D20201231&s2=TW.AACO.&Page=Next&OS=ISD/1-1-2015-%3E12-31-2020+AND+AACO/TW&RS=ISD/1-1-2015-%3E12-31-2020+AND+AACO/TW']

    def parse(self, response):
        if self.currentPage < self.maxPage:
            self.currentPage = self.currentPage + 1
            for href in response.xpath('//body/table//tr/td[2]/a/@href'):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, self.parsePost)
            next_page = response.xpath('//a/img[@src="/netaicon/PTO/nextlist.gif"]/../@href').extract_first()
            if next_page:
                yield scrapy.Request('http://patft.uspto.gov' + next_page, self.parse)
        else:
            print('done')

    def parsePost(self, response):
        item = PatftItem()

        if response.xpath('//b[descendant-or-self::*[text()="Claims"]]'):
            claims = response.xpath('//text()[preceding-sibling::*[descendant-or-self::*[text()="Claims"]] and following-sibling::center[preceding-sibling::center[1][descendant-or-self::*[text()="Claims"]]]]')
            claim = ' '.join(map(lambda e: ' '.join(e.get().replace('\n', '').split()), claims))
            item['claim'] = claim
        else:
            item['claim'] = ''

        if response.xpath('//b[descendant-or-self::*[text()="Description"]]'):
            dess = response.xpath('//text()[preceding-sibling::*[descendant-or-self::*[text()="Description"]] and following-sibling::center[preceding-sibling::center[1][descendant-or-self::*[text()="Description"]]]]')
            des = ' '.join(map(lambda e: ' '.join(e.get().replace('\n', '').split()), dess))
            item['description'] = des
        else:
            item['description'] = ''

        if response.xpath('//b[text()="Abstract"]'):
            item['abstract'] = ' '.join(response.xpath('//b[text()="Abstract"]/../following-sibling::p[1]/text()').extract_first().replace('\n', '').split())
        else:
            item['abstract'] = ''

        item['UnitedStatesPatent'] = response.xpath('//b[text()="United States Patent "]/../following-sibling::td/b/text()').extract_first()
        item['current_international_class'] = response.xpath('//b[text()="Current International Class: "]/../following-sibling::td/text()').extract_first().strip()
        item['current_us_class'] = response.xpath('//b[text()="Current U.S. Class:"]/../following-sibling::td/b/text()').extract_first() + response.xpath('//b[text()="Current U.S. Class:"]/../following-sibling::td/text()').extract_first()
        item['date'] = response.xpath('//table[2]//tr[2]/td[2]/b/text()').extract_first().replace('\n', '').strip()
        item['title'] = ' '.join(response.xpath('/html/body/font/text()').extract_first().replace('\n', '').split())

        return item
