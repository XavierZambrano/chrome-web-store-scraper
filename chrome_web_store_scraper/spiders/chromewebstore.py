from scrapy.spiders import SitemapSpider

from chrome_web_store_scraper.utils import script_to_data
from chrome_web_store_scraper.items import ChromeWebStoreItem, ChromeWebStoreItemLoader
from chrome_web_store_scraper.errors import NotAvailableItem


class ChromeWebStoreSpider(SitemapSpider):
    name = "chromewebstore"
    allowed_domains = ["chromewebstore.google.com"]
    sitemap_urls = ['https://chromewebstore.google.com/sitemap']
    sitemap_rules = [
        ("/detail/", "parse"),
    ]

    def parse(self, response):
        if response.xpath('//div[@class="VuNdOd"]').get():
            self.crawler.stats.inc_value('item_skipped_count', 1, 0)
            self.crawler.stats.inc_value(f'item_skipped_reasons_count/{NotAvailableItem.__name__}', 1, 0)
            self.logger.info(f'{NotAvailableItem.__name__}: {response.url}')
            return

        l = ChromeWebStoreItemLoader(ChromeWebStoreItem(), selector=response)
        id = response.url.split('/')[-1]

        featured_container = response.xpath('//span[@class="OmOMFc"]').get()
        l.add_value('featured', True if featured_container else False)

        script_raw = response.xpath(f'''//script[contains(text(), 'data:[[\"{id}\"')]/text()''').get()
        data = {}
        data.update(script_to_data(script_raw))

        developer_address_raw = response.xpath('//div[@class="Fm8Cnb"]/text()').getall()
        developer_address = '\n'.join(developer_address_raw)
        developer_trader_raw = response.xpath('//li[@class="ZbWJPd LoyuIb"]//div[@class="nws2nb"]/text()').get()
        data['developer']['address'] = developer_address if developer_address else None
        data['developer']['website'] = response.xpath('//a[@class="Gztlsc"]/@href').get()
        data['developer']['trader'] = True if developer_trader_raw.lower() == 'Trader'.lower() else False

        l.add_value('url', response.url)
        l.add_value('id', id)
        l.add_xpath('category', '//a[@class="gqpEIe bgp7Ye"]/text()')
        l.add_xpath('website_owner', '//a[@class="cJI8ee"]/@href')
        l.add_value('created_by_the_website_owner', data['created_by_the_website_owner'])
        l.add_value('developer', data['developer'])
        l.add_value('icon', data['icon'])
        l.add_value('small_promo_tile', data['small_promo_tile'])
        l.add_value('title', data['title'])
        l.add_value('rating', data['rating'])
        l.add_value('rating_count', data['rating_count'])
        l.add_value('type', data['type'])
        l.add_value('users', data['users'])
        l.add_value('screenshots', data['screenshots'])
        l.add_value('overview', data['overview'])
        l.add_value('version', data['version'])
        l.add_value('size', data['size'])
        l.add_value('languages', data['languages'])
        l.add_value('last_updated', data['last_updated'])

        # TODO reviews
        # https://chromewebstore.google.com/_/ChromeWebStoreConsumerFeUi/data/batchexecute
        # + query string parameters
        # + form data

        # TODO Add privacy data?
        # TODO Add related extensions data?
        yield l.load_item()
