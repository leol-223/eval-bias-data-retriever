from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def get_cookies(homepage_url):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome()#options=options)
    
    cookies = []
    try:
        driver.get(homepage_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        time.sleep(20)

        cookies = driver.get_cookies()
        
    except Exception as e:
        print(f"An error occurred with Selenium: {e}")
    finally:
        driver.quit()
        
    return cookies