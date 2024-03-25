# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from at_bot.items import ATBotItem
import logging
import json

class ATSpider(Spider):
    name = "Auto Trader"
    page = 1
    base_url = ""
    headers = {}

    def base_url(self):
        return "https://www.autotrader.ca"


    def start_requests(self):
        self.base_url = self.base_url()
        make = self.settings.get('MAKE')
        model = self.settings.get('MODEL')
        year = self.settings.get('YEAR')
        url = self.base_url + f'/cars/{make}/{model}/on/mississauga/?rcp=100&rcs=0&srt=35&yRng={year}%2C{year}&prx=100&prv=Ontario&loc=L5B%200J8&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch'
        logging.info("Start Request: " + url)
        yield Request(url, callback=self.parse_page, headers=self.headers)

    def parse_page(self, response):
        data = response.selector.xpath('//script[@type="application/ld+json"]/text()').get().strip()
        json_data = json.loads(data)
        for x in json_data['offers']["offers"]:
            item_url = self.base_url + str(x["url"])
            logging.info("Start Request: " + item_url)
            yield response.follow(item_url, callback=self.parse_item, headers=self.headers)

    def parse_item(self, response):
        scripts = response.selector.xpath('//script[@type="text/javascript"]/text()').getall()
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
                            return self.build_item(json_data)
                            
        
    def build_item(self, json_data):
        item = ATBotItem()

        item['adId'] = json_data['adBasicInfo']['adId']

        carfax = json_data['carfax']
        item['carfax'] = carfax.get('carProofReportUrl', '')

        hero = json_data.get('hero')
        item['make'] = hero.get('make')
        item['model'] = hero.get('model')
        item['year'] = hero.get('year')
        item['trim'] = hero.get('trim', '')
        item['price'] = hero.get('price')
        item['location'] = hero.get('location')
        item['mileage'] = hero.get('mileage')
        item['priceAnalysis'] = hero.get('priceAnalysis', '')
        item['vehicleAge'] = hero.get('vehicleAge')
        item['priceAnalysisDescription'] = hero.get('priceAnalysisDescription')
        item['status'] = hero.get('status')
        item['stockNumber'] = hero.get('stockNumber', '')

        gallery_items = json_data['gallery']['items']
        gallery = ''
        for x in gallery_items:
            gallery = gallery + str(x['photoViewerUrl']) + ', '
        if len(gallery) > 0: 
            gallery = gallery[:-2]
        item['gallery'] = gallery

        yield item