import unittest
import json
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess

from chrome_web_store_scraper.spiders.chromewebstore import ChromeWebStoreSpider
from tests.utils import mock_response_from_file


if 'unittest.util' in __import__('sys').modules:
    # Show full diff in case of failure
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999


class TestChromeWebStoreSpider(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.spider = ChromeWebStoreSpider()
        process = CrawlerProcess(install_root_handler=False)
        crawler = process.create_crawler(ChromeWebStoreSpider)
        self.spider.crawler = crawler

    def test_parse_top_extension(self):
        mock_response = self.get_mock_response(
            'nllcnknpjnininklegdoijpljgdjkijc',
            'https://chromewebstore.google.com/detail/wordtune-generative-ai-pr/nllcnknpjnininklegdoijpljgdjkijc'
        )
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict(), expected_result)

    def test_parse_no_logo(self):
        mock_response = self.get_mock_response(
            'hpaaaecejfpkokofieggejohddmmaajp',
            'https://chromewebstore.google.com/detail/tweaks-for-topmeteoeu/hpaaaecejfpkokofieggejohddmmaajp'
        )
        expected_result = None
        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['logo'], expected_result)



    def get_mock_response(self, id, url):
        mock_response_path = f'assets/example_responses/{id}.html'
        return mock_response_from_file(mock_response_path, url=url)

    def get_expected_result(self, id):
        expected_result_path = f'assets/expected/{id}.json'
        with open(expected_result_path, 'r', encoding='utf-8') as f:
            return json.load(f)
