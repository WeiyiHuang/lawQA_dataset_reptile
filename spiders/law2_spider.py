# -*- coding: utf-8 -*-
import scrapy
from items import FindlawItem

class Law2SpiderSpider(scrapy.Spider):
    name = "law2_spider"
    allowed_domains = ["www.66law.cn"]
    start_urls = ['http://www.66law.cn/question/list_1_r3.aspx']

    def parse(self, response):
        for con in response.xpath("/html/body/div[4]/div[1]/div/div[2]/div//div/ul//li/p/a"):
            if con.xpath("@href").extract_first():
                url = "http://www.66law.cn" + str(con.xpath("@href").extract_first())
                yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.xpath("/html/body/div[4]/div[1]/div/div[2]/div/div[5]/div/a[last()]/@href").extract_first()
        if next_page:
            yield scrapy.Request("http://www.66law.cn" + str(next_page), callback=self.parse)

    def parse_page(self, response):
        lawitem = FindlawItem()
        content_list = response.xpath("/html/body/div[3]/div[3]/div[1]/div[2]/ul//li/p/text()").extract()
        content = "|||".join(content_list)
        lawitem['answer'] = content.strip().replace('\r\n', '').replace('\xa0', '').replace('\u3000', '').replace('\r','').replace('\n', '')
        content_list1 = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/p[1]/text()").extract()
        content1 = "".join(content_list1)
        lawitem['question'] = content1.strip().replace('\r\n', '').replace('\xa0', '').replace('\u3000', '').replace('\r', '').replace('\n', '')
        yield lawitem
