import requests
from bs4 import BeautifulSoup

def get_page(url):
    try:
        response = requests.get(url)
    except requests.HTTPError:
        return None
    return response


def find_links(html_doc):
    soup = BeautifulSoup(html_doc)
    return soup.find_all('a')


if __name__ == "__main__":
    link = 'https://paris.craigslist.org/d/housing/search/hhh?s='
    offers = get_page(link)
    print(offers.status_code)

    # links = find_links(offers.text)
