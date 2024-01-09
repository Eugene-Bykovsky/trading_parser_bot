import json
from datetime import datetime


def format_telegram_message(data: dict) -> str:
    # Преобразование строк в объекты datetime
    report_date = datetime.strptime(data['report_date'], "%Y-%m-%d %H:%M:%S")
    trade_date = datetime.strptime(data['trade_date'], "%Y-%m-%d")

    # Форматирование дат в новый формат
    formatted_report_date = report_date.strftime("%d-%m-%Y")
    formatted_trade_date = trade_date.strftime("%d-%m-%Y")

    telegram_message = (
        f"Новая инсайдерская сделка:\n"
        f" 🗓Дата регистрации отчета: {formatted_report_date}\n"
        f"Дата совершения сделки: {formatted_trade_date}\n\n"
        f"🇺🇸Тикер компании: {data['ticker']}\n"
        f"Название компании: {data['company_name']}\n\n"
        f"🤵ФИО инсайдера: {data['insider_name']}\n"
        f"Должность инсайдера: {data['position']}\n\n"
        f"{'🟥' if data['trade_type'][0] == 'S' else '🟩'}Тип сделки: {data['trade_type']}\n\n"
        f"💵Цена: {data['price']}\n"
        f"🧮Количество: {data['quantity']}\n"
        f"📊Количество акций в собственности: {data['owned']}\n"
        f"📈Процент изменения: {data['own']}\n"
        f"💰Общая сумма сделки: {data['value']}\n"
    )
    return telegram_message


def read_data(filename):
    try:
        with open(filename, "r", encoding='utf8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data


def write_data(data, filename):
    with open(filename, "w", encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
