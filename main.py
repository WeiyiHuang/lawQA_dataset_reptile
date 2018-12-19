# -*- coding: utf-8 -*-

from scrapy import cmdline

cmdline.execute('scrapy crawl law_spider -o law_data.csv'.split())
