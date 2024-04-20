# chrome-web-store-scraper

This is a scraper for the [Chrome Web Store](https://chromewebstore.google.com/). It extracts data from extensions, themes, and apps.  You can find the dataset at mydomain.com (coming soon). The dataset is updated regularly. Alternatively, you can scrape the data yourself using this scraper.

## Installation

### Setup

1. Clone the repository
2. Create a virtual environment
3. Install the dependencies
```bash
pip install -r requirements.txt
```


### Set proxy (optional)
Set HTTP_PROXY and HTTPS_PROXY in the `.env` file.
```bash
HTTP_PROXY=http://host:port
HTTPS_PROXY=http://host:port
```

### Setup DynamoDB Pipeline (optional)
The DynamoDBPipeline saves the scraped items to a DynamoDB table.

1. Deploy the AWS resources using SAM CLI and copy the AccessKeyId and SecretAccessKey:
```bash
sam build & sam deploy
```
2. Set the env vars in the `.env` file.
```bash
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
AWS_REGION_NAME=YOUR_AWS_REGION
DYNAMODB_TABLE_NAME=YOUR_DYNAMODB_TABLE_NAME
```
3. Config [`settings.py`](chrome_web_store_scraper/settings.py). **Uncomment** the following code in the [`settings.py`](chrome_web_store_scraper/settings.py) file:
```python
ITEM_PIPELINES = {
   # "chrome_web_store_scraper.pipelines.DynamoDbPipeline": 300,
}
```

### Setup PostgresqlPipeline (optional)
The PostgreSQLPipeline saves the scraped items to a PostgreSQL table.

1. Create the PostgreSQL db
2. Set the env vars in the `.env` file.
```bash
PGHOST=YOUR_PGHOST
PGDATABASE=YOUR_PGHDATABASE
PGUSER=YOUR_PGUSER
PGPASSWORD=YOUR_PGPASSWORD
```
3. Create the table, execute [`scripts/create_postgresql_table.py`](scripts/create_postgresql_table.py)
4. Config [`settings.py`](chrome_web_store_scraper/settings.py). **Uncomment** the following code in the [`settings.py`](chrome_web_store_scraper/settings.py) file:
```python
ITEM_PIPELINES = {
  # "chrome_web_store_scraper.pipelines.PostgresqlPipeline": 301,
}
```

## Usage
Note: Remember activate the virtual environment before running the commands.

Scrape the data and use the Pipelines to save the data to a DB.
```bash
scrapy crawl chromewebstore
```

Scrape the data and save in a CSV file. (If a Pipeline is enabled, the data will also be saved also in the corresponding DB)
```bash
scrapy crawl chromewebstore -O output.csv
```

Scrape the data and save in a json file. (If a Pipeline is enabled, the data will also be saved also in the corresponding DB)
```bash
scrapy crawl chromewebstore -O output.json
```

For more information about scrapy crawl arguments, refer to the [scrapy docs](https://docs.scrapy.org/en/latest/topics/commands.html#std-command-crawl).
