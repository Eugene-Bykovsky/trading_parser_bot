from requests import get, RequestException
from bs4 import BeautifulSoup

from config import URL


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
                        deals = {
                            'report_date': cells[1].get_text(),
                            'trade_date': cells[2].get_text(),
                            'ticker': cells[3].get_text(),
                            'company_name': cells[4].get_text(),
                            'insider_name': cells[5].text.strip(),
                            'position': cells[6].text.strip(),
                            'trade_type': cells[7].text.strip(),
                            'price': cells[8].text.strip(),
                            'quantity': cells[9].text.strip(),
                            'owned': cells[10].text.strip(),
                            'own': cells[11].text.strip(),
                            'value': cells[12].text.strip(),
                        }
                return deals
            except AttributeError:
                print("No table with class tinytable.")
        else:
            return 'No page content to parse. Call fetch_page() first.'
