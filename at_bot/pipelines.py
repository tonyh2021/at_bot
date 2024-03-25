# -*- coding: utf-8 -*-
from at_bot.items import ATBotItem
import logging
import json

class ItemPipeline:
    def open_spider(self, spider):
        self.item_file = open('items.json', 'w')

    def close_spider(self, spider):
        self.item_file.close()

    def process_item(self, item, spider):
        if isinstance(item, ATBotItem):
            return self.handleItem(item, spider) 
        
    def handleItem(self, item, spider): # needed self added
        logging.info(f'handleItem: {item["adId"]}')
        self.item_file.write(json.dumps(dict(item), ensure_ascii=False) + "\n")
        return item