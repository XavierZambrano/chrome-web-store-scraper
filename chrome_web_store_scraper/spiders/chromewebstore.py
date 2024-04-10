import scrapy
from scrapy.spiders import SitemapSpider


class ChromeWebStoreSpider(SitemapSpider):
    name = "chromewebstore"
    allowed_domains = ["chromewebstore.google.com"]
    sitemap_urls = ['https://chromewebstore.google.com/sitemap']
    sitemap_rules = [
        ("/detail/", "parse"),
    ]

    def parse(self, response):
        pass
