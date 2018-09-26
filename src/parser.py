import os
import requests
from lxml import html
from lxml import etree
from lxml.etree import ParseError
from datetime import datetime
from src.settings import *
from src.log_manager import LogManager
from src.utils import load_config_file, get_base_folder_path, get_datetime_now


class Parser:
    def __init__(self, config_name='allegro', config={}, quantity=10,
                 start_page=1, start_id=1, username='admin', extension='json'):
        self.log_manager = LogManager()
        self.log_manager.on_init(config_name, config, quantity, start_page, start_id, username, extension)
        self.config = config
        self.page = start_page
        self.config_name = config_name
        self.start_id = start_id
        self.item_id = start_id
        self.quantity = quantity
        self.extension = extension
        self.filename = os.path.join(
            get_base_folder_path(), 'parsed_data/{} {}.{}')\
            .format(username, get_datetime_now(), extension)
        self.dump_handler = None

    def start_parse(self):
        try:
            self.dump_handler = self.choose_format_handler(self.extension)
        except Exception as e:
            self.log_manager.on_exception_occurred(e)
            return
        else:
            self.config = load_config_file(self.config_name)
            if self.verify_config():
                self.log_manager.on_init_finish()
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
                self.log_manager.on_exception_occurred(e)
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
                    field_val = tree.xpath(xpath)
                    item_dict[field_name] = self.delete_all_non_ascii(field_val)
                except Exception as e:
                    self.log_manager.on_exception_occurred(e)
        if item_dict:
            item_dict['id'] = item_id
            self.dump_handler(self.filename, item_dict)

    @staticmethod
    def delete_all_non_ascii(text: str) -> str:
        return "".join([x for x in text if x not in SPEC_SYMBOLS]).replace('\\', '')

    def get_page(self, url: str):
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
                self.log_manager.on_exception_occurred(e)
            else:
                return page.content
