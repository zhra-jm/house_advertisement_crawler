import requests
from bs4 import BeautifulSoup


def get_page(url, start):
    try:
        response = requests.get(url + str(start))
    except requests.HTTPError:
        return None
    # print(response.status_code, response.url)
    return response


def find_links(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    # content = soup.find('div', attrs={"class", "content"})
    # adv_list = soup.find('li', attrs={"class", "result-row"})
    return soup.find_all('a', attrs={"class", "hdrlnk"})


def start_crawl_city(url):
    start = 0
    crawl = True
    ad_list = list()
    while crawl:
        offers = get_page(url, start)
        new_list = find_links(offers.text)
        ad_list.extend(new_list)
        start += 120
        crawl = bool(len(new_list))
    return ad_list


def start_crawl():
    cities = ['paris', 'munich', 'amsterdam', 'berlin']
    link = 'https://{}.craigslist.org/d/housing/search/hhh?s='
    for city in cities:
        links = start_crawl_city(link.format(city))
        print('total', city, len(links))


if __name__ == "__main__":
    start_crawl()
