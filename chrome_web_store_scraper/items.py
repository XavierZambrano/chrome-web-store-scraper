# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass


@dataclass
class ChromeWebStoreItem:
    url: str
    id: str
    name: str
    logo: str
    banner: str
    website_owner: str
    created_by_the_website_owner: bool
    featured: bool
    rating: float
    rating_count: int
    category: str
    subcategory: str
    users: int
    images: list[str]
    overview: str
    version: str
    size: str
    languages: list[str]
    last_updated: int
    developer: dict[str, str]