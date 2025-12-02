import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def sample_df() -> pd.DataFrame:
    data = {
        "Дата операции": ["20.12.2021 10:00:00", "15.10.2021 12:00:00", "20.12.2021 15:00:00"],
        "Категория": ["Супермаркеты", "Аптека", "Супермаркеты"],
        "Сумма": [100, 200, 300],
    }
    return pd.DataFrame(data)


@pytest.mark.parametrize(
    "category, date, expected_len",
    [
        ("Супермаркеты", "21.12.2021 00:00:00", 2),
        ("Аптека", "21.12.2021 00:00:00", 1),
        ("Автосервис", "21.12.2021 00:00:00", 0),
    ],
)
def test_spending_by_category(sample_df: pd.DataFrame, category: str, date: str, expected_len: int) -> None:
    result = spending_by_category(sample_df, category, date)
    assert len(result) == expected_len
