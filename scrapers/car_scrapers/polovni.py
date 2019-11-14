import scrapy, json, re, math, codecs, pymongo, datetime, time, sys, random
import time, requests
from contorllers.scraper_contorler.car_controller.car_contoroller import CarContorller
from contorllers.db_controllers.storage_controller import StorageController
from adapters.mongo_adapter import MongoAdapter
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from conf import ctx


class PolovniScrap(scrapy.Spider):
    name = 'polovni_scrap'
    allowed_domains = ['polovniautomobili.com']
    start_urls = [
        'https://www.polovniautomobili.com/auto-oglasi/pretraga?page=1&sort=sort=renewDate_desc&city_distance=0&showOldNew=all&without_price=1']
    cars = []
    mongoAdp = MongoAdapter('mongodb://localhost:27017/', 'cardb')
    storageCtl = StorageController(mongoAdp)
    controller = CarContorller(storageCtl)

    def parse(self, response):
        arr_urls = []
        tmpStr = response.css('div.js-hide-on-filter small::text').get()
        numE = int(re.search('Prikazano od 1 do 25 oglasa od ukupno ([0-9]*)', tmpStr).group(1))
        print("OGLASA: " + str(numE))
        r = random.randint(1000, 100000)
        numPages = int(math.ceil(numE / 25))

        print("BROJ STRNICA: " + str(numPages))

        for i in range(numPages):
            url = 'https://www.polovniautomobili.com/auto-oglasi/pretraga?page=' + str(
                i + 1) + '&sort=renewDate_desc&city_distance=0&showOldNew=all&without_price=1'
            arr_urls.append(url)
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_page,
                errback=self.errback_httpbin,
                dont_filter=True
            )

    def parse_page(self, response):
        carUrls = response.css(
            'article.single-classified:not([class*="uk-hidden"]):not([class*="paid-0"]) h2 a::attr(href)').getall()

        carRenewal = response.xpath('//i[has-class("uk-icon-calendar")]/../text()').getall()

        renewal_dates = list(map(lambda x: x.split(':')[1].strip(), carRenewal))

        carUrls = list(map(lambda x: 'https://www.polovniautomobili.com' + x + '?show_date=true', carUrls))
        # print(carUrls)
        for (i, url) in enumerate(carUrls, start=0):
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_car,
                errback=self.errback_httpbin,
                dont_filter=True,
                meta={'renewal_date': renewal_dates[i]}
            )

    def parse_price(self, response):
        price = response.css('div.price-item::text').get()
        if price == '' or price is None:
            price = response.xpath('//div[has-class("price-item-discount position-relative")]').get()
            price = price.replace('\n', '').replace(' ', '').replace('\t', '')
            price = re.search(r'([0-9]*\.?[0-9]*)€', price).group(1)

        price = price.strip()
        if price == 'Po dogovoru' or price == 'Na upit':
            price = -1
        else:
            first = re.search('([0-9]*)\.?[0-9]*', price)
            second = re.search('[0-9]*\.([0-9]*)', price)
            if second is None:
                price = int(first.group(1))
            else:
                price = int(first.group(1)) * 1000 + int(second.group(1))

        return price

    def parse_car(self, response):
        renewal_date = response.meta.get('renewal_date')
        datetime_object = datetime.datetime.strptime(renewal_date, '%d.%m.%Y.')

        price = self.parse_price(response)
        exist = self.controller.check_object({'link': response.url, 'cena': price, 'datum_obnove' : datetime_object}, 'cars')
        if exist:
            return

        sec = response.css('section.classified-content div div::text').getall()
        # ctx.log.info(sec[-1])
        # ctx.log.info(response.css('section.classified-content').getall())
        arr = []
        for s in sec:
            w = s.strip()
            if w != '' and '\n' not in w and '\t' not in w:
                arr.append(w)

        keys = []
        vals = []
        for i in range(len(arr)):
            if i % 2 == 0:
                keys.append(arr[i])
            else:
                vals.append(arr[i])

        x = {}

        x['datum_obnove'] = datetime_object
        date_arr = sec[-1].split(':')
        date = date_arr[-1]
        date = date.strip()
        datetime_object = datetime.datetime.strptime(date, '%d.%m.%Y.')
        x['datum_postavke'] = datetime_object

        for i in range(len(keys)):
            if i < len(vals):

                if keys[i] == "Godište":
                    since = re.search('([0-9]*).', vals[i])
                    if since is not None:
                        x["Godiste"] = int(since.group(1))

                elif keys[i] == "Kubikaža":
                    cub = re.search('([0-9]*) cm', vals[i])
                    if cub is not None:
                        x["Kubikaza"] = int(cub.group(1))

                elif keys[i] == "Kilometraža":
                    km1 = re.search('([0-9]*)\.?[0-9]* km', vals[i])
                    km2 = re.search('[0-9]*\.([0-9]*) km', vals[i])
                    if km1 is not None:
                        if km2 is not None:
                            x["Kilometraza"] = int(km1.group(1)) * 1000 + int(km2.group(1))
                        else:
                            x["Kilometraza"] = int(km1.group(1))
                elif keys[i] == "Snaga motora":
                    power = re.search('([0-9]*)\/([0-9]*) \(kW\/KS\)', vals[i])
                    if (power != None):
                        x["Snaga_motora"] = int(power.group(2))

                else:
                    x[keys[i]] = vals[i]

        x['Postoji'] = True
        x['link'] = response.url
        x['logo'] = 'https://www.polovniautomobili.com/bundles/site/images/polovniautomobili-logo.svg'
        x['slika'] = response.css('ul[id="image-gallery"] li::attr(data-thumb)').get()

        ts = time.gmtime()
        ts = time.strftime("%Y-%m-%d", ts)
        x['cena'] = price
        x['istorija'] = [{ts: price}]
        print(x)
        x['mesto'] = response.css('aside.table-cell section.uk-grid div div div.uk-width-1-2::text').get().strip()

        if x['mesto'] == '':
            x['mesto'] = response.css('aside.table-cell section.uk-grid div div div div::text').get().strip()

        if x['mesto'] == '':
            x['mesto'] = response.css('aside.table-cell section.uk-grid div div::text').get().strip()

        if x['mesto'] == '':
            x['mesto'] = response.css(
                'aside.table-cell section.uk-grid div div.uk-margin-top-remove div.uk-width-1-2::text').get().strip()

        try:
            self.controller.insert_object(x, 'cars')
        except Exception as e:
            err = open("err.txt", "a+")
            err.write("Unexpected error:" + str(e))
            err.close()


    def errback_httpbin(self, failure):

        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            ctx.log.error('HttpError on %s', response.url)
            # self.wait_for_page(response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            ctx.log.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError):
            request = failure.request
            ctx.log.error('TimeoutError on %s', request.url)
            # self.wait_for_page(request.url)

    def wait_for_page(self, url):
        while True:
            r = requests.get(url)
            if r.status_code == 200:
                break
            time.sleep(60*10)