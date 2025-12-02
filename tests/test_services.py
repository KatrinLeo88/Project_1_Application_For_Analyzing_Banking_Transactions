import json
from typing import Any, Dict, List

import pytest

from src.services import simple_search


@pytest.fixture
def transactions_data() -> List[Dict[str, Any]]:
    return [
        {"Описание": "Магазин Пятерочка", "Категория": "Продукты", "Сумма": 100},
        {"Описание": "Аптека", "Категория": "Лекарства", "Сумма": 500},
        {"Описание": "Кинотеатр", "Категория": "Развлечения", "Сумма": 300},
    ]


@pytest.mark.parametrize(
    "query, expected_count, expected_desc",
    [
        ("Пятерочка", 1, "Магазин Пятерочка"),
        ("Лекарства", 1, "Аптека"),
        ("Автосалон", 0, None),
        ("", 0, None),
    ],
)
def test_simple_search(
    transactions_data: List[Dict[str, Any]], query: str, expected_count: int, expected_desc: str
) -> None:
    result_json = simple_search(query, transactions_data)
    result = json.loads(result_json)

    assert len(result) == expected_count
    if expected_count > 0 and expected_desc:
        found = False
        for item in result:
            if item.get("Описание") == expected_desc:
                found = True
                break
        assert found
