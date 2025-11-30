from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd

from src.utils import get_currency_rates, get_greeting, get_stock_prices, load_transactions_excel


@patch("requests.get")
def test_get_currency_rates(mock_get: Any) -> None:

    mock_response = MagicMock()
    mock_response.status_code = 200

    mock_response.json.return_value = {"rates": {"USD": 0.013, "EUR": 0.011}}
    mock_get.return_value = mock_response

    result = get_currency_rates(["USD", "EUR"])

    assert len(result) == 2
    assert result[0]["currency"] == "USD"

    assert result[0]["rate"] == 76.92


@patch("requests.get")
def test_get_stock_prices(mock_get: Any) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"Global Quote": {"05. price": "150.00"}}
    mock_get.return_value = mock_response

    result = get_stock_prices(["AAPL"])
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == 150.00


def test_get_greeting() -> None:
    greeting = get_greeting()
    assert greeting in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]


def test_load_transactions_excel_file_not_found() -> None:
    result = load_transactions_excel("non_existent_file.xlsx")
    assert result.empty


@patch("pandas.read_excel")
def test_load_transactions_excel_success(mock_read: Any) -> None:
    mock_df = pd.DataFrame({"col1": [1, 2]})
    mock_read.return_value = mock_df
    result = load_transactions_excel("dummy.xlsx")
    assert not result.empty
    assert result.iloc[0]["col1"] == 1
