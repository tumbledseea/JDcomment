import scrapy
from jd.items import JdGoodsCommitItem
import json
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlencode
class JDSpiders(scrapy.Spider):
    name = 'JDSpiders'
    allowed_domains = ['www.jd.com']
    url_head = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1710760204048&loginType=3&uuid=181111935.1006305175.1710410734.1710746212.1710759853.17&productId=100009440877&score=0&sortType=5'
    url_middle = '&page='
    url_end = '&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='

    def start_requests(self):
        params = {
            'appid': 'item-v3',
            'functionId': 'pc_club_productPageComments',
            'client': 'pc',
            'clientVersion': '1.0.0',
            't': '1710760204048',
            'loginType': '3',
            'uuid': '181111935.1006305175.1710410734.1710746212.1710759853.17',
            'productId': '100009440877',
            'score': '0',
            'sortType': '5',
            'page': '0',
            'pageSize': '10',
            'isShadowSku': '0', 
            'fold': '1',
            'bbtf': '',
            'shield': '',
        }
        for i in range(0, 2):
            url=self.url_head + self.url_middle + str(i)+urlencode(params) +self.url_end
            print("当前页面：", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_string = response.text
        soup = BeautifulSoup(json_string, 'html.parser')
        pattern = re.compile(r'{"jw.*?}')  # 使用正则表达式匹配以 {"jw 开头的数据
        json_string = soup.find(text=pattern)
        data = json.loads(json_string)
        comments = data['comments']
        for i in range(len(comments)):
            item = JdGoodsCommitItem()
            jd_nickname = comments[i]['nickname']
            jd_content = comments[i]['content']
            jd_score = comments[i]['score']
            jd_time = comments[i]['creationTime']
            jd_location = comments[i]['location']
            print("nickname",jd_nickname)
            print("location",jd_location)
            print("creationTime",jd_time)
            # 保存提取的数据到文件
            item["nickname"] = jd_nickname
            item["content"] = jd_content
            item["score"] = jd_score
            item["creationTime"] = jd_time
            item["location"] = jd_location
            yield item