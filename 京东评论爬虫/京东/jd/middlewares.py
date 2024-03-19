# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

import requests
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
from webdriver_manager.chrome import ChromeDriverManager
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium import webdriver
from scrapy.http import HtmlResponse


class JdSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JdDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if spider.name == 'JDSpiders':
            driver = self.get_driver()
            driver.get(request.url)
            driver.implicitly_wait(10)  # TODO 如果你的网页加载很慢，可以适当调大这个时间
            # 京东-欢迎登录
            if driver.title == '京东-欢迎登录':
                input('请在浏览器中登录京东账号，完成后按回车键继续')
                driver.get(request.url)
                driver.implicitly_wait(10)
            # 将页面滚动条拖到底部，因加载原因，需要拖动多次,以确保所有商品都加载出来
            for i in range(1, 10):
                js = "document.documentElement.scrollTop=%d" % (i * 1000)
                driver.execute_script(js)
                time.sleep(2)
            return HtmlResponse(url=driver.current_url, body=driver.page_source, encoding='utf-8', request=request)
        else:
            driver = self.get_driver()
            driver.get(request.url)
            driver.implicitly_wait(10)  # TODO 如果你的网页加载很慢，可以适当调大这个时间
            if driver.title == '京东-欢迎登录':
                input('请在浏览器中登录京东账号，完成后按回车键继续')
                driver.get(request.url)
                driver.implicitly_wait(10)
            return HtmlResponse(url=driver.current_url, body=driver.page_source, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    webdriver = None
    def get_driver(self):
        if self.webdriver is None:
            options = webdriver.EdgeOptions()
            options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            # 设置浏览器驱动程序路径
            driver = webdriver.Edge(options=options)
            self.webdriver = driver
        return self.webdriver
