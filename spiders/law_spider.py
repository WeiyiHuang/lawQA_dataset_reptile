# -*- coding: utf-8 -*-
import scrapy
from items import FindlawItem


class LawSpiderSpider(scrapy.Spider):
    name = "law_spider"
    allowed_domains = ["www.110.com"]
    start_urls = []
    for i in range(1,101):
        url = 'http://www.110.com/ask/browse-p%ds2c0r0.html' % (i)
        start_urls.append(url)


    def parse(self, response):
        for con in response.xpath("//div[@class='tit07']/span[1]/a[2]"):
            if con.xpath("@href").extract_first():
                url = "http://www.110.com"+str(con.xpath("@href").extract_first())
                yield scrapy.Request(url, callback=self.parse_page)

        # next_page = response.xpath("//div[@class='pages']//a[contains(text(),'下一页')]/@href").extract_first()
        # if next_page:
        #     yield scrapy.Request("http://www.110.com"+str(next_page),callback=self.parse)

    def parse_page(self, response):
        lawitem = FindlawItem()
        content_list = response.xpath("//div[@class='zjdanr']/text()").extract()
        content = "".join(content_list)
        lawitem['answer'] = content
        content_list1 = response.xpath("//div[@class='xwz']/text()").extract()
        content1 = "".join(content_list1)
        lawitem['question'] = content1
        yield lawitem


    # def parse(self, response):
    #     q_list = response.xpath("//div[@class='leftbox02']//div[@class='tit07']")
    #     for i_item in q_list:
    #         lawitem = FindlawItem()
    #         lawitem['question'] = i_item.xpath("./span[1]/a[2]/text()").extract_first()
    #         yield lawitem
    #
    #     next_link = response.xpath("/html/body/div[8]/div[1]/div[2]/div[53]/table/tbody/tr/td[14]/a[contains(text(),'下一页)]/@href").extract_first()
    #     if next_link:
    #         yield scrapy.Request('http://www.110.com'+next_link, callback=self.parse)
