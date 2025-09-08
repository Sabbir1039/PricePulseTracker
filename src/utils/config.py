# src/utils/config.py
import os
import logging
from dotenv import load_dotenv

# --- Load environment variables from .env ---
load_dotenv()

# --- Project metadata ---
PROJECT_NAME = "PricePulseTracker"
VERSION = "1.0.0"

# --- Environment variables ---
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", 1))  # default=1 if not set

# --- Directories (absolute paths) ---
# BASE_DIR = PricePulseTracker/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")
TRACKED_FILE = os.path.join(DATA_DIR, "tracked_products.json")
TRACKED_CSV_FILE = os.path.join(DATA_DIR, "tracked_products_CSV.csv")

def ensure_directories():
    """Create required directories if they don't exist."""
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

def setup_logging():
    """Setup logging configuration with both file and console handlers."""
    ensure_directories()  # Make sure logs/ exists

    log_file = os.path.join(LOG_DIR, "price_pulse_tracker_logs.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(PROJECT_NAME)
