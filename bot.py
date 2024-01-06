import asyncio

from datetime import datetime, time

import schedule
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from parser import SiteParser
from config import TOKEN, CHAT_ID
from utils import format_telegram_message, read_data, write_data

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def send_deals_with_delay(obj_bot) -> None:
    insider_parser = SiteParser()
    insider_parser.fetch_content()
    list_deals = insider_parser.parse_all_deals()

    current_time = datetime.now().time()
    print(current_time)
    if current_time < time(8, 0) or current_time > time(19, 0):
        # Вне рабочего времени, не отправлять сообщения
        return

    last_sent_deal = read_data('last_sent_deal.json')

    last_sent_date_str = last_sent_deal.get('report_date', '')
    last_sent_date = datetime.strptime(last_sent_date_str,
                                       '%Y-%m-%d %H:%M:%S') if last_sent_date_str else datetime.min

    for deal in list_deals:
        deal_date = datetime.strptime(deal['report_date'], '%Y-%m-%d %H:%M:%S')

        if deal_date > last_sent_date:
            await obj_bot.send_message(chat_id=CHAT_ID,
                                       text=format_telegram_message(deal))
            last_sent_deal = deal

        await asyncio.sleep(5)

    write_data(last_sent_deal, 'last_sent_deal.json')


async def start_bot(obj_bot) -> None:
    await send_deals_with_delay(obj_bot)
    await dp.start_polling(obj_bot)


def run_schedule():
    schedule.every(60).minutes.do(
        lambda: asyncio.run(send_deals_with_delay(bot)))

    while True:
        schedule.run_pending()
        asyncio.sleep(1)


if __name__ == '__main__':
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    asyncio.run(start_bot(bot))
    run_schedule()
