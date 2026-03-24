# app/utils/logger.py

import logging
import os
from datetime import datetime


# Create logs directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def get_log_file_name():
    """
    Generates log file name based on current date and time
    Example: 2026-03-23_22-10-15.log
    """
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(LOG_DIR, f"{current_time}.log")


# Create single log file per run
LOG_FILE = get_log_file_name()


def get_logger(name: str = "app_logger") -> logging.Logger:
    """
    Returns a configured logger instance
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger

    # Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] "
        "[%(filename)s:%(lineno)d] - %(message)s"
    )

    # File Handler (new file per run)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger