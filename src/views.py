import json
import os
from datetime import datetime

import pandas as pd

from src.logger import setup_logger
from src.utils import get_currency_rates, get_greeting, get_stock_prices, load_transactions_excel

logger = setup_logger("views", "views.log")


def main_page_view(date_str: str) -> str:
    """
    Главная функция страницы «Главная».
    Принимает дату и время (YYYY-MM-DD HH:MM:SS).
    Возвращает JSON с приветствием, картами, топом транзакций, курсами и акциями.
    """
    logger.info(f"Генерация главной страницы для даты: {date_str}")

    try:
        with open("user_settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
        user_currencies = settings.get("user_currencies", [])
        user_stocks = settings.get("user_stocks", [])
    except FileNotFoundError:
        logger.error("Файл настроек user_settings.json не найден")
        user_currencies = ["USD", "EUR"]
        user_stocks = []

    greeting = get_greeting()

    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        start_of_month = target_date.replace(day=1, hour=0, minute=0, second=0)

        file_path = os.path.join("data", "operations.xlsx")
        df = load_transactions_excel(file_path)

        if df.empty:
            raise ValueError("Пустой DataFrame")

        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

        filtered_df = df[(df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= target_date)]
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

    cards_data = []
    try:

        if "Номер карты" in filtered_df.columns:
            cards_groups = filtered_df.groupby("Номер карты")
            for card_num, group in cards_groups:
                if pd.isna(card_num):
                    continue

                expenses = group[group["Сумма платежа"] < 0]["Сумма платежа"].sum()
                total_spent = abs(expenses)

                cashback = round(total_spent / 100, 2)

                cards_data.append(
                    {"last_digits": str(card_num)[-4:], "total_spent": round(total_spent, 2), "cashback": cashback}
                )
    except Exception as e:
        logger.error(f"Ошибка расчета карт: {e}")

    top_transactions = []
    try:
        top5 = filtered_df.sort_values(by="Сумма платежа", key=abs, ascending=False).head(5)

        for _, row in top5.iterrows():
            top_transactions.append(
                {
                    "date": row["Дата операции"].strftime("%d.%m.%Y"),
                    "amount": row["Сумма платежа"],
                    "category": row.get("Категория", "Unknown"),
                    "description": row.get("Описание", "Unknown"),
                }
            )
    except Exception as e:
        logger.error(f"Ошибка расчета топа: {e}")

    currency_rates = get_currency_rates(user_currencies)
    stock_prices = get_stock_prices(user_stocks)

    response = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    result_json = json.dumps(response, ensure_ascii=False, indent=4)
    logger.info("Главная страница сформирована успешно")
    return result_json
