import scrapy


class RecSysSpider(scrapy.Spider):
    name = 'recsys-spider'

    def start_requests(self):
        self.abstract_index = 0

        if not hasattr(self, 'yy'):
            self.yy = '17'
        elif self.yy == '14':
            self.abstract_index = 2
        elif self.yy not in ['14', '15', '16', '17']:
            raise ValueError('Invalid year: ' + self.yy)

        url = 'https://recsys.acm.org/recsys{}/accepted-contributions/'.format(self.yy)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for elem in response.css('ul.accordion li'):
            yield {'abstract': elem.css('div p ::text').extract()[self.abstract_index].strip()}
