import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()

    return driver
    #driver.quit()

def open_page(driver, url):
    driver.get(url)

base_url = "https://amazone.com"

driver = get_driver()
open_page(driver,base_url)
