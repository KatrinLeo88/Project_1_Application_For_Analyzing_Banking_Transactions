import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def sample_df():
    data = {
        "Дата операции": ["20.12.2021 10:00:00", "15.10.2021 12:00:00"],
        "Категория": ["Супермаркеты", "Аптека"],
        "Сумма": [100, 200],
    }
    return pd.DataFrame(data)


def test_spending_by_category(sample_df: pd.DataFrame) -> None:
    result = spending_by_category(sample_df, "Супермаркеты", "21.12.2021 00:00:00")
    assert len(result) == 1
    assert result.iloc[0]["Категория"] == "Супермаркеты"


def test_spending_by_category_empty(sample_df: pd.DataFrame) -> None:
    result = spending_by_category(sample_df, "Автосервис", "21.12.2021 00:00:00")
    assert len(result) == 0
