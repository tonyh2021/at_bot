# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from at_bot.items import ATBotItem
import logging
import json
import random

class ATSpider(Spider):
    name = "Auto Trader"
    page = 1
    base_url = ""
    headers = {}
    item_url_count = 0
    item_count = 0

    def base_url(self):
        return "https://www.autotrader.ca"


    def start_requests(self):
        self.base_url = self.base_url()
        make = self.settings.get('MAKE')
        model = self.settings.get('MODEL')
        year = self.settings.get('YEAR')
        random_number = random.randint(1, 9)
        url = self.base_url + f'/cars/{make}/{model}/on/mississauga/?rcp=100&rcs=0&srt=35&yRng={year}%2C{year}&prx=100&prv=Ontario&loc=L5B%200J{random_number}&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch'
        logging.info("Start Request: " + url)
        yield Request(url, callback=self.parse_page, headers=self.headers)

    def parse_page(self, response):
        data = response.selector.xpath('//script[@type="application/ld+json"]/text()').get()
        if data is None:
            logging.info("End Request: " + response.text)
            return
        json_data = json.loads(data.strip())
        make = self.settings.get('MAKE')
        model = self.settings.get('MODEL')
        year = self.settings.get('YEAR')
        logging.info(f'{make}-{model}-{year} Offer Count: ' + str(json_data['offers']["offerCount"]))
        for x in json_data['offers']["offers"]:
            item_url = self.base_url + str(x["url"])
            logging.info("Start Request: " + item_url)
            yield response.follow(item_url, callback=self.parse_item, headers=self.headers)

    def parse_item(self, response):
        scripts = response.selector.xpath('//script[@type="text/javascript"]/text()').getall()
        found = False
        for s in scripts:
            if "ngVdpModel" in s:
                startIndex = s.index("window['ngVdpModel'] = ")
                if startIndex > 0:
                    s = s[startIndex:]
                    s = s.replace("window['ngVdpModel'] = ", "").strip()
                    endIndex = s.index("window['ngVdpGtm'] =")
                    if endIndex > 0:
                        s = s[:endIndex]
                        s = s.replace("window['ngVdpGtm'] =", "").strip()
                        if (s[-1] == ";"):
                            s = s[:-1]
                            json_data = json.loads(s)
                            self.item_count += 1
                            logging.info("Item Count: " + str(self.item_count))
                            found = True
                            yield self.build_item(json_data, response)
        if not found:
            logging.info("Item Not Found: " + response.text)
        
    def build_item(self, json_data, response):
        item = ATBotItem()

        item['adId'] = json_data['adBasicInfo']['adId']

        carfax = json_data['carfax']
        item['carfax'] = carfax.get('carProofReportUrl', '')

        hero = json_data.get('hero')
        item['trim'] = hero.get('trim', '')
        item['price'] = hero.get('price')
        item['location'] = hero.get('location')
        item['mileage'] = hero.get('mileage')
        item['stockNumber'] = hero.get('stockNumber', '')
        item['item_url'] = response.url

        item['conditions'] =  ', '.join(json_data.get('conditionAnalysis').get('options', []))

        if 'https://vhr.carfax.ca/?id=' in item['carfax']:
            carfax_id = item['carfax'].replace('https://vhr.carfax.ca/?id=', '')
            carfax_url = f'https://vhr.carfax.ca/Json/GetData?id={carfax_id}'
            logging.info("Start Request: " + carfax_url)
            return response.follow(carfax_url, callback=self.parse_carfax, headers=self.headers, meta={'item': item}, method='POST')
        else:
            return item

    def parse_carfax(self, response):
        item = response.meta["item"]
        carfax_info = json.loads(response.text)

        item['oneOwner'] = carfax_info.get('HighlightsViewModel').get('OneOwner', False)
        item['vin'] = carfax_info.get('VehicleDetailsViewModel').get('Vin', '')
        item['damaged'] = carfax_info.get('VehicleHistoryTilesViewModel').get('AccidentDamagesType', '0')
        item['serviceRecords'] = carfax_info.get('VehicleHistoryTilesViewModel').get('ServiceRecords', '0')
        item['openRecall'] = carfax_info.get('VehicleHistoryTilesViewModel').get('RecallCount', '0')
        item['stolen'] = carfax_info.get('VehicleHistoryTilesViewModel').get('Stolen', False)
        return item