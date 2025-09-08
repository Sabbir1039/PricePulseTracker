import time
import schedule
from src.utils.config import ensure_directories, setup_logging, TRACKED_FILE, TRACKED_CSV_FILE
from src.utils.export_to_csv import export_to_csv
from src.tracker import track_product
from src.notifier import send_email_alert


# Define products to track
TEST_PRODUCTS = {
    "product1": {
        "url": "https://www.amazon.com/dp/B0CPLB9NHR/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0CPLB9NHR&pd_rd_w=umx8L&content-id=amzn1.sym.7446a9d1-25fe-4460-b135-a60336bad2c9&pf_rd_p=7446a9d1-25fe-4460-b135-a60336bad2c9&pf_rd_r=5FFEBN4SEAV7MKEA54N3&pd_rd_wg=HqK4K&pd_rd_r=0e90c4bd-ed74-47ef-b774-fa2aaffa4ab1&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw",
        "threshold": 40
    },
    "product2": {
        "url": "https://www.amazon.com/Nintendo-Switch-OLED-Model-White-Joy/dp/B098RKWHHZ/ref=sr_1_2?dib=eyJ2IjoiMSJ9.SnJwwaQgWAAz2ipQdcQ--ww0mUwm9OAXePgwWaeU0beIFh8x7x3Ztf6rw5W-PIowGJUhbZ22Tt1wRmzEGDdO0zvQkuBHzrzFlfF37ed4Foa_QA13u9ETMBZOgPu4gFm8r77xf-7L-QaoNSAw9NhY4S1vTzSVaRFjkEBxasLEy9v963b8TWmJGW-4F7csqbKuZ-NuL6O1FWVqCBwCDtyC1k_lWO77w46cUQpG5vEv9CI.LkDPeQMJVU_765kRkUMPKfSH5BeRLnFjlNttYheNDV4&dib_tag=se&keywords=nintendo%2Bswitch%2B2&qid=1752433182&sr=8-2&th=1",
        "threshold": 400
    }
}


def track_all_products(products: dict, logger):
    """
    Run price tracking for all products and send alerts if needed.
    
    Args:
        products (dict): Mapping of product name -> {url, threshold}.
        logger (Logger): Logger instance.
    """
    for name, info in products.items():
        should_alert, product_data = track_product(
            url=info["url"], threshold_price=info["threshold"]
        )

        if product_data:
            logger.info(f"[{name}] Title: {product_data['title']} | Price: {product_data['price']}")

        if should_alert:
            send_email_alert(product_data, info["threshold"])
            logger.info(f"ALERT sent for {name} (below threshold {info['threshold']})")

    # Export JSON history to CSV
    export_to_csv(TRACKED_FILE, TRACKED_CSV_FILE)
    logger.info("Tracked JSON file exported to CSV.")


def job(products, logger):
    """Wrapper for scheduled job."""
    track_all_products(products, logger)


def run_scheduler(products: dict):
    """
    Start the scheduler to track products at a fixed interval.
    """
    ensure_directories()
    logger = setup_logging()
    logger.info("Starting PricePulseTracker...")

    # Schedule hourly
    schedule.every().hour.do(job, products, logger)

    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # check every 30s if a job is due
    except KeyboardInterrupt:
        logger.warning(f"Script closed by keyboard interruption!")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        
    finally:
        logger.info("Cleaning up scheduler...")
        schedule.clear()


if __name__ == "__main__":
    run_scheduler(TEST_PRODUCTS)
