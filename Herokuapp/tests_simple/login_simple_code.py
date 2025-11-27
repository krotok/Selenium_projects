import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_login():
    # In new Selenium versions we can use installed Chrome instead of driver.
    driver = webdriver.Chrome()

    try:
        print("Open page...")
        driver.get("https://the-internet.herokuapp.com/login")

        # Find elements
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        # Input data
        username.send_keys("tomsmith")
        password.send_keys("SuperSecretPassword!")
        btn.click()

        # Check result
        assert "/secure" in driver.current_url
        print("Success test!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_login()