from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from typing import TypedDict
from src.utils.config import setup_logging

class ProductData(TypedDict):
    title: str
    price: float | None
    url: str

def scrape_e_commerce_product(url: str) -> ProductData:
    logger = setup_logging()

    options = Options()
    service = Service(ChromeDriverManager().install())
    options.add_argument("--headless=new")           # Headless mode (Chrome 109+)
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options, service=service)

    try:
        logger.info(f"[Scrapper] Started to scrape product data!")
        driver.get(url)
        
        # Wait for the product title or product price to appear (max 15 sec)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price-fraction"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # print(soup.prettify())

        title = soup.find('span', {'id' : 'productTitle'}).get_text().strip()
        whole_price = soup.find('span', {'class' : 'a-price-whole'})
        fraction_price = soup.find('span', {'class' : 'a-price-fraction'})

        if whole_price and fraction_price:
            price = f"{whole_price.get_text(strip=True).replace('.', '')}.{fraction_price.get_text(strip=True)}"
        else:
            price = "Not found"

        logger.info(f"[Scrapper] Successfully scraped product info!")

        return {
            'title' : title,
            'price' : price,
            'url' : url
        }

    except Exception as e:
        logger.warning(f"[Scrapper] Error while scrapping {url}: {e}")
        return None
    
    finally:
        driver.quit()
        logger.info("[Scrapper] Chrome driver closed!")

if __name__ == '__main__':
    product_url =   r"https://www.amazon.com/dp/B0CPLB9NHR/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0CPLB9NHR&pd_rd_w=umx8L&content-id=amzn1.sym.7446a9d1-25fe-4460-b135-a60336bad2c9&pf_rd_p=7446a9d1-25fe-4460-b135-a60336bad2c9&pf_rd_r=5FFEBN4SEAV7MKEA54N3&pd_rd_wg=HqK4K&pd_rd_r=0e90c4bd-ed74-47ef-b774-fa2aaffa4ab1&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw"
    product_data = scrape_e_commerce_product(product_url)
    
    for key, value in product_data.items():
        print(f"{key} : {value}")