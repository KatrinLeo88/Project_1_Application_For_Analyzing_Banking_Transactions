import logging
import os


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Функция для создания логгера."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_path = os.path.join("logs", log_file)

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
