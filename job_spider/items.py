# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobid = scrapy.Field()
    jobname = scrapy.Field()
    coname = scrapy.Field()
    issuedate = scrapy.Field()
    degree = scrapy.Field()
    cityname = scrapy.Field()
    funtypename = scrapy.Field()
    workyear= scrapy.Field()
    providesalary = scrapy.Field()
    jobinfo = scrapy.Field()
    url = scrapy.Field()
    collect_date = scrapy.Field()
