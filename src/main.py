import os

import pandas as pd

from src.reports import spending_by_category
from src.services import simple_search
from src.utils import load_transactions_excel
from src.views import main_page_view


def main() -> None:
    print("\n--- 1. ГЛАВНАЯ СТРАНИЦА (VIEWS) ---")

    result_view = main_page_view("2021-12-21 15:00:00")
    print(result_view)

    file_path = os.path.join("data", "operations.xlsx")
    if os.path.exists(file_path):
        df = load_transactions_excel(file_path)
        transactions_list = df.to_dict(orient="records")
    else:
        print("\n[WARNING] Файл operations.xlsx не найден в папке data. Тесты будут на пустых данных.")
        df = pd.DataFrame()
        transactions_list = []

    print("\n--- 2. СЕРВИСЫ (SIMPLE SEARCH) ---")
    search_query = "Супермаркет"
    result_search = simple_search(search_query, transactions_list) # type: ignore

    print(f"Результат поиска (первые 200 симв): {result_search[:2000]}...")

    print("\n--- 3. ОТЧЕТЫ (REPORTS) ---")
    category_query = "Супермаркеты"
    result_report = spending_by_category(df, category_query, "21.12.2021 12:00:00")

    print(f"Отчет сформирован. Найдено записей: {len(result_report)}")
    print("Проверьте файл report_....json в корне проекта.")


if __name__ == "__main__":
    main()
