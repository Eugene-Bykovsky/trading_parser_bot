from requests import get, RequestException
from bs4 import BeautifulSoup

from config import URL, deal_fields


class SiteParser:
    def __init__(self, url=URL):
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
            try:
                table = soup.find('table', class_='tinytable')
                deals = []

                for deal_row in table.find_all('tr'):
                    cells = deal_row.find_all('td')
                    if cells:
                        deal = {field: cells[i].get_text() for i, field in
                                enumerate(deal_fields, start=1)}
                        deals.append(deal)
                return deals[::-1]
            except AttributeError:
                print("No table with class tinytable.")
        else:
            return 'No page content to parse. Call fetch_page() first.'
