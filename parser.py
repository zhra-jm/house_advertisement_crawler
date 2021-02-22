from bs4 import BeautifulSoup


class AdvertisementPageParser:
    def parse(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        data = dict(
            title=None, price=None, body=None, post_id=None,
            created_time=None, modified_time=None
        )
        title_tag = soup.find('span', attrs={'id': 'titletextonly'})
        if title_tag:
            data['title'] = title_tag.text

        price_tag = soup.find('span', attrs={'class': 'price'})
        if price_tag:
            data['price'] = price_tag.text

        body_tag = soup.select_one('#postingbody')
        if body_tag:
            data['body'] = body_tag.text
        #
        # post_id_tag = soup.find('p', attrs={'class': 'postinginfo'})
        # if post_id_tag:
        #     data['post_id'] = post_id_tag.text
        #
        # created_time_tag = soup.find('time',attrs={'class': 'date timeago'})
        # if created_time_tag:
        #     data['created_time'] = created_time_tag.text
        #
        # modified_time_tag = soup.find('p', attrs={'class':"postinginfo reveal"})
        # if modified_time_tag:
        #     data['modified_time'] = modified_time_tag.text
        # return data
