import pandas as pd

from src.logger import setup_logger

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
