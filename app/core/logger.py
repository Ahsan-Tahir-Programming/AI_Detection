"""Logging setup with rotating file handler and console output."""
import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import LOG_DIR

# Create logger
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

# Only add handlers if none exist yet to avoid duplicate logs during reload
if not logger.handlers:
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")

    # File handler with rotation (10MB per file, keep 5 backups)
    log_file_path = os.path.join(LOG_DIR, "app.log")
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
