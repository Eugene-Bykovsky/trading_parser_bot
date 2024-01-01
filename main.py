import os
import sqlite3
from parser import SiteParser
from dotenv import load_dotenv

load_dotenv()


if __name__ == '__main__':
    parser = SiteParser(os.getenv("URL"))
    parser.fetch_content()
    print(parser.page_content)
