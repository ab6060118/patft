import scrapy
import re
from ..db import DB

class Patft(scrapy.Spider):
    name = "patft"
    total = 0
    DB = None

    def start_requests(self):
        self.DB = DB()
        urls = ['http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=taiwan&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_total)

    def get_total(self, response):
        self.total = response.xpath('/html/body/i/strong[3]/text()').extract_first()
        self.total = 3
        for i in range(1, int(self.total) + 1):
            url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=' + str(i) + '&f=G&l=50&co1=AND&d=PTXT&s1=taiwan&OS=taiwan&RS=taiwan'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if not response.xpath('//b[text()="Related U.S. Patent Documents"]').extract_first():
            related_us = []
        else:
            related_us = []
            docs = response.xpath('//b[text()="Related U.S. Patent Documents"]/../following-sibling::table[1]//tr')
            for i in range(2, len(docs) - 1):
                related_us.append({
                    'Application Number': docs[i].css('td:nth-child(2)::text').extract_first() or 'None',
                    'Filing Date': docs[i].css('td:nth-child(3)::text').extract_first() or 'None',
                    #  'Patent Number': docs[i].css('td:nth-child(4)::text').extract_first() or 'None',
                    #  'Issue Date': docs[i].css('td:nth-child(5)::text').extract_first() or 'None',
                    })

        if not response.xpath('//b[text()="References Cited  "]'):
            reference = "None"
        else:
            reference = {}

            if not response.xpath('//b[text()="U.S. Patent Documents"]'):
                reference["U.S. Patent Documents"] = []
            else:
                reference["U.S. Patent Documents"] = []
                docs = response.xpath('//b[text()="U.S. Patent Documents"]/../following-sibling::table[1]//tr')
                for i in range(1, len(docs) - 1):
                    reference["U.S. Patent Documents"].append({
                        'first': docs[i].css('td:nth-child(1) a::text').extract_first() or 'None',
                        'second': docs[i].css('td:nth-child(2)::text').extract_first().replace('\n', '') or 'None',
                        'third': docs[i].css('td:nth-child(3)::text').extract_first().replace('\n', '') or 'None',
                        })

            if not response.xpath('//b[text()="Foreign Patent Documents"]'):
                reference["Foreign Patent Documents"] = []
            else:
                reference["Foreign Patent Documents"] = []
                docs = response.xpath('//b[text()="Foreign Patent Documents"]/../following-sibling::table[1]//tr')
                for i in range(1, len(docs) - 1):
                    reference["Foreign Patent Documents"].append({
                        'first': docs[i].css('td:nth-child(2)::text').extract_first() or 'None',
                        'second': docs[i].css('td:nth-child(4)::text').extract_first().replace('\n', '') or 'None',
                        'third': docs[i].css('td:nth-child(6)::text').extract_first().replace('\n', '') or 'None',
                        })
            
            if not response.xpath('//b[text()="Other References"]'):
                reference["Other References"] = []
            else:
                reference["Other References"] = []
                docs = response.xpath('//b[text()="Other References"]/../following-sibling::tr/td/align').extract_first()
                docs = docs.replace('\n', '')
                reference['Other References'] = re.sub(r'(<[/]*align>)|(<a.*/a>)|(<[/]*b>)|(<[/]*i>)', '', docs).split('<br>')
                del reference['Other References'][0]
            
        Current_US_Class =  response.xpath('//b[text()="Current International Class: "]/../following-sibling::td/text()') or 'None'
        if Current_US_Class != 'None':
            Current_US_Class = Current_US_Class.extract_first().replace('&nbsp', ' ')
        yield self.DB.write({
                'United States Patent': response.xpath('//b[text()="United States Patent "]/../following-sibling::td/b/text()').extract_first(),
                'Date': response.xpath('//table[2]//tr[2]/td[2]/b/text()').extract_first().strip(),
                'Current U.S. Class': response.xpath('//b[text()="Current U.S. Class:"]/../following-sibling::td/b/text()').extract_first() + response.xpath('//b[text()="Current U.S. Class:"]/../following-sibling::td/text()').extract_first(),
                'Current International Class': Current_US_Class,
                'Related U.S. Patent Documents': related_us,
                'References Cited': reference,
                })
