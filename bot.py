import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from datetime import datetime, time

from config import TOKEN, CHAT_ID, CHAT_ID_ADMIN
from parser import SiteParser
from utils import format_telegram_message, read_data, write_data

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def send_deals_with_delay(obj_bot) -> None:
    new_deals_found = False
    insider_parser = SiteParser()
    insider_parser.fetch_content()
    list_deals = insider_parser.parse_all_deals()
    await obj_bot.send_message(chat_id=CHAT_ID_ADMIN, text='Парсер запущен!')

    last_sent_deal = read_data('last_sent_deal.json')

    last_sent_date_str = last_sent_deal.get('report_date', '')
    last_sent_date = datetime.strptime(last_sent_date_str,
                                       '%Y-%m-%d %H:%M:%S') if last_sent_date_str else datetime.min

    for deal in list_deals:
        deal_date = datetime.strptime(deal['report_date'], '%Y-%m-%d %H:%M:%S')

        if deal_date <= last_sent_date:
            continue  # Пропускаем уже обработанные сделки

        try:
            new_deals_found = True
            await obj_bot.send_message(chat_id=CHAT_ID, text=format_telegram_message(deal))
            last_sent_deal = deal
            write_data(last_sent_deal, 'last_sent_deal.json')
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error sending deal: {e}")

    print(new_deals_found)
    if not new_deals_found:
        await obj_bot.send_message(chat_id=CHAT_ID_ADMIN, text='Новых сделок пока нет!')


async def start_bot(obj_bot) -> None:
    await obj_bot.send_message(chat_id=CHAT_ID_ADMIN, text='Бот запущен!')

    while True:
        current_time = datetime.now().time()
        print(current_time)
        if time(22, 0) >= current_time <= time(8, 0):
            await asyncio.sleep(3600)  # Перерыв в 1 час, если текущее время внутри указанного интервала
        else:
            try:
                await send_deals_with_delay(obj_bot)
                await asyncio.sleep(3600)
            except Exception as e:
                print(f"Error in bot loop: {e}")

if __name__ == '__main__':
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    asyncio.run(start_bot(bot))
