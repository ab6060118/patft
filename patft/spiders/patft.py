import scrapy
import re

from ..items import PatftItem
from scrapy.http import FormRequest

class Patft(scrapy.Spider):
    name = "patft"
    currentPage = 0
    maxPage = 1
    start_urls=['http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=taiwan+AND+ISD%2F1-1-2015-%3E12-31-2020%0D%0A&d=PTXT']

    def parse(self, response):
        if self.currentPage < self.maxPage:
            self.currentPage = self.currentPage + 1
            for href in response.xpath('//body/table//tr/td[2]/a/@href'):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, self.parsePost)
            next_page = response.xpath('//a/img[@src="/netaicon/PTO/nextlist.gif"]/../@href').extract_first()
            if next_page:
                print(next_page)
                yield scrapy.Request('http://patft.uspto.gov' + next_page, self.parse)
        else:
            print('done')

    def parsePost(self, response):
        item = PatftItem()

        if response.xpath('//b[descendant-or-self::*[text()="Claims"]]'):
            claims = response.xpath('//text()[preceding-sibling::*[descendant-or-self::*[text()="Claims"]] and following-sibling::center[preceding-sibling::center[1][descendant-or-self::*[text()="Claims"]]]]')
            claim = ' '.join(map(lambda e: ' '.join(e.get().replace('\n', '').split()), claims))
            item['claim'] = claim

        if response.xpath('//b[descendant-or-self::*[text()="Description"]]'):
            dess = response.xpath('//text()[preceding-sibling::*[descendant-or-self::*[text()="Description"]] and following-sibling::center[preceding-sibling::center[1][descendant-or-self::*[text()="Description"]]]]')
            des = ' '.join(map(lambda e: ' '.join(e.get().replace('\n', '').split()), dess))
            item['description'] = des
            print(des)

        if response.xpath('//b[text()="Abstract"]'):
            item['abstract'] = ' '.join(response.xpath('//b[text()="Abstract"]/../following-sibling::p[1]/text()').extract_first().replace('\n', '').split())

        item['UnitedStatesPatent'] = response.xpath('//b[text()="United States Patent "]/../following-sibling::td/b/text()').extract_first()
        item['date'] = response.xpath('//table[2]//tr[2]/td[2]/b/text()').extract_first().replace('\n', '').strip()
        item['title'] = ' '.join(response.xpath('/html/body/font/text()').extract_first().replace('\n', '').split())
        item['description'] = ' '.join(response.xpath('/html/body/font/text()').extract_first().replace('\n', '').split())
        return item
