from scrapers.car_scrapers.polovni import PolovniScrap
from scrapy.crawler import CrawlerProcess
import sys, time
from scrapy.utils.project import get_project_settings

scrapers = [PolovniScrap]


def find_scraper(scraper_name, scrapers):
    for scraper in scrapers:
        if scraper.name == scraper_name:
            return scraper


process = CrawlerProcess()
process.crawl(find_scraper(sys.argv[1], scrapers))
process.start()
print('Crawling finished')


