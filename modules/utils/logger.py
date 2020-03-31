# https://github.com/Delgan/loguru
from loguru import logger
import os
import sys


def get_logger(log_level="INFO"):
    if os.getenv("LOG_LEVEL") in ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]:
        log_level = os.environ["LOG_LEVEL"]  # 環境変数の値を優先する

    # loggerはSignletonにするため、初回以外は設定を変更しない
    if logger is None:
        logger.add(
            sys.stdout, format="{time} {level} {name} {message}", backtrace=True, diagnose=True, level=log_level)

    return logger
