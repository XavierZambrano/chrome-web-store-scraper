# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Identity


def take_second(value):
    if len(value) > 1:
        return value[1]


@dataclass
class ChromeWebStoreItem:
    id: str = field(default=None)
    url: str = field(default=None)
    title: str = field(default=None)
    icon: str = field(default=None)
    small_promo_tile: str = field(default=None)
    website_owner: str = field(default=None)
    created_by_the_website_owner: bool = field(default=None)
    featured: bool = field(default=None)
    rating: float = field(default=0.0)
    rating_count: int = field(default=0)
    type: str = field(default=None)
    category: str = field(default=None)
    users: int = field(default=0)
    screenshots: list[str] = field(default_factory=list)
    overview: str = field(default=None)
    version: str = field(default=None)
    size: str = field(default=None)
    languages: list[str] = field(default_factory=list)
    last_updated: int = field(default=None)
    developer: dict[str, str] = field(default_factory=dict)


class ChromeWebStoreItemLoader(ItemLoader):
    default_item_class = ChromeWebStoreItem

    url_in = MapCompose(str)
    url_out = TakeFirst()

    id_in = MapCompose(str)
    id_out = TakeFirst()

    title_in = MapCompose(str)
    title_out = TakeFirst()

    icon_in = MapCompose(str)
    icon_out = TakeFirst()

    small_promo_tile_in = MapCompose(str)
    small_promo_tile_out = TakeFirst()

    website_owner_in = MapCompose(str)
    website_owner_out = TakeFirst()

    created_by_the_website_owner_in = MapCompose(bool)
    created_by_the_website_owner_out = TakeFirst()

    featured_in = MapCompose(bool)
    featured_out = TakeFirst()

    rating_in = MapCompose(float)
    rating_out = take_second

    rating_count_in = MapCompose(int)
    rating_count_out = take_second

    type_in = MapCompose(str)
    type_out = TakeFirst()

    category_in = MapCompose(str)
    category_out = TakeFirst()

    users_in = MapCompose(int)
    users_out = take_second

    screenshots_in = Identity()
    screenshots_out = Identity()

    overview_in = MapCompose(str)
    overview_out = TakeFirst()

    version_in = MapCompose(str)
    version_out = TakeFirst()

    size_in = MapCompose(str)
    size_out = TakeFirst()

    languages_in = Identity()
    languages_out = Identity()

    last_updated_in = MapCompose(int)
    last_updated_out = TakeFirst()

    developer_in = MapCompose(dict)
    developer_out = take_second
