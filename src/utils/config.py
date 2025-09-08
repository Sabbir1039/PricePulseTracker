import os
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Project metadata
PROJECT_NAME = "PricePulseTracker"
VERSION = "1.0.0"

# Env vars
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", 1))

# Directories (always at project root)
BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
TRACKED_FILE = DATA_DIR / "tracked_products.json"
TRACKED_CSV_FILE = DATA_DIR / "tracked_products_CSV.csv"

def ensure_directories():
    LOG_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

def setup_logging():
    ensure_directories()
    log_file = LOG_DIR / "price_pulse_tracker_logs.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(PROJECT_NAME)
