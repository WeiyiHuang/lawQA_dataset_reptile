# -*- coding: utf-8 -*-

import scrapy

class FindlawItem(scrapy.Item):
    question = scrapy.Field()
    answer = scrapy.Field()
