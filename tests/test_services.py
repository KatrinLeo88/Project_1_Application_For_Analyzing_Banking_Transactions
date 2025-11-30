import json
from typing import Any, Dict, List

import pytest

from src.services import simple_search


@pytest.fixture
def transactions_data() -> List[Dict[str, Any]]:
    return [
        {"Описание": "Магазин Пятерочка", "Категория": "Продукты", "Сумма": 100},
        {"Описание": "Аптека", "Категория": "Лекарства", "Сумма": 500},
        {"Описание": "Кино", "Категория": "Развлечения", "Сумма": 300},
    ]


def test_simple_search_found(transactions_data: List[Dict[str, Any]]) -> None:
    result_json = simple_search("Пятерочка", transactions_data)
    result = json.loads(result_json)
    assert len(result) == 1
    assert result[0]["Описание"] == "Магазин Пятерочка"


def test_simple_search_category(transactions_data: List[Dict[str, Any]]) -> None:
    result_json = simple_search("Лекарства", transactions_data)
    result = json.loads(result_json)
    assert len(result) == 1


def test_simple_search_not_found(transactions_data: List[Dict[str, Any]]) -> None:
    result_json = simple_search("Автосалон", transactions_data)
    result = json.loads(result_json)
    assert len(result) == 0


def test_simple_search_empty_query(transactions_data: List[Dict[str, Any]]) -> None:
    result_json = simple_search("", transactions_data)
    result = json.loads(result_json)
    assert result == []
