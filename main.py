import requests
from bs4 import BeautifulSoup


def get_page(url, start):
    try:
        response = requests.get(url.format(str(start)))
    except requests.HTTPError:
        return None
    print(response.status_code, response.url)
    return response


def find_links(html_doc):
    soup = BeautifulSoup(html_doc)
    # content = soup.find('div', attrs={"class", "content"})
    # adv_list = soup.find('li', attrs={"class", "result-row"})
    return soup.find_all('a', attrs={"class", "hdrlnk"})


def start_crawl(url):
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


if __name__ == "__main__":
    link = 'https://paris.craigslist.org/d/housing/search/hhh?s={}'
    links = start_crawl(link)
    print('total', len(links))
