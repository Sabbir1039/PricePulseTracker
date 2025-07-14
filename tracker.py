import json
import os
from scrapper import scrape_e_commerce_product
from datetime import datetime

TRACKED_FILE = "tracked_products.json"
LOG_FILE = "tracker_log.txt"

def load_tracked_products():
    if os.path.exists(TRACKED_FILE):
        with open(TRACKED_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tracked_products(products):
    with open(TRACKED_FILE, 'w') as f:
        json.dump(products, f, indent=2)

def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {message}\n")

def is_duplicate_entry(history, new_entry):
    if not history:
        return False
    last_entry = history[-1]
    same_price = last_entry['price'] == new_entry['price']
    same_date = last_entry['date'].split("T")[0] == datetime.now().date().isoformat()
    return same_price and same_date


def track_product(url, threshold_price):
    """
    This function tracks a single product:
    1.It checks if the product is already tracked.
    2.Scrapes the current price.
    3.Saves the data (with date) in tracked_products.json.
    4.Checks if the price has dropped below the user-defined threshold price.
    5.Returns whether an alert should be triggered, and the product data.
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
                log_message(f"Failed to convert price to float: {current_data['price']}")
                return False, None
            
            current_data['date'] = datetime.now().isoformat()
            history = products[url]["history"]
        
            # Avoid duplicate entries
            if not is_duplicate_entry(history, current_data):
                history.append(current_data)
                save_tracked_products(products)
                log_message(f"Tracked: {current_data['title']} | ${current_data['price']}")

            if current_data['price'] <= threshold_price:
                return True, current_data
            else:
                return False, current_data
        else:
            log_message(f"Failed to fetch complete data for {url}")
            return False, None

    except Exception as e:
        log_message(f"Error tracking {url}: {str(e)}")
        return False, None
    
    
def track_all_products():
    products = load_tracked_products()

    if not products:
        print("No products to track. Add a product first.")
        return
    
    for url, info in products.items():
        threshold = info['threshold']
        alert_triggered, product_data  = track_product(url, threshold)

        if product_data:
            print(f"Checked: {product_data['title']}")
            print(f"  🏷 Current Price: ${product_data['price']}")
            print(f"  🎯 Threshold:     ${threshold}")
            if alert_triggered:
                print(f"  🚨 ALERT: Price dropped below threshold!\n")
        else:
            print(f"❌ Failed to fetch data for {url}\n")

if __name__ == "__main__":
    # product_url = ""
    # threshold = 400.00
    # price_lowered, product = track_product(product_url, threshold)
    # track_all_products()
    pass