from urllib.parse import urlparse
from unittest.mock import Mock

from scrapy import Spider
from scrapy.utils.test import get_crawler

from crawlera_fetch.middleware import CrawleraFetchMiddleware

from tests.data import SETTINGS


class MockDownloader:
    def _get_slot_key(self, request, spider):
        if "download_slot" in request.meta:
            return request.meta["download_slot"]
        return urlparse(request.url).hostname or ""


class MockEngine:
    def __init__(self):
        self.downloader = MockDownloader()


class FooSpider(Spider):
    name = "foo"

    def foo_callback(self, response):
        pass


foo_spider = FooSpider()


def get_test_middleware(settings=None):
    settings_dict = SETTINGS.copy()
    settings_dict.update(settings or {})

    foo_spider = FooSpider()
    foo_spider.crawler = get_crawler(FooSpider, settings_dict=settings_dict)
    foo_spider.crawler.engine = MockEngine()

    middleware = CrawleraFetchMiddleware.from_crawler(foo_spider.crawler)
    middleware.spider_opened(foo_spider)

    return middleware


mocked_time = Mock(return_value=1234567890.123)
