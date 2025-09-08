import json
import os
from src.scrapper import scrape_e_commerce_product
from datetime import datetime
from src.utils.config import setup_logging, TRACKED_FILE

logger = setup_logging()

def load_tracked_products():
    if os.path.exists(TRACKED_FILE):
        with open(TRACKED_FILE, 'r') as f:
            logger.info(f"Tracked file loaded.")
            return json.load(f)
    return {} # if missing or no products in tracked file

def save_tracked_products(products):
    with open(TRACKED_FILE, 'w') as f:
        json.dump(products, f, indent=2)
        logger.info(f"Tracked file saved.")

def is_duplicate_entry(history, new_entry):
    """
    Checks whether the new price entry is a duplicate of the last recorded entry.

    A duplicate is defined as:
      - The last entry in `history` has the same price as `new_entry`, AND
      - Both entries were recorded on the same day (date matches, regardless of time)

    Parameters:
        history (list): A list of previous entries (each entry is a dict with 'price' and 'date' keys).
        new_entry (dict): A dictionary representing the new entry to be checked.

    Returns:
        bool: True if the new entry is a duplicate of the last one (same price and date), False otherwise.
    """
    if not history:
        return False
    last_entry = history[-1]
    same_price = last_entry['price'] == new_entry['price']
    same_date = last_entry['date'].split("T")[0] == datetime.now().date().isoformat()
    return same_price and same_date


def track_product(url: str, threshold_price: float | int):
    """
    Tracks a product's price from the given URL and determines if an alert should be triggered.

    The function performs the following steps:
        1. Loads previously tracked product data from a JSON file.
        2. Initializes tracking if the product is new.
        3. Scrapes the latest product data (title, price).
        4. Cleans and converts the price to float.
        5. Records the price and date if it's not a duplicate of the last entry.
        6. Saves the updated tracking history.
        7. Compares the price with the user-defined threshold to decide if an alert should be sent.

    Parameters:
        url (str): The URL of the product to be tracked.
        threshold_price (float/int): The price below which an alert should be triggered.

    Returns:
        tuple:
            - (bool): True if the current price is less than or equal to the threshold, otherwise False.
            - (dict or None): The latest product data (title, price, date) if available, else None.
    """
    
    products = load_tracked_products()

    if url not in products:
        products[url] = {
            "threshold": threshold_price,
            "history": []
        }
    
    try:
        current_data = scrape_e_commerce_product(url)

        if current_data and 'price' in current_data and 'title' in current_data:
            try:
                current_data['price'] = float(str(current_data['price']).replace(",", "").replace("$", "").strip())
            except ValueError:
                logger.error(f"Failed to convert price to float: {current_data['price']}")
                return False, None
            
            current_data['date'] = datetime.now().isoformat()
            history = products[url]["history"]
        
            # Avoid duplicate entries
            if not is_duplicate_entry(history, current_data):
                history.append(current_data)
                save_tracked_products(products)
                logger.info(f"Tracked: {current_data['title']} | ${current_data['price']}")

            if current_data['price'] <= threshold_price:
                return True, current_data
            else:
                return False, current_data
        else:
            logger.info(f"Failed to fetch complete data for {url}")
            return False, None

    except Exception as e:
        logger.error(f"Error tracking {url}: {str(e)}")
        return False, None
    
    
def track_all_products():
    """
    Tracks all products currently being monitored and prints their latest price status.

    This function:
        1. Loads the list of all tracked products from storage.
        2. Iterates over each product URL and:
            - Scrapes current price and title.
            - Logs the latest price and threshold.
            - Checks if the current price is below the defined threshold.
            - Prints an alert if the price has dropped.

    Prints status messages for each product, including:
        - Product title
        - Current price
        - Threshold price
        - Alert message (if applicable)
        - Error message if scraping fails

    Returns:
        None
    """
    products = load_tracked_products()

    if not products:
        print("No products to track. Add a product first.")
        return
    
    for url, info in products.items():
        threshold = info['threshold']
        alert_triggered, product_data  = track_product(url, threshold)

        if product_data:
            print(f"Checked: {product_data['title']}")
            print(f"Current Price: ${product_data['price']}")
            print(f"Threshold:     ${threshold}")
            if alert_triggered:
                print(f"ALERT: Price dropped below threshold!\n")
        else:
            print(f"Failed to fetch data for {url}\n")
