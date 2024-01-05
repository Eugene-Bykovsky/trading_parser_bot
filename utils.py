def format_telegram_message(data):
    telegram_message = (
        f"Новая инсайдерская сделка:\n"
        f" 🗓Дата регистрации отчета: {data['report_date']}\n"
        f"Дата совершения сделки: {data['trade_date']}\n\n"
        f"🇺🇸Тикер компании: {data['ticker']}\n"
        f"Название компании: {data['company_name']}\n\n"
        f"🤵ФИО инсайдера: {data['insider_name']}\n"
        f"Должность инсайдера: {data['position']}\n\n"
        f"🔴Тип сделки: {data['trade_type']}\n\n"
        f"💵Цена: {data['price']}\n"
        f"🧮Количество: {data['quantity']}\n"
        f"📊Количество акций в собственности: {data['owned']}\n"
        f"📈Процент изменения: {data['own']}\n"
        f"💰Общая сумма сделки: {data['value']}\n"
    )
    return telegram_message
