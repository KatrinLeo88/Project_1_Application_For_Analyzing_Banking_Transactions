import functools
import json
from datetime import datetime
from typing import Any, Callable, Optional

import pandas as pd

from src.logger import setup_logger

logger = setup_logger("reports", "reports.log")


def report_to_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор, который записывает результат функции-отчета в файл.
    Если filename не передан, генерирует имя по умолчанию.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            nonlocal filename
            if not filename:
                filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            logger.info(f"Запись отчета в файл: {filename}")

            try:
                if isinstance(result, pd.DataFrame):
                    result.to_json(filename, orient="records", force_ascii=False, indent=4)
                elif isinstance(result, (dict, list)):
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=4)
                else:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(str(result))
            except Exception as e:
                logger.error(f"Ошибка записи отчета: {e}")

            return result

        return wrapper

    return decorator


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние 3 месяца (от переданной даты).
    """
    logger.info(f"Формирование отчета по категории: {category}")

    try:
        if date:
            current_date = pd.to_datetime(date, format="%d.%m.%Y %H:%M:%S", dayfirst=True)
        else:
            current_date = pd.Timestamp.now()

        start_date = current_date - pd.DateOffset(months=3)

        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

        filtered_df = transactions[
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= current_date)
            & (transactions["Категория"].str.contains(category, case=False, na=False))
        ]

        logger.info(f"Найдено {len(filtered_df)} записей")
        return filtered_df

    except Exception as e:
        logger.error(f"Ошибка при формировании отчета: {e}")
        return pd.DataFrame()
