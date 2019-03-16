# -*- coding: utf-8 -*-
import scrapy
from items import FindlawItem


class LawSpiderSpider(scrapy.Spider):
    name = "law_spider"
    allowed_domains = ["www.110.com"]
    start_urls = []
    for j in range(1, 70):
        for i in range(1,101):
            # p - page, s - answered, c -category(0: all, 1-70:category), r - unknown
            url = 'http://www.110.com/ask/browse-p%ds2c%dr0.html' % (i, j)
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
        content_list1 = response.xpath("//div[@class='wenz']//h1/text()").extract()
        content1 = "".join(content_list1)
        content_list1 = response.xpath("//div[@class='xwz']/text()").extract()
        content1 += "|||"
        content1 += "".join(content_list1)
        lawitem['question'] = content1
        content_list = response.xpath("/html/body/div[@class='main']/div[@class='left']/div[@class='leftbox02 bjing1']/div[@class='zjright']/div[@class='zjdanr']/text()").extract()
        content = "".join(content_list)
        lawitem['best_answer'] = content
        content_list = response.xpath("/html/body/div[@class='main']/div[@class='left']/div[@class='leftbox02 bjing1']/div[@class='zjdaz']/div[@class='zjda']/ul/li[2]/a/@href").extract()
        content = "".join(content_list)
        lawitem['best_answer_lawyer'] = content
        ls = response.xpath("/html/body/div[@class='main']/div[@class='left']/div[@class='leftbox02 bjing2']/div[@class='zjdaz']/div[@class='zjda']")
        length = len(ls)
        lawitem['other_answer_num'] = length
        content_ls = []
        for i in range(length):
            idx = (i + 1) * 4
            content_list = response.xpath("/html/body/div[@class='main']/div[@class='left']/div[@class='leftbox02 bjing2']/div[%d]/div[2]/text()" % idx).extract()
            tmp = "".join(content_list)
            content_ls.append(tmp)
        content = "|||".join(content_ls)
        lawitem['other_answer'] = content
        content_list = response.xpath("/html/body/div[@class='main']/div[@class='left']/div[@class='leftbox02 bjing2']/div[@class='zjdaz']/div[@class='zjda']/ul/li[2]/a/@href").extract()
        content = "|||".join(content_list)
        lawitem['other_answer_lawyer'] = content
        content_list = response.xpath("/html/body/div[@class='showpath']/span[@class='lshowpath']/a/text()").extract()
        content = "|||".join(content_list)
        lawitem['category'] = content
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
