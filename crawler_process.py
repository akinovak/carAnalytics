from scrapers.car_scrapers.polovni import PolovniScrap
from scrapy.crawler import CrawlerProcess
import sys

scrapers = [PolovniScrap]


def find_scraper(scraper_name, scrapers):
    for scraper in scrapers:
        if scraper.name == scraper_name:
            return scraper


print('Crawling started')
process = CrawlerProcess()
process.crawl(find_scraper(sys.argv[1], scrapers))
process.start()
print('Crawling finished')


