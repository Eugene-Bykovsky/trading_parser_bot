import os

from requests import get, RequestException
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


class SiteParser:
    def __init__(self, url=os.getenv("URL")):
        self.url = url
        self.page_content = None

    def fetch_content(self):
        try:
            response = get(self.url)
            response.raise_for_status()
            self.page_content = response.text
        except RequestException as e:
            print(f'failed to fetch the page. Error {e}')

    def parse_all_deals(self):
        if self.page_content:
            soup = BeautifulSoup(self.page_content, 'html.parser')
            return soup.find_all('tr')
        else:
            return 'No page content to parse. Call fetch_page() first.'
