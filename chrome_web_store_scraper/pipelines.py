# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
from decimal import Context

from chrome_web_store_scraper.errors import DynamoDbPipelineProcessError


def default_encoder(value):
    ctx = Context(prec=6)
    if isinstance(value, float):
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
