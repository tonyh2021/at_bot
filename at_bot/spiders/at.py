# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from at_bot.items import ATBotItem
from urllib import parse
import logging
import json

class ATSpider(Spider):
    name = "Auto Trader"
    page = 1
    base_url = ""
    headers = {}

    def base_url(self):
        self.headers = {"authorization": self.settings["AUTH_TOKEN"]}
        return "https://www.autotrader.ca/"


    def start_requests(self):
        self.base_url = self.base_url()
        url = self.base_url + '/cars/acura/mdx/on/mississauga/?rcp=100&rcs=0&srt=35&yRng=2020%2C2022&prx=100&prv=Ontario&loc=L5B%200J8&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch'
        logging.info("Start Request: " + url)
        yield Request(url, callback=self.parse_page, headers=self.headers)

    def parse_page(self, response):
        print(response.text)