from bs4 import BeautifulSoup


class AdvertisementPageParser:

    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_tag = self.soup.find('span', attrs={'id': 'titletextonly'})
        if title_tag:
            return title_tag.text
        return None

    @property
    def price(self):
        price_tag = self.soup.find('span', attrs={'class': 'price'})
        if price_tag:
            return price_tag.text
        return None

    @property
    def body(self):
        body_tag = self.soup.select_one('#postingbody')
        if body_tag:
            return body_tag.text

    @property
    def post_id(self):
        selector = 'p.postinginfo:nth-child(1)'
        id_tag = self.soup.select_one(selector)
        if id_tag:
            return id_tag.text.replace("post id:", '')

    @property
    def created_time(self):
        time_selector = '.postinginfos > p:nth-child(2) > time:nth-child(1)'
        time = self.soup.select_one(time_selector)
        if time:
            return time.attrs['datetime']

    @property
    def modified_time(self):
        modified_selector = 'p.postinginfo:nth-child(3) > time:nth-child(1)'
        time = self.soup.select_one(modified_selector)
        if time:
            return time.attrs['datetime']

    @property
    def images(self):
        img_list = self.soup.find_all('img')
        img_sources = set([img.attrs['src'].replace('50x50c', '600x450') for img in img_list])
        return [{"url": src, 'flag': False} for src in img_sources]

    def parse(self, html_data):
        self.soup = BeautifulSoup(html_data, 'html.parser')
        data = dict(
            title=self.title, price=self.price, body=self.body, post_id=self.post_id,
            created_time=self.created_time, modified_time=self.modified_time,
            images=self.images
        )

        return data
