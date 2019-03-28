# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from caigou.items import CaigouItem
# from caigou.items import ZfcaigouItemLoad, CaigouItem


class ZfcaigouSpider(scrapy.Spider):
    name = 'zfcaigou'
    allowed_domains = ['www.zjzfcg.gov.cn']
    start_urls = ['http://www.zjzfcg.gov.cn/purchaseNotice/index.html?categoryId=3001']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,
                                args={'wait': 10}, endpoint='render.html')

    def parse(self, response):
        # print(response.body.decode("utf-8"))
        infodata = response.css(".items p")
        for infoline in infodata:
            caigouitem = CaigouItem()
            caigouitem['city'] = infoline.css(".warning::text").extract()[0].replace("[", "").replace("·", "").strip()
            caigouitem['issuescate'] = infoline.css(".warning .limit::text").extract()[0]
            caigouitem['title'] = infoline.css("a .underline::text").extract()[0].replace("]", "")
            caigouitem['publish_date'] = infoline.css(".time::text").extract()[0].replace("[", "").replace("]", "")
            yield caigouitem



