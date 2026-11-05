"""Application configuration, constants, and path definitions."""
import os
from typing import Dict, Tuple

# --- PATH SETUP ---
FILE_PATH = os.path.abspath(__file__)
CORE_DIR = os.path.dirname(FILE_PATH)
APP_DIR = os.path.dirname(CORE_DIR)
BASE_DIR = os.path.dirname(APP_DIR)

# --- DIRECTORIES SETUP ---
MODELS_DIR = os.path.join(APP_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# Handle Docker Environment path vs Local path for Downloads
if os.getenv("DOCKER_ENV"):
    DOWNLOAD_DIR = "/app/download"
else:
    DOWNLOAD_DIR = os.path.join(APP_DIR, "download")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Database directory & URL
DB_DIR = os.path.join(APP_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)
DEFAULT_DB_PATH = os.path.join(DB_DIR, "detections.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# Logs directory
if os.getenv("DOCKER_ENV"):
    LOG_DIR = "/app/logs"
else:
    LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

# --- FONT PATH ---
FONT_PATH = os.path.join(APP_DIR, "assets", "ARIALBD.TTF")

# --- ENVIRONMENT & INFERENCE SETTINGS ---
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ALLOWED_ORIGINS = [
    origin.strip() 
    for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",") 
    if origin.strip()
]
MAX_IMAGE_SIZE_BYTES = int(os.getenv("MAX_IMAGE_SIZE_BYTES", str(25 * 1024 * 1024)))  # 25 MB
DEFAULT_CONFIDENCE = float(os.getenv("DEFAULT_CONFIDENCE", "0.5"))
DEFAULT_IOU = float(os.getenv("DEFAULT_IOU", "0.7"))

# --- CLASS CONFIGURATION ---
CLASSES_FILE = os.path.join(APP_DIR, "assets", "classes.txt")

# Default fallback configuration in case classes.txt is missing or partially corrupted
DEFAULT_CLASS_CONFIG: Dict[str, Tuple[str, Tuple[int, int, int]]] = {
    "Backlit Not Functional": ("backlit_not_functional", (255, 0, 0)),
    "Backlit Functional": ("backlit_functional", (0, 255, 0)),
    "BWU Damage": ("sheet_damaged", (255, 165, 0)),
    "Compartment": ("compartment", (0, 0, 255)),
    "CAN Compartment Damage": ("compartment_damage", (255, 0, 255)),
    "Paint Fade Off": ("paint_fade_off", (255, 255, 0)),
    "Visibility Hidden With Others Items": ("Visibility_hidden_other_items", (128, 0, 128)),
    "ZYN Logo Damage": ("logo_damage", (255, 20, 147)),
    "Asset Available Not Deployed": ("non_compliant", (0, 255, 255)),
}

CLASS_COLORS: Dict[str, Tuple[int, int, int]] = {}
CLASS_NAME_MAP: Dict[str, str] = {}

if os.path.exists(CLASSES_FILE):
    try:
        with open(CLASSES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) >= 5:
                    yolo_class = parts[0].strip()
                    mapped_class = parts[1].strip()
                    try:
                        r, g, b = int(parts[2]), int(parts[3]), int(parts[4])
                        CLASS_COLORS[yolo_class] = (r, g, b)
                        CLASS_NAME_MAP[yolo_class] = mapped_class
                    except ValueError:
                        pass
    except Exception:
        pass

# Populate fallback values for any missing mappings
for yolo_cls, (mapped_cls, color) in DEFAULT_CLASS_CONFIG.items():
    if yolo_cls not in CLASS_COLORS:
        CLASS_COLORS[yolo_cls] = color
    if yolo_cls not in CLASS_NAME_MAP:
        CLASS_NAME_MAP[yolo_cls] = mapped_cls