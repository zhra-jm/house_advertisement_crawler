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
            self.store([{'url': li.get('href'), 'flag': False} for li in adv_links])
        return adv_links

    def store(self, data, *args):
        self.storage.store(data, 'advertisement_links')


class DataCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()

    def __load_links(self):
        return self.storage.load('advertisement_links', {'flag': False})

    def start(self, store):
        for link in self.links:
            response = self.get(link['url'])
            data = self.parser.parse(response.text)
            if store:
                self.store(data, data.get('post_id', 'sample'))
            self.storage.update_flag(data)

    def store(self, data, filename):
        self.storage.store(data, 'advertisement_data')
        print(data['post_id'])


class ImageDownloader(CrawlerBase):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.advertisements = self.__load_advertisements()

    def __load_advertisements(self):
        return self.storage.load('advertisement_data')

    @staticmethod
    def get(link):
        try:
            response = requests.get(link, stream=True)
        except requests.HTTPError:
            return None
        return response

    def start(self, store=True):
        for advertisement in self.advertisements:
            counter = 1
            for image in advertisement['images']:
                response = self.get(image['url'])
                if store:
                    self.store(response, advertisement['post_id'], counter)
                counter += 1

    def store(self, data, adv_id, img_number):
        filename = f'{adv_id} - {img_number}'
        return self.save_to_disc(data, filename)

    def save_to_disc(self, response, filename):
        with open(f'fixtures/images/{filename}.jpg', 'ab') as f:
            f.write(response.content)
            for _ in response.iter_content():
                f.write(response.content)
        print(filename)
        return filename
