# -*- coding: utf-8 -*-
import scrapy
from findlaw.items import FindlawItem


class Law4SpiderSpider(scrapy.Spider):
    name = "law4_spider"
    allowed_domains = ["lawtime.cn"]
    start_urls = ['http://www.lawtime.cn/ask/browse_t2.html']
    for i in range(7,19):
        for j in range(1,13):
            url = ['http://www.lawtime.cn/ask/browse_d20%02d%02d_t2.html' % (i,j)]
            start_url = ''.join(url)
            start_urls.append(start_url)

    def parse(self, response):
        for con in response.xpath("//ul[@class='list-main']//li//a"):
            if con.xpath("@href").extract_first():
                url = str(con.xpath("@href").extract_first())
                yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page:
            yield scrapy.Request("http://www.lawtime.cn" +next_page, callback=self.parse)

    def parse_page(self, response):
        lawitem = FindlawItem()
        content_list = response.xpath("//div[@class='consult-answer-detail-text']//text()").extract()
        content = "".join(content_list)
        lawitem['answer'] = content.strip().replace('\r\n','').replace('\xa0','').replace('\u3000','').replace('\r','').replace('\n','')
        content_list1 = response.xpath("//p[@class='consult-question-detail']//text()").extract()
        content1 = "".join(content_list1)
        lawitem['question'] = content1.strip().replace('\r\n','').replace('\xa0','').replace('\u3000','').replace('\r','').replace('\n','')
        # content_list = response.xpath("//div[@class='SC_txt']//h3[@class='vone_en']//text()").extract()
        # content = "".join(content_list)
        # for i_content in content:
        #     content_s = "".join(i_content.split())
        #     lawitem['answer'] = content_s
        # content1 = response.xpath("//p[@class='consult-question-detail']//text()").extract()
        # for i_content1 in content1:
        #     content1_s = "".join(i_content1.split())
        #     lawitem['question'] = content1_s
        yield lawitem

