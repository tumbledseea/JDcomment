# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pandas as pd
#############################
class JdPipeline:
    def open_spider(self, spider):
        if not os.path.exists('dataset'):
            os.mkdir('dataset')
        if not os.path.exists('dataset/items.csv'):
            #item['nickname'], item['content'], item['score'],item['time']
            jd_goold = pd.DataFrame(columns=['nickname', 'content', 'score', 'creationTime', 'location'])
            jd_goold.to_csv('dataset/jd_goods.csv', index=False)

    def process_item(self, item, spider):
        if spider.name == 'JDSpiders':
            # 将item转换为JdGoodsItemModel，然后保存到数据库
            row = pd.DataFrame({'nickname': item['nickname'], 'content': item['content'], 'score': item['score'],
                                'creationTime': item['creationTime'], 'location': item['location']}, index=[0])
            row.to_csv('dataset/jd_goods.csv', index=False, encoding='utf-8', mode='a', header=False)

        return item