from scrapy.spiders import SitemapSpider
from scrapy.http import Request
from scrapy.spiders.sitemap import iterloc
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
import os


class CustomSitemapSpider(SitemapSpider):
    """
    Add proxy
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = os.getenv('PROXY')
        if self.proxy is None:
            raise ValueError("PROXY environment variable is not set")

    def start_requests(self):
        for url in self.sitemap_urls:
            yield Request(url, self._parse_sitemap, meta={'proxy': self.proxy})

    def _parse_sitemap(self, response):
        if response.url.endswith("/robots.txt"):
            for url in sitemap_urls_from_robots(response.text, base_url=response.url):
                yield Request(url, callback=self._parse_sitemap, meta={'proxy': self.proxy})
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                self.logger.warning(
                    "Ignoring invalid sitemap: %(response)s",
                    {"response": response},
                    extra={"spider": self},
                )
                return

            s = Sitemap(body)
            it = self.sitemap_filter(s)

            if s.type == "sitemapindex":
                for loc in iterloc(it, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap, meta={'proxy': self.proxy})
            elif s.type == "urlset":
                for loc in iterloc(it, self.sitemap_alternate_links):
                    for r, c in self._cbs:
                        if r.search(loc):
                            yield Request(loc, callback=c, meta={'proxy': self.proxy})
                            break
