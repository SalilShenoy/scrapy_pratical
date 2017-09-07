'''
Author: Salil Shenoy
'''

import scrapy
from scrapy.http import Request

'''
A class which uses scrapy scrapper api to retrieve the data from the given urls
'''
class InvestingSpider(scrapy.Spider):

    name = 'InvestingSpider'
    start_urls = ['https://www.investing.com/commodities/silver-historical-data']

    def parse(self, response):
        urls = ['https://www.investing.com/commodities/gold-historical-data',
                'https://www.investing.com/commodities/silver-historical-data']
        for i in range(len(urls)):
            yield Request(url=urls[i], callback=self.parse_item)

    def parse_item(self, response):

        text = response.xpath('//title/text()').extract()[0]
        if 'Gold' in text:
            com = 'gold'
        else:
            com = 'silver'
        rows = response.xpath('//table[(@id = "curr_table")]/tbody/tr')
        for row in rows:
            item = CommodityPrice()
            item['date'] = row.xpath('td[1]/text()').extract()
            item['current_price'] = row.xpath('td[2]/text()').extract()
            #item['open_price'] = row.xpath('td[3]/text()').extract()
            #item['high_price'] = row.xpath('td[4]/text()').extract()
            #item['low_price'] = row.xpath('td[5]/text()').extract()
            item['commodity'] = com
            yield item


'''
Item class to to store data retrieved from investing.com in memory for gold and silver
'''
class CommodityPrice(scrapy.Item):

    date = scrapy.Field()
    current_price = scrapy.Field()
    #open_price = scrapy.Field()
    #high_price = scrapy.Field()
    #low_price = scrapy.Field()
    commodity = scrapy.Field()

'''
Usage:
    scrapy runspider scrapper.py -o investing_data.csv
    
For sake of the exercise the file created by running this file is investing_data.csv.
It has 3 columns, 
    1. Date 
    2. Price
    3. Commodity

The name of the csv is used in DataAnalysis file as well so if needs to be the same or if 
we change it, it needs to be changed in both the files.
'''