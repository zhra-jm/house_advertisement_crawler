from bs4 import BeautifulSoup


class AdvertisementPageParser:
    def parse(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        # data = dict(
        #     title=None, price=None, body=None, post_id=None,
        #     created_time=None, modified_time=None
        # )
        data = dict(title=None)
        title_tag = soup.find('span', attrs={'id': 'titletextonly'})
        if title_tag:
            data['title'] = title_tag.text

        price_tag = soup.find('span', attrs={'class': 'price'})

        return data
