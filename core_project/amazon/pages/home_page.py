import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../core'))

from selenium.webdriver.common.by import By
from core_project.core.base.base_page import BasePage
import allure
from core_project.core.utils.log_decorators import log_page_interaction, log_function_call


class HomePage(BasePage):
    """Amazon homepage with search functionality"""

    # Locators
    SEARCH_BOX = (By.ID, "twotabsearchtextbox")
    SEARCH_BUTTON = (By.ID, "nav-search-submit-button")
    CART_COUNT = (By.ID, "nav-cart-count")
    ACCEPT_COOKIES = (By.ID, "sp-cc-accept")
    DELIVERY_LOCATION = (By.ID, "nav-global-location-popover-link")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.debug("Amazon HomePage initialized")

    @allure.step("Navigate to Amazon homepage")
    @log_page_interaction("Navigate to Amazon homepage")
    def navigate_to_homepage(self, base_url: str) -> bool:
        """Navigate to Amazon homepage"""
        try:
            self.driver.get(base_url)
            self.wait_for_page_to_load()
            self.logger.info(f"Navigated to Amazon homepage: {base_url}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to Amazon homepage: {e}")
            return False

    @allure.step("Accept cookies if present")
    def accept_cookies_if_present(self) -> bool:
        """Accept cookies if the dialog is present"""
        try:
            if self.is_element_present(self.ACCEPT_COOKIES, timeout=5):
                self.safe_click(self.ACCEPT_COOKIES)
                self.logger.info("Amazon cookies accepted")
                return True
        except Exception as e:
            self.logger.debug(f"Cookie acceptance not required or failed: {e}")
        return False

    @allure.step("Search for product: {search_term}")
    @log_page_interaction("Search for product")
    def search_for_product(self, search_term: str) -> bool:
        """Search for a product on Amazon"""
        try:
            self.type_text(self.SEARCH_BOX, search_term)
            self.safe_click(self.SEARCH_BUTTON)
            self.wait_for_page_to_load()
            self.logger.info(f"Searched for: {search_term}")
            return True
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return False

    @allure.step("Get cart items count")
    @log_function_call(log_result=True)
    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        try:
            count_text = self.get_element_text(self.CART_COUNT)
            return int(count_text) if count_text else 0
        except Exception as e:
            self.logger.debug(f"Could not get cart count: {e}")
            return 0

    @allure.step("Open shopping cart")
    @log_page_interaction("Open shopping cart")
    def open_cart(self) -> bool:
        """Open shopping cart"""
        try:
            self.safe_click(self.CART_COUNT)
            self.wait_for_page_to_load()
            self.logger.info("Opened shopping cart")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open cart: {e}")
            return False