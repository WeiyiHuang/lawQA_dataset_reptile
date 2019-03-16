# -*- coding: utf-8 -*-

import scrapy

class FindlawItem(scrapy.Item):
    question = scrapy.Field()
    best_answer = scrapy.Field()
    best_answer_lawyer = scrapy.Field()
    other_answer_num = scrapy.Field()
    other_answer = scrapy.Field()
    other_answer_lawyer = scrapy.Field()
    category = scrapy.Field()
