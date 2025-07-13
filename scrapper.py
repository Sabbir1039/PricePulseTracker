import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_e_commerce_product(url):
    options = Options()
    service = Service(ChromeDriverManager().install())
    options.add_argument("--headless=new")         # Headless mode (Chrome 109+)
    driver = webdriver.Chrome(options=options, service=service)

    try:
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

        return {
            'title' : title,
            'price' : price,
            'url' : url
        }


    except Exception as e:
        print(f"Error scrapping {url}: {e}")
        return None
    
    finally:
        driver.quit()
        print("driver closed")

if __name__ == '__main__':
    product_url = "sabbir.ecommerce.com/products?id=1/"
    product_data = scrape_e_commerce_product(product_url)
    
    for key, value in product_data.items():
        print(f"{key} : {value}")