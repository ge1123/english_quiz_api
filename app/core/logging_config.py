# app/core/logging_config.py
from loguru import logger
import sys

def setup_logger():
    logger.remove()
    logger.add(sys.stdout, level="INFO", enqueue=True, colorize=True, backtrace=True, diagnose=False)
    logger.add("logs/english_api.log", rotation="1 week", level="DEBUG", encoding="utf-8", enqueue=True)
