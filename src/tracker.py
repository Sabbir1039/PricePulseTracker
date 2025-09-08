import json
import os
from src.scrapper import scrape_e_commerce_product
from datetime import datetime
from src.utils.config import setup_logging, TRACKED_FILE

logger = setup_logging()

def load_tracked_products():
    """
    Load the tracked products from the JSON file.

    Returns:
        dict: Dictionary containing tracked products and their history.
              Format:
              {
                "<url>": {
                  "threshold": float,
                  "history": [ { "title": str, "price": float, "date": str }, ... ]
                },
                ...
              }
    """
    if os.path.exists(TRACKED_FILE):
        with open(TRACKED_FILE, 'r', encoding="utf-8") as f:
            logger.info(f"Tracked file loaded.")
            return json.load(f)
    return {} # if missing then returns {} empty dict


def save_tracked_products(products: dict[str, any]) -> None:
    """
    Save tracked products dictionary back to JSON file.

    Args:
        products (dict): Dictionary of tracked products.
    """
    with open(TRACKED_FILE, 'w') as f:
        json.dump(products, f, indent=2)
        logger.info(f"Tracked file saved.")


def is_duplicate_entry(history: list, new_entry: dict) -> bool:
    """
    Check if a new entry is a duplicate of the last recorded entry.

    A duplicate is defined as:
        - Last entry has the same price as the new entry, AND
        - Both entries were recorded on the same day.

    Args:
        history (list): Previous entries for a product.
        new_entry (dict): New entry with 'price' and 'date'.

    Returns:
        bool: True if duplicate, False otherwise.
    """
    if not history:
        return False
    last_entry = history[-1]
    same_price = last_entry['price'] == new_entry['price']

    # Parse timestamps
    last_dt = datetime.fromisoformat(last_entry['date'])
    new_dt = datetime.fromisoformat(new_entry['date'])

    # Check same year, month, day, and hour
    same_hour = (
        last_dt.year == new_dt.year
        and last_dt.month == new_dt.month
        and last_dt.day == new_dt.day
        and last_dt.hour == new_dt.hour
    )

    return same_price and same_hour

def clean_price(raw_price: str) -> float | None:
    """
    Convert raw scraped price string into float.

    Args:
        raw_price (str): Price string (e.g., "$1,299.99").

    Returns:
        float: Cleaned price or None if conversion fails.
    """
    try:
        return float(str(raw_price).replace(",", "").replace("$", "").strip())
    except ValueError:
        logger.error(f"Failed to convert price to float: {raw_price}")
        return None


def track_product(url: str, threshold_price: float | int) -> tuple[bool, dict | None]:
    """
    Track a product price from a given URL and decide if alert is needed.

    Steps:
        1. Load existing tracked products.
        2. Initialize entry if product is new.
        3. Scrape current product info (title, price).
        4. Clean price and add timestamp.
        5. Avoid duplicate entries.
        6. Save updated history.
        7. Check against threshold.

    Args:
        url (str): Product URL.
        threshold_price (float|int): Alert threshold price.

    Returns:
        tuple:
            (bool, dict|None):
              - bool: True if current price <= threshold.
              - dict: Latest product data (title, price, date).
    """
    
    products = load_tracked_products()

    # Ensure product entry exists
    if url not in products:
        products[url] = {
            "threshold": threshold_price,
            "history": []
        }
    
    try:
        # Scrape current data
        current_data = scrape_e_commerce_product(url)
        if not current_data or "price" not in current_data or "title" not in current_data:
            logger.warning(f"Incomplete data scraped for {url}")
            return False, None
        
        # Clean price
        current_data["price"] = clean_price(current_data["price"])
        if current_data["price"] is None:
            return False, None
        
        # Add timestamp
        current_data["date"] = datetime.now().isoformat()
        history = products[url]["history"] 
        
        # Append only if not duplicate
        if not is_duplicate_entry(history, current_data):
            history.append(current_data)
            save_tracked_products(products)
            logger.info(f"Tracked: {current_data['title']} | ${current_data['price']}")

        # Check threshold
        alert_needed = current_data["price"] <= threshold_price
        return alert_needed, current_data
    
    except Exception as e:
        logger.error(f"Error tracking {url}: {str(e)}")
        return False, None
