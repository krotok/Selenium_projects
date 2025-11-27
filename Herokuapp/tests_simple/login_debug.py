import pytest
from config.init import Config
from pages.login_page import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def test_debug_config():
    """Debug configuration loading"""
    print("\n=== DEBUG CONFIG ===")

    # Test config loading
    config = Config("dev")
    print(f"Config type: {type(config)}")
    print(f"Config environment: {config.environment}")
    print(f"Config data keys: {list(config.config_data.keys())}")
    print(f"Base URL: {config.base_url}")
    print(f"Config object dir: {[attr for attr in dir(config) if not attr.startswith('_')]}")

    # Test accessing non-existent key
    try:
        username = config.get('username')
        print(f"Username from config: {username}")
    except Exception as e:
        print(f"Error getting username: {e}")

    assert True


def test_debug_login_page():
    """Debug login page initialization"""
    print("\n=== DEBUG LOGIN PAGE ===")

    # Setup minimal driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        config = Config("dev")
        login_page = LoginPage(driver)

        print(f"LoginPage type: {type(login_page)}")
        print(f"LoginPage attributes: {[attr for attr in dir(login_page) if not attr.startswith('_')]}")
        print(f"USERNAME_FIELD: {login_page.USERNAME_FIELD}")
        print(f"PASSWORD_FIELD: {login_page.PASSWORD_FIELD}")

        # Test navigation
        login_page.navigate_to_login(config.base_url)
        print("Navigation successful")

        # Test element presence
        is_username_present = login_page.is_element_present(login_page.USERNAME_FIELD)
        is_password_present = login_page.is_element_present(login_page.PASSWORD_FIELD)
        print(f"Username field present: {is_username_present}")
        print(f"Password field present: {is_password_present}")

        # Test individual methods
        print("Testing enter_username...")
        login_page.enter_username("tomsmith")
        print("enter_username completed")

        print("Testing enter_password...")
        login_page.enter_password("SuperSecretPassword!")
        print("enter_password completed")

        print("Testing click_login...")
        login_page.click_login()
        print("click_login completed")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()


def test_debug_traceback():
    """Get full traceback for the error"""
    print("\n=== DEBUG TRACEBACK ===")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    config = Config("dev")
    login_page = LoginPage(driver)

    try:
        login_page.navigate_to_login(config.base_url)

        # This should trigger the error
        login_page.login("tomsmith", "SuperSecretPassword!")

    except Exception as e:
        print(f"EXCEPTION TYPE: {type(e)}")
        print(f"EXCEPTION MESSAGE: {e}")
        print("FULL TRACEBACK:")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()