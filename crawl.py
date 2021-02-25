import json
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from storage import MongoStorage, FileStorage
from config import BASE_LINK, STORAGE_TYPE
from parser import AdvertisementPageParser


class CrawlerBase(ABC):

    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'mongo':
            return MongoStorage()
        return FileStorage()

    @abstractmethod
    def start(self, store=False):
        pass

    @abstractmethod
    def store(self, data):
        pass

    @staticmethod
    def get(link):
        try:
            response = requests.get(link)
        except requests.HTTPError:
            return None
        return response

    @staticmethod
    def store(self, data, filename=None):
        pass


class LinkCrawler(CrawlerBase):

    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link
        super().__init__()

    def find_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.find_all('a', attrs={"class", "hdrlnk"})

    def start_crawl_city(self, url):
        start = 0
        crawl = True
        ad_list = list()
        while crawl:
            offers = self.get(url + str(start))
            new_list = self.find_links(offers.text)
            ad_list.extend(new_list)
            start += 120
            crawl = bool(len(new_list))
        return ad_list

    def start(self, store):
        adv_links = list()
        for city in self.cities:
            links = self.start_crawl_city(self.link.format(city))
            print('total', city, len(links))
            adv_links.extend(links)
        if store:
            self.store([{'url': li.get('href')} for li in adv_links])
        return adv_links

    def store(self, data, *args):
        self.storage.store(data, 'advertisement_links')


class DataCrawler(CrawlerBase):
    def __init__(self):
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()
        super().__init__()

    @staticmethod
    def __load_links():
        with open('fixtures/data.json', 'r') as f:
            links = json.loads(f.read())
        return links

    def start(self, store):
        for link in self.links:
            response = self.get(link)
            data = self.parser.parse(response.text)
            if store:
                self.store(data, data.get('post_id', 'sample'))

    def store(self, data, filename):
        self.storage.store(data, 'advertisement_data')
        print(data['post_id'])
