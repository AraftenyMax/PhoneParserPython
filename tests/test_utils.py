import unittest
from bs4 import BeautifulSoup
from src.parser import Parser
from src.utils import load_config_file


class Tests(unittest.TestCase):

    def test_load_json(self):
        expected_value = "//h2[contains(@class, '_4462670')]//a"
        data = load_config_file("allegro.json")
        self.assertEqual(data["CheckXpaths"]["DetailLinkSelector"], expected_value, "Config loading is working")

    def test_page_crawler(self):
        title = 'Xiaomi Redmi S2 3/32Gb (Gray) Официальная международная версия.' \
                ' Купить Xiaomi Redmi S2 3/32Gb (Gray) Официальная международная версия' \
                ' по низкой цене в Киеве, Харькове, Одессе, Днепре, Николаеве, Запорожье, Украине | Цитрус'
        page = Parser.get_page('https://www.citrus.ua/smartfony/s2-332-gb-gray-xiaomi-ua-628874.html')
        html = BeautifulSoup(page, "html.parser")
        self.assertEqual(title, html.title.string)


if __name__ == '__main__':
    unittest.main()