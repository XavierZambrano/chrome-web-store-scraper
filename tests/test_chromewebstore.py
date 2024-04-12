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
        self.mock_response = {
            'nllcnknpjnininklegdoijpljgdjkijc': 'https://chromewebstore.google.com/detail/wordtune-generative-ai-pr/nllcnknpjnininklegdoijpljgdjkijc',
            'hpaaaecejfpkokofieggejohddmmaajp': 'https://chromewebstore.google.com/detail/tweaks-for-topmeteoeu/hpaaaecejfpkokofieggejohddmmaajp',
            'efaidnbmnnnibpcajpcglclefindmkaj': 'https://chromewebstore.google.com/detail/adobe-acrobat-pdf-edit-co/efaidnbmnnnibpcajpcglclefindmkaj',
            'mafbdhjdkjnoafhfelkjpchpaepjknad': 'https://chromewebstore.google.com/detail/morpheon-dark/mafbdhjdkjnoafhfelkjpchpaepjknad'
        }

    def test_parse_top_extension(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict(), expected_result)

    def test_parse_id(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['id']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['id'], expected_result)

    def test_parse_name(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['name']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['name'], expected_result)

    def test_parse_logo(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['logo']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['logo'], expected_result)

    def test_parse_logo_none(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = None
        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['logo'], expected_result)

    def test_parse_banner(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['banner']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['banner'], expected_result)

    def test_parse_banner_none(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = None

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['banner'], expected_result)

    def test_parse_website_owner(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['website_owner']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['website_owner'], expected_result)

    def test_parse_website_owner_none(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = None

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['website_owner'], expected_result)

    def test_parse_created_by_the_website_owner_true(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = True

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['created_by_the_website_owner'], expected_result)

    def test_parse_created_by_the_website_owner_false(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = False

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['created_by_the_website_owner'], expected_result)

    def test_parse_featured_true(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = True

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['featured'], expected_result)

    def test_parse_featured_false(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = False

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['featured'], expected_result)

    def test_parse_rating(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['rating']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['rating'], expected_result)

    def test_parse_rating_without_ratings(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = 0.0

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['rating'], expected_result)

    def test_parse_rating_count(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['rating_count']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['rating_count'], expected_result)

    def test_parse_rating_count_without_ratings(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = 0

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['rating_count'], expected_result)

    def test_parse_category_extension(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['category']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['category'], expected_result)

    def test_parse_category_theme(self):
        mock_response = self.get_mock_response('mafbdhjdkjnoafhfelkjpchpaepjknad')
        expected_result = self.get_expected_result('mafbdhjdkjnoafhfelkjpchpaepjknad')['category']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['category'], expected_result)

    def test_parse_subcategory(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['subcategory']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['subcategory'], expected_result)

    def test_parse_users(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['users']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['users'], expected_result)

    def test_parse_users_zero(self):
        # Find an extension with 0 users
        pass  # TODO

    def test_parse_images(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['images']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['images'], expected_result)

    def test_parse_no_images(self):
        pass  # All the chrome web store items have at least one screenshot

    def test_parse_overview(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['overview']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['overview'], expected_result)

    def test_parse_no_overview(self):
        pass  # All the chrome web store items have an overview

    def test_parse_version(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['version']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['version'], expected_result)

    def test_parse_size(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['size']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['size'], expected_result)

    def test_parse_languages_with_only_one_language(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['languages']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['languages'], expected_result)

    def test_parse_languages_more_than_one(self):
        mock_response = self.get_mock_response('efaidnbmnnnibpcajpcglclefindmkaj')
        expected_result = self.get_expected_result('efaidnbmnnnibpcajpcglclefindmkaj')['languages']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['languages'], expected_result)

    def test_parse_last_updated(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['last_updated']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['last_updated'], expected_result)

    def test_parse_developer_name_when_is_created_by_the_website_owner(self):
        mock_response = self.get_mock_response('nllcnknpjnininklegdoijpljgdjkijc')
        expected_result = self.get_expected_result('nllcnknpjnininklegdoijpljgdjkijc')['developer']['name']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['developer']['name'], expected_result)

    def test_parse_developer_name_when_is_not_created_by_the_website_owner(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = self.get_expected_result('hpaaaecejfpkokofieggejohddmmaajp')['developer']['name']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['developer']['name'], expected_result)

    def test_parse_developer_address_none(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = self.get_expected_result('hpaaaecejfpkokofieggejohddmmaajp')['developer']['address']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['developer']['address'], expected_result)

    def test_parse_developer_website_none(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = self.get_expected_result('hpaaaecejfpkokofieggejohddmmaajp')['developer']['website']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['developer']['website'], expected_result)

    def test_parse_developer_email_none(self):
        # All the chrome web store items have a developer email
        # https://developer.chrome.com/docs/webstore/register
        pass

    def test_parse_developer_trader_false(self):
        mock_response = self.get_mock_response('hpaaaecejfpkokofieggejohddmmaajp')
        expected_result = self.get_expected_result('hpaaaecejfpkokofieggejohddmmaajp')['developer']['trader']

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(ItemAdapter(result).asdict()['developer']['trader'], expected_result)

    def get_mock_response(self, id):
        mock_response_path = f'assets/example_responses/{id}.html'
        mock_response_url = self.mock_response[id]
        return mock_response_from_file(mock_response_path, mock_response_url)

    def get_expected_result(self, id):
        expected_result_path = f'assets/expected/{id}.json'
        with open(expected_result_path, 'r', encoding='utf-8') as f:
            return json.load(f)
