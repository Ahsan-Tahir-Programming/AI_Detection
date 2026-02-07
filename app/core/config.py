# Paths, environment vars, constants
import os

# --- PATH SETUP ---

# 1. Get the path of THIS file (config.py) -> ".../app/core/config.py"
FILE_PATH = os.path.abspath(__file__)

# 2. Go up one step to 'core' folder -> ".../app/core"
CORE_DIR = os.path.dirname(FILE_PATH)

# 3. Go up one more step to 'app' folder -> ".../app"
APP_DIR = os.path.dirname(CORE_DIR)

# --- DIRECTORIES SETUP ---
# --- MODELS PATH ---
# MODELS: Inside app/models -> ".../app/models"
MODELS_DIR = os.path.join(APP_DIR, "models")

# --- DOWNLOAD PATH ---
# # Handle Docker Environment path vs Local path for Downloads
if os.getenv("DOCKER_ENV"):
    # In Docker, we use the absolute path we created in Dockerfile
    DOWNLOAD_DIR = "/app/download"
else:
    # Locally, we create 'download' inside the 'app' folder -> ".../app/download"
    DOWNLOAD_DIR = os.path.join("app/download")

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# --- FONT PATH ---
# Assuming ARIALBD.TTF is inside the 'app/assets' folder -> ".../app/assets/ARIALBD.TTF"
FONT_PATH = os.path.join(APP_DIR, "assets", "ARIALBD.TTF")

# --- LOAD CLASS CONFIGURATION ---
# Load class names, colors, and mappings from classes.txt file
CLASSES_FILE = os.path.join(APP_DIR, "assets", "classes.txt")

CLASS_COLORS = {}
CLASS_NAME_MAP = {}

if os.path.exists(CLASSES_FILE):
    with open(CLASSES_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('|')
            if len(parts) >= 4:
                yolo_class = parts[0]
                mapped_class = parts[1]
                try:
                    r, g, b = int(parts[2]), int(parts[3]), int(parts[4])
                    CLASS_COLORS[yolo_class] = (r, g, b)
                    CLASS_NAME_MAP[yolo_class] = mapped_class
                except (ValueError, IndexError):
                    print(f"Warning: Could not parse class line: {line}")
else:
    print(f"Warning: Classes file not found at {CLASSES_FILE}")
    # Fallback to hardcoded values if file doesn't exist
    CLASS_COLORS = {
        "Backlit Not Functional": (255, 0, 0),
        "Backlit Functional": (0, 255, 0),
        "BWU Damage": (255, 165, 0),
        "Compartment": (0, 0, 255),
        "CAN Compartment Damage": (255, 0, 255),
        "Paint Fade Off": (255, 255, 0),
        "Visibility Hidden With Others Items": (128, 0, 128),
        "ZYN Logo Damage": (255, 20, 147),
        "Asset Available Not Deployed": (0, 255, 255)
    }