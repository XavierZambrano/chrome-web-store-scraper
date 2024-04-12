# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChromeWebStoreItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    logo = scrapy.Field()
    banner = scrapy.Field()
    website_owner = scrapy.Field()
    created_by_the_website_owner = scrapy.Field()
    featured = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    users = scrapy.Field()
    images = scrapy.Field()
    overview = scrapy.Field()
    version = scrapy.Field()
    size = scrapy.Field()
    languages = scrapy.Field()
    last_updated = scrapy.Field()
    developer = scrapy.Field()
