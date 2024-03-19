from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider(spider_name):
    execute(['scrapypro', 'crawl', spider_name])


def run_all_spiders(didntWorkSpider=None):
    if didntWorkSpider is None:
        didntWorkSpider = []
    setting = get_project_settings()
    process = CrawlerProcess(setting)

    # 不需要工作的爬虫
    didntWorkSpider = didntWorkSpider

    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider:
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()


if __name__ == '__main__':
    run_spider('JDSpiders')