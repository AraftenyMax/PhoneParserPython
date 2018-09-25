import unittest

from bs4 import BeautifulSoup

from src.parser import Parser


class TestingPhoneParser(unittest.TestCase):
    def test_page_crawler(self):
        page = Parser.get_page('https://www.citrus.ua/smartfony/s2-332-gb-gray-xiaomi-ua-628874.html')
        html = BeautifulSoup(page, "html.parser")
        self.assertEqual(html.title)