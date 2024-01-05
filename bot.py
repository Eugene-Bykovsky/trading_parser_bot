import asyncio
import json

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from parser import SiteParser
from config import TOKEN, CHAT_ID
from utils import format_telegram_message

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def send_deals_with_delay(bot: Bot) -> None:
    insider_parser = SiteParser()
    insider_parser.fetch_content()
    list_deals = insider_parser.parse_all_deals()
    for deal in list_deals:
        await bot.send_message(chat_id=CHAT_ID,
                               text=format_telegram_message(deal))
        await asyncio.sleep(5)


async def start_bot() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.send_message(chat_id=CHAT_ID, text="Бот запущен!")
    await send_deals_with_delay(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
