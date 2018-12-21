# -*- coding: utf-8 -*-
import scrapy
from items import FindlawItem

class Law1SpiderSpider(scrapy.Spider):
    name = "law1_spider"
    allowed_domains = ["consult.fabao365.com"]
    start_urls = []
    for i in range(1, 100):
        url = ['http://consult.fabao365.com/top_3_%d.html' % (i)]
        start_url = ''.join(url)
        start_urls.append(start_url)

    def parse(self, response):
        for con in response.xpath("//div[@class='flcitem']/dl[@class='c1']/a[1]"):
            if con.xpath("@href").extract_first():
                url = "http://consult.fabao365.com" + str(con.xpath("@href").extract_first())
                yield scrapy.Request(url, callback=self.parse_page)

        # next_page = response.xpath("//a[@title='下一页']/@href").extract_first()
        # if next_page:
        #     yield scrapy.Request("http://consult.fabao365.com" + str(next_page), callback=self.parse)

    def parse_page(self, response):
        lawitem = FindlawItem()
        content_list = response.xpath("//div[@class='content']//text()").extract()
        content = "".join(content_list)
        lawitem['answer'] = content.strip().replace('\r\n', '').replace('\xa0', '').replace('\u3000', '').replace('\r','').replace('\n', '')
        content_list1 = response.xpath("//p[@style='text-indent:2em']//text()").extract()
        content1 = "".join(content_list1)
        lawitem['question'] = content1.strip().replace('\r\n', '').replace('\xa0', '').replace('\u3000', '').replace('\r', '').replace('\n', '')
        # content_list = response.xpath("//div[@class='SC_txt']//h3[@class='vone_en']//text()").extract()
        # content = "".join(content_list)
        # for i_content in content:
        #     content_s = "".join(i_content.split())
        #     lawitem['answer'] = content_s
        # content1 = response.xpath("//p[@class='consult-question-detail']//text()").extract()
        # for i_content1 in content1:
        #     content1_s = "".join(i_content1.split())
        #     lawitem['question'] = content1_s
        if lawitem['answer'] != '' and lawitem['question'] != '':
            yield lawitem
