import logging
from logging.handlers import RotatingFileHandler
import os

# Environment-aware log directory (same pattern as main.py)
if os.getenv("DOCKER_ENV"):
    LOG_DIR = "/app/logs"  # Docker volume path
else:
    LOG_DIR = "logs" # Local path

# Ensure logs folder exists
os.makedirs(LOG_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

# File handler with rotation (e.g., max 5MB per file, keep 3 backups)
file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"), # Use os.path.join for proper path
    maxBytes=10*1024*1024,
    backupCount=5
)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
file_handler.setFormatter(formatter)

# Console handler (for local/debug)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
