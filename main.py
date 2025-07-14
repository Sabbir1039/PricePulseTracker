from tracker import track_all_products, track_product

if __name__ == "__main__":
    """
    Here i can use 2 methods
    1. track_all_products (for previous products)
    2. track_product (for new product)
    """
    # track_all_products()

    test_url = "https://www.amazon.com/dp/B0CPLB9NHR/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0CPLB9NHR&pd_rd_w=umx8L&content-id=amzn1.sym.7446a9d1-25fe-4460-b135-a60336bad2c9&pf_rd_p=7446a9d1-25fe-4460-b135-a60336bad2c9&pf_rd_r=5FFEBN4SEAV7MKEA54N3&pd_rd_wg=HqK4K&pd_rd_r=0e90c4bd-ed74-47ef-b774-fa2aaffa4ab1&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw"
    test_threshold = 50
    alert, product = track_product(test_url, test_threshold)
    print("*****")
    print(alert)
    print(product)
    print("*****")