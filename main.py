from parser import SiteParser


if __name__ == '__main__':
    insider_parser = SiteParser()
    insider_parser.fetch_content()
    print(insider_parser.parse_all_deals())
