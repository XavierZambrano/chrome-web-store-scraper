import scrapy
from scrapy.spiders import SitemapSpider
from dotenv import load_dotenv

from chrome_web_store_scraper.utils import script_to_data
from chrome_web_store_scraper.items import ChromeWebStoreItem


load_dotenv()


class ChromeWebStoreSpider(SitemapSpider):
    name = "chromewebstore"
    allowed_domains = ["chromewebstore.google.com"]
    sitemap_urls = ['https://chromewebstore.google.com/sitemap']
    sitemap_rules = [
        ("/detail/", "parse"),
    ]

    def parse(self, response):
        id = response.url.split('/')[-1]
        # name = response.xpath('//h1[@class="Pa2dE"]//text()').get()
        category = response.xpath('//a[@class="gqpEIe FjUAcd"]/text()').get()  #
        subcategory = response.xpath('//a[@class="gqpEIe bgp7Ye"]/text()').get()  #
        # website_owner = response.xpath('//a[@class="cJI8ee"]/@href').get()
        # created_by_the_website_owner = True if website_owner else False
        featured_raw = response.xpath('//span[@class="OmOMFc"]').getall()
        featured = True if featured_raw else False  #
        # rating_raw = response.xpath('//div[@class="B1UG8d or8rae"]/@title').get()
        # rating = int(rating_raw.split()[0])

        script_raw = response.xpath(f'''//script[contains(text(), 'data:[[\"{id}\"')]/text()''').get()
        data = {}
        data.update(script_to_data(script_raw))
        data['url'] = response.url
        data['category'] = category
        data['subcategory'] = subcategory
        data['featured'] = featured
        data['website_owner'] = response.xpath('//a[@class="cJI8ee"]/@href').get()
        developer_address_raw = response.xpath('//div[@class="C2WXF"]/text()').getall()
        developer_address = '\n'.join(developer_address_raw)
        data['developer']['address'] = developer_address
        data['developer']['website'] = response.xpath('//a[@class="XQ8Hh"]/@href').get()
        chrome_web_store_item = ChromeWebStoreItem(**data)

        # TODO reviews
        # https://chromewebstore.google.com/_/ChromeWebStoreConsumerFeUi/data/batchexecute
        # + query string parameters
        # + form data

        # TODO Add privacy data?
        # TODO Add related extensions data?
        yield chrome_web_store_item
