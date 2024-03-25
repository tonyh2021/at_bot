# -*- coding: utf-8 -*-
from at_bot.items import ATBotItem
import logging
import json
import time

class ItemPipeline:
    def open_spider(self, spider):
        make = spider.settings.get('MAKE')
        model = spider.settings.get('MODEL')
        year = spider.settings.get('YEAR')
        date = time.strftime("%Y_%m_%d", time.localtime(time.time()))
        file_name = f'data/{make}_{model}_{year}_{date}.json'
        self.item_file = open(file_name, 'w')

    def close_spider(self, spider):
        self.item_file.close()

    def process_item(self, item, spider):
        if isinstance(item, ATBotItem):
            return self.handleItem(item, spider) 
        
    def handleItem(self, item, spider): # needed self added
        logging.info(f'handleItem: {item["adId"]}')
        self.item_file.write(json.dumps(dict(item), ensure_ascii=False) + "\n")
        return item