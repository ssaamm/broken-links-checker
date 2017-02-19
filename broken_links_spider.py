from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
import config


class BrokenItem(Item):
    url = Field()
    referer = Field()
    status = Field()


class BrokenLinksSpider(CrawlSpider):
    name = config.name
    allowed_domains = config.allowed_domains
    start_urls = config.start_urls
    handle_httpstatus_list = [404]
    rules = (Rule(LinkExtractor(), callback='parse_item', follow=True),)

    def parse_item(self, response):
        if response.status != 200:
            item = BrokenItem()
            item['url'] = response.url
            item['referer'] = response.request.headers.get('Referer')
            item['status'] = response.status

            return item
