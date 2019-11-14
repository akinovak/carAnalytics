import scrapy
import pymongo
import time, datetime

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from contorllers.scraper_contorler.sold_controller.sold_controller import sold_ctl
from conf import ctx


class SoldSpider(scrapy.Spider):
    name = "sold_spider"
    my_client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = my_client['cardb']
    collection = 'cars'
    # start_urls = ['https://www.polovniautomobili.com/auto-oglasi/14680618/bmw-x3-20d']
    # start_urls_healty = ['https://www.polovniautomobili.com/auto-oglasi/15336995/nissan-x-trail']

    def start_requests(self):
        for document in self.db[self.collection].find():
            yield scrapy.Request(document['link'], callback=self.parse,
                                 errback=self.errback_httpbin,
                                 dont_filter=True,
                                 meta={'car': document})

    def parse(self, response):
        if not isinstance(response.request.meta.get('redirect_urls'), type(None)):
            obj = response.meta.get('car')
            delta = datetime.datetime.now() - obj['datum']
            if delta.days < 30:
                sold_ctl.insert_to_sold(obj, self.collection, 'sold')
            else:
                sold_ctl.insert_to_sold(obj, self.collection, 'expired')

    def errback_httpbin(self, failure):
        if failure.check(HttpError):
            ctx.log.error('ERROR IN HTTP, DETERMINE HOW TO HANDLE')
        elif failure.check(DNSLookupError):
            request = failure.request
            ctx.log.error('ERROR IN DNS, WEB SITE ERROR')
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            ctx.log.warning(request)
            time.sleep(60*10)
