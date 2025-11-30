import json
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.views import main_page_view


@patch("src.views.load_transactions_excel")
def test_main_page_view(mock_load: Any) -> None:
    data = {
        "Дата операции": ["2021-12-20 10:00:00", "2021-12-20 11:00:00"],
        "Номер карты": [1234567812345678, 1234567812345678],
        "Сумма платежа": [-100.0, -200.0],
        "Категория": ["Еда", "Еда"],
        "Описание": ["Магазин", "Кафе"],
    }
    mock_load.return_value = pd.DataFrame(data)

    result_json = main_page_view("2021-12-21 12:00:00")
    result = json.loads(result_json)

    assert "greeting" in result
    assert "cards" in result
    assert len(result["cards"]) == 1
    assert result["cards"][0]["last_digits"] == "5678"
    assert result["cards"][0]["total_spent"] == 300.0
