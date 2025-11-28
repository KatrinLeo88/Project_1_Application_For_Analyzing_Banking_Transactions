import os
from typing import Dict, List
import requests
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv, find_dotenv

from src.logger import setup_logger

load_dotenv(find_dotenv())

logger = setup_logger("utils", "utils.log")

def load_transactions_excel(path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла в DataFrame."""
    logger.info(f"Загрузка данных из файла: {path}")
    try:
        df = pd.read_excel(path)
        logger.info("Данные успешно загружены")
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel: {e}")
        return pd.DataFrame()

def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """Получает курсы валют через API."""
    logger.info(f"Запрос курсов валют для: {currencies}")
    
    url = "https://api.apilayer.com/exchangerates_data/latest"
    api_key = os.getenv("API_KEY_CURRENCY")
    
    rates_data = []
    
    if not api_key:
        logger.warning("API Key для валют не найден в .env. Возвращаем пустые данные.")
        return [{"currency": curr, "rate": 0.0} for curr in currencies]

    try:
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers, params={"base": "RUB", "symbols": ",".join(currencies)}, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})

            for curr in currencies:
                rate = rates.get(curr, 0.0)

                if rate > 0:
                    rate = round(1 / rate, 2) 
                rates_data.append({"currency": curr, "rate": rate})
        else:
            logger.error(f"Ошибка API валют: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Ошибка подключения к API валют: {e}")
        
    return rates_data


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """Получает стоимость акций."""
    logger.info(f"Запрос стоимости акций: {stocks}")
    api_key = os.getenv("API_KEY_STOCKS")
    stock_data = []
    
    if not api_key:
        logger.warning("API Key для акций не найден. Возвращаем заглушки.")

        import random
        return [{"stock": stock, "price": round(random.uniform(100, 3000), 2)} for stock in stocks]

    try:
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                price = float(data.get("Global Quote", {}).get("05. price", 0.0))
                stock_data.append({"stock": stock, "price": price})
            else:
                logger.error(f"Ошибка API акций для {stock}")
    except Exception as e:
        logger.error(f"Ошибка подключения к API акций: {e}")
        
    return stock_data

def get_greeting() -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
