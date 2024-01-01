from requests import get, RequestException
from bs4 import BeautifulSoup


class SiteParser:
    def __init__(self, url):
        self.url = url
        self.page_content = None

    def fetch_content(self):
        try:
            response = get(self.url)
            response.raise_for_status()
            self.page_content = response.text
        except RequestException as e:
            print(f'failed to fetch the page. Error {e}')
