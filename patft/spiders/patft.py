import scrapy
import re

from ..items import PatftItem
from scrapy.http import FormRequest

class Patft(scrapy.Spider):
    name = "patft"
    currentPage = 0
    maxPage = 100
    start_urls=['http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=taiwan&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT']

    def parse(self, response):
        if self.currentPage < self.maxPage:
            self.currentPage = self.currentPage + 1
            for href in response.xpath('//body/table//tr/td[2]/a/@href'):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, self.parsePost)
            if response.xpath('//input[contains(@name, "NextList")]'):
                print(response.url)
                yield FormRequest.from_response(response, formdata = { response.xpath('//input[contains(@name, "NextList")]/@name').extract_first() : response.xpath('//input[contains(@name, "NextList")]/@value').extract_first() }, formname = 'srchForm', callback=self.parse)
        else:
            print('done')

    def parsePost(self, response):
        relatedUS = []
        USPatentDocs = []
        foreignPatentDocs = []
        otherRefs = []

        if response.xpath('//b[text()="Related U.S. Patent Documents"]'):
            docs = response.xpath('//b[text()="Related U.S. Patent Documents"]/../following-sibling::table[1]//tr')
            for i in range(2, len(docs) - 1):
                relatedUS.append({
                    'Application Number': docs[i].css('td:nth-child(2)::text').extract_first() or 'None',
                    'Filing Date': docs[i].css('td:nth-child(3)::text').extract_first() or 'None',
                    })

        if response.xpath('//b[text()="U.S. Patent Documents"]'):
                docs = response.xpath('//b[text()="U.S. Patent Documents"]/../following-sibling::table[1]//tr')
                for i in range(1, len(docs) - 1):
                    USPatentDocs.append({
                        'first': docs[i].css('td:nth-child(1) a::text').extract_first() or 'None',
                        'second': docs[i].css('td:nth-child(2)::text').extract_first().replace('\n', '') or 'None',
                        'third': docs[i].css('td:nth-child(3)::text').extract_first().replace('\n', '') or 'None',
                        })

        if response.xpath('//b[text()="Foreign Patent Documents"]'):
            docs = response.xpath('//b[text()="Foreign Patent Documents"]/../following-sibling::table[1]//tr')
            for i in range(1, len(docs) - 1):
                foreignPatentDocs.append({
                    'first': docs[i].css('td:nth-child(2)::text').extract_first() or 'None',
                    'second': docs[i].css('td:nth-child(4)::text').extract_first().replace('\n', '') or 'None',
                    'third': docs[i].css('td:nth-child(6)::text').extract_first().replace('\n', '') or 'None',
                    })

        if response.xpath('//b[text()="Other References"]'):
            docs = response.xpath('//b[text()="Other References"]/../following-sibling::tr/td/align').extract_first()
            docs = docs.replace('\n', '')
            otherRefs = re.sub(r'(<[/]*align>)|(<a.*/a>)|(<[/]*b>)|(<[/]*i>)', '', docs).split('<br>')
            del otherRefs[0]

        item = PatftItem()
        item['UnitedStatesPatent'] = response.xpath('//b[text()="United States Patent "]/../following-sibling::td/b/text()').extract_first()
        item['CurrentUSClass'] = response.xpath('//b[text()="Current U.S. Class:"]/../following-sibling::td/b/text()').extract_first() + response.xpath('//b[text()="Current U.S. Class:"]/../following-sibling::td/text()').extract_first()
        item['CurrentInternationalClass'] = response.xpath('//b[text()="Current International Class: "]/../following-sibling::td/text()').extract_first()
        item['date'] = response.xpath('//table[2]//tr[2]/td[2]/b/text()').extract_first()
        item['RelatedUSPatentDocuments'] = relatedUS
        item['USPatentDocuments'] = USPatentDocs
        item['ForeignPatentDocuments'] = foreignPatentDocs
        item['OtherReferences'] = otherRefs
        return item
