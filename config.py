import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
URL = os.getenv("URL")
CHAT_ID = os.getenv("CHAT_ID")

deal_fields = ('report_date', 'trade_date', 'ticker', 'company_name',
               'insider_name', 'position', 'trade_type', 'price',
               'quantity', 'owned', 'own', 'value')
