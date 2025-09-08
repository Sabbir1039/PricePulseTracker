from tracker import track_all_products, track_product
from export_to_csv import export_to_csv
from notifier import send_email_alert

if __name__ == "__main__":
    """
    Here i can use 2 methods
    1. track_all_products (for previous multiple products)
    2. track_product (for given new product)
    Also can add timer for track product price
    """
    # Track given products using track_product()
    test_products = {
        "product1": {
            "url": "https://www.amazon.com/dp/B0CPLB9NHR/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0CPLB9NHR&pd_rd_w=umx8L&content-id=amzn1.sym.7446a9d1-25fe-4460-b135-a60336bad2c9&pf_rd_p=7446a9d1-25fe-4460-b135-a60336bad2c9&pf_rd_r=5FFEBN4SEAV7MKEA54N3&pd_rd_wg=HqK4K&pd_rd_r=0e90c4bd-ed74-47ef-b774-fa2aaffa4ab1&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw",
            "threshold": 40
        },
        "product2": {
            "url": "https://www.amazon.com/Nintendo-Switch-OLED-Model-White-Joy/dp/B098RKWHHZ/ref=sr_1_2?dib=eyJ2IjoiMSJ9.SnJwwaQgWAAz2ipQdcQ--ww0mUwm9OAXePgwWaeU0beIFh8x7x3Ztf6rw5W-PIowGJUhbZ22Tt1wRmzEGDdO0zvQkuBHzrzFlfF37ed4Foa_QA13u9ETMBZOgPu4gFm8r77xf-7L-QaoNSAw9NhY4S1vTzSVaRFjkEBxasLEy9v963b8TWmJGW-4F7csqbKuZ-NuL6O1FWVqCBwCDtyC1k_lWO77w46cUQpG5vEv9CI.LkDPeQMJVU_765kRkUMPKfSH5BeRLnFjlNttYheNDV4&dib_tag=se&keywords=nintendo%2Bswitch%2B2&qid=1752433182&sr=8-2&th=1",
            "threshold": 400
        }
    }

    for product, info in test_products.items():
        should_alert, product_data = track_product(url=info["url"], threshold_price=info["threshold"])

        if should_alert:
            send_email_alert(product_data, info["threshold"])

    # TRACKED_PRODUCT = "tracked_products.json"
    # SAVED_FILE = "exported_products_data.csv"
    # export_to_csv(TRACKED_PRODUCT, SAVED_FILE)