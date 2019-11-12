from scrapers.car_scrapers.polovni import PolovniScrap
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import time


def infinite_crawl():
    process = CrawlerProcess()

    process.crawl(PolovniScrap)
    process.start()
    print('Crawling finished')


# scrapy_settings = get_project_settings()
# scrapy_settings.set('DUPEFILTER_CLASS', 'scrapy.dupefilters.BaseDupeFilter')

while True:
    infinite_crawl()
    time.sleep(10)



