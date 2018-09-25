import os
import json
from types import FunctionType

import requests
from lxml import html
from lxml import etree
from lxml.etree import ParseError
from datetime import datetime
from lxml.etree import XPathSyntaxError

from src.settings import *
from src.utils import load_config_file, get_base_folder_path


class Parser:
    def __init__(self, config_name='allegro', config={}, quantity=10,
                 start_page=1, start_id=1, username='admin', extension='json'):
        self.config = config
        self.page = start_page
        self.config_name = config_name
        self.start_id = start_id
        self.item_id = start_id
        self.quantity = quantity
        self.extension = extension
        self.filename = os.path.join(
            get_base_folder_path(), 'parsed_data/{} {}.{}')\
            .format(username, datetime.now().strftime("%b %d %Y %H-%M-%S"), extension)
        self.dump_handler = None

    def start_parse(self):
        try:
            self.dump_handler = self.choose_format_handler(self.extension)
        except Exception as e:
            print(e)
            return
        else:
            self.config = load_config_file(self.config_name)
            if self.verify_config():
                self.parse()

    @staticmethod
    def choose_format_handler(extension):
        if extension in AVAILABLE_DUMPS:
            return AVAILABLE_DUMPS[extension]
        raise Exception('Couldn\'t find handler for this extension')

    def verify_config(self):
        for section_key, fields in REQUIRED_SECTIONS.items():
            section = self.config.get(section_key, None)
            if not section:
                return False
            if section:
                for field in fields:
                    if not section.get(field, None):
                        return False
        return True

    def parse(self):
        while True:
            if self.item_id - self.start_id == self.quantity:
                break
            list_url = self.config['UrlResolveRules']['PageLinkTemplate'].format(str(self.page))
            tree = html.fromstring(self.get_page(list_url))
            try:
                detail_urls = tree.xpath(self.config['CheckXpaths']['DetailLinkSelector'])
            except ParseError as e:
                print(e)
                break
            detail_url_pattern = self.config['UrlResolveRules'].get('DetailLinkTemplate', None)
            if detail_url_pattern:
                detail_urls = [detail_url_pattern.format(x) for x in detail_urls]
            for detail_url in detail_urls:
                self.parse_single_item(str(detail_url), self.item_id)
                self.item_id += 1
            self.page += 1

    def parse_single_item(self, url: str, item_id: int):
        item_dict = {}
        tree = html.fromstring(self.get_page(url))
        if SMFIELDS_SECTION_KEY in self.config.keys():
            for field_name, xpath in self.config[SMFIELDS_SECTION_KEY].items():
                try:
                    item_dict[field_name] = "".join([x for x in tree.xpath(xpath)]).replace(' ', '').replace('\n', '')
                except XPathSyntaxError:
                    print('Invalid xpath: ', xpath)
                except Exception as e:
                    print(e)
        if item_dict:
            item_dict['id'] = item_id
            self.dump_handler(self.filename, item_dict)

    @staticmethod
    def get_page(url: str):
        while True:
            try:
                page = requests.get(url)
            except requests.exceptions.Timeout:
                print("Timeout error, now I will try again...")
                continue
            except requests.exceptions.TooManyRedirects as e:
                print("Something gone bad: your url has too many redirects")
                print(e)
            except requests.exceptions.RequestException as e:
                print(e)
            else:
                return page.content
