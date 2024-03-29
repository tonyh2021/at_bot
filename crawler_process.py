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
    cars = project_settings["CARS"]
    for car in cars:
        project_settings["MAKE"] = car["make"]
        project_settings["MODEL"] = car["model"]
        project_settings["YEAR"] = car["year"]
        process = CrawlerProcess(project_settings)
        process.crawl(ATSpider)
    process.start()


def main():
    crawl_process()


if __name__ == "__main__":
    main()
