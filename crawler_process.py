# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from at_bot.spiders.at import ATSpider
from scrapy.utils.project import get_project_settings
import logging
import os
import sys
import shutil

project_settings = get_project_settings()


def crawl_process():
    # creat CrawlerProcess project
    process = CrawlerProcess(project_settings)
    process.crawl(ATSpider)
    process.start()

def main():
    crawl_process()


if __name__ == "__main__":
    main()
