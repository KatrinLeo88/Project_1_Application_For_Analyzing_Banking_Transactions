import json
import re
from typing import Any, Dict, List

from src.logger import setup_logger

logger = setup_logger("services", "services.log")


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> str:
    """
    Пользователь передает строку для поиска, возвращается JSON-ответ
    со всеми транзакциями, содержащими запрос в описании или категории.
    """
    logger.info(f"Вызван сервис simple_search с запросом: '{query}'")

    if not query:
        logger.warning("Передан пустой запрос")
        return json.dumps([], ensure_ascii=False)

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    result = []

    for txn in transactions:
        description = str(txn.get("Описание", ""))
        category = str(txn.get("Категория", ""))

        if pattern.search(description) or pattern.search(category):
            result.append(txn)

    logger.info(f"Найдено {len(result)} транзакций")

    return json.dumps(result, ensure_ascii=False, indent=4)
