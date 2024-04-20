# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
from decimal import Context
import psycopg2
import json

from chrome_web_store_scraper.errors import DynamoDbPipelineProcessError


ctx = Context(prec=6)


def default_encoder(value):
    if isinstance(value, float):
        return ctx.create_decimal_from_float(value)
    else:
        return value


def postgresql_encoder(value):
    if isinstance(value, dict):
        return json.dumps(value)
    elif isinstance(value, float):
        return ctx.create_decimal_from_float(value)
    else:
        return value


class DynamoDbPipeline(object):
    def __init__(self, stats, aws_access_key_id, aws_secret_access_key, region_name, table_name, encoder=default_encoder):
        self.stats = stats
        self.encoder = encoder
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.table_name = table_name
        self.table = None

        stats.set_value('spider_exceptions/DynamoDbPipelineProcessError', 0)

    @classmethod
    def from_crawler(cls, crawler):
        aws_access_key_id = crawler.settings.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = crawler.settings.get('AWS_SECRET_ACCESS_KEY')
        region_name = crawler.settings.get('AWS_REGION_NAME')
        table_name = crawler.settings.get('DYNAMODB_TABLE_NAME')

        return cls(
            stats=crawler.stats,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            table_name=table_name,
        )

    def open_spider(self, spider):
        db = boto3.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )
        self.table = db.Table(self.table_name)
        self.table.load()

    def close_spider(self, spider):
        self.table = None
        spider.logger.info(f'Stored ({self.stats.get_value("item_scraped_count")} items) in DynamoDB table: {self.table_name}')

    def process_item(self, item, spider):
        try:
            self.table.put_item(
                Item={k: self.encoder(v) for k, v in ItemAdapter(item).items()}
            )
        except Exception as e:
            self.stats.inc_value('spider_exceptions/DynamoDbPipelineProcessError')
            raise DynamoDbPipelineProcessError(e)

        return item


class PostgresqlPipeline(object):
    def __init__(self, host, user, password, db_name, table_name='chrome_web_store_item', encoder=postgresql_encoder):
        self.encoder = encoder
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.table_name = table_name
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('PGHOST')
        user = crawler.settings.get('PGUSER')
        password = crawler.settings.get('PGPASSWORD')
        db_name = crawler.settings.get('PGDATABASE')

        return cls(
            host=host,
            user=user,
            password=password,
            db_name=db_name,
        )

    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            dbname=self.db_name,
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        spider.logger.info(f'Stored ({self.cursor.rowcount} items) in PostgreSQL table: {self.table_name}')

    def process_item(self, item, spider):
        insert_query = f'''
            INSERT INTO {self.table_name} (
                id, url, title, icon, small_promo_tile, website_owner, created_by_the_website_owner,
                featured, rating, rating_count, type, category, users, screenshots, overview,
                version, size, languages, last_updated, developer
            ) VALUES (
                %(id)s, %(url)s, %(title)s, %(icon)s, %(small_promo_tile)s, %(website_owner)s, %(created_by_the_website_owner)s,
                %(featured)s, %(rating)s, %(rating_count)s, %(type)s, %(category)s, %(users)s, %(screenshots)s, %(overview)s,
                %(version)s, %(size)s, %(languages)s, %(last_updated)s, %(developer)s
            ) ON CONFLICT (id) DO UPDATE SET
                url = excluded.url,
                title = excluded.title,
                icon = excluded.icon,
                small_promo_tile = excluded.small_promo_tile,
                website_owner = excluded.website_owner,
                created_by_the_website_owner = excluded.created_by_the_website_owner,
                featured = excluded.featured,
                rating = excluded.rating,
                rating_count = excluded.rating_count,
                type = excluded.type,
                category = excluded.category,
                users = excluded.users,
                screenshots = excluded.screenshots,
                overview = excluded.overview,
                version = excluded.version,
                size = excluded.size,
                languages = excluded.languages,
                last_updated = excluded.last_updated,
                developer = excluded.developer
        '''
        self.cursor.execute(insert_query, {k: self.encoder(v) for k, v in ItemAdapter(item).items()})

        self.conn.commit()

        return item
