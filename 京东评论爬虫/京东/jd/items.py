# Define here the models for your scraped items
#使用Scrapy框架定义了三个数据模型
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 商品评论
class JdGoodsCommitItem(scrapy.Item):
    shop_id = scrapy.Field()
    content = scrapy.Field()
    creationTime = scrapy.Field()
    nickname = scrapy.Field()
    score = scrapy.Field()
    location=scrapy.Field()