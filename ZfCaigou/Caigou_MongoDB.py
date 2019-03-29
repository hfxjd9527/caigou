# -*- coding: utf-8 -*-
# @AuThor  : frank_lee

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from scrapy.selector import Selector
import pymongo


class ZfCaigou():
    """
    """
    def __init__(self):
        self.url = 'http://www.zjzfcg.gov.cn/purchaseNotice/index.html?categoryId=3001'
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)  # 设置超时时间
        self.zoom = 1

        # 以下保存到MongoDB数据库，不想要可以删掉
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.db = self.client['zfcaigou']
        # MongoDB部分结束

    def get_info(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(5)
        i = 0
        while i < 3:  # 想抓多少页就写多少页，任性。也可以定义一个total_page，然后在这里用self.total_page调用
            time.sleep(2)
            data = self.driver.page_source
            response = Selector(text=data)  # 这里如果不使用"text=data",直接写data将会报错 'str' object has no attribute 'text'
            infodata = response.css(".items p")
            for infoline in infodata:
                city = infoline.css(".warning::text").extract()[0].replace("[", "").replace("·", "").strip()
                issuescate = infoline.css(".warning .limit::text").extract()[0]
                title = infoline.css("a .underline::text").extract()[0].replace("]", "").replace("[", "")
                publish_date = infoline.css(".time::text").extract()[0].replace("[", "").replace("]", "")

                # 为保存到MongoDB做的处理，不想保存可以删掉
                result = {
                    "city": city,
                    "issuescate": issuescate,
                    "title": title,
                    "publish_date": publish_date,
                }
                self.save_to_mongo(result)
                # 结束

            self.driver.find_element_by_css_selector(
                'div.paginationjs-pages > ul > li.paginationjs-next.J-paginationjs-next a').click()
            i += 1
            time.sleep(3)
        time.sleep(3)
        self.driver.close()

    def save_to_mongo(self, result):
        if self.db['caigou'].insert(result):
            print("保存成功啦，嘻嘻")


if __name__ == '__main__':
    z = ZfCaigou()
    z.get_info()
