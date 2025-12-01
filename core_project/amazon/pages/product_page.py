import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../core'))

from selenium.webdriver.common.by import By
from core_project.core.base.base_page import BasePage
import allure
import time
from core_project.core.utils.log_decorators import log_page_interaction, log_function_call


class ProductPage(BasePage):
    """Amazon product page with add to cart functionality"""

    # Locators
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-button")
    BUY_NOW_BUTTON = (By.ID, "buy-now-button")
    PRODUCT_TITLE = (By.ID, "productTitle")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".a-price-whole")
    CART_COUNT = (By.ID, "nav-cart-count")
    CART_SIDESHEET = (By.ID, "attach-sidesheet-view-cart-button")
    NO_THANKS_BUTTON = (By.ID, "attachSiNoCoverage")
    PROCEED_TO_CHECKOUT = (By.NAME, "proceedToRetailCheckout")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.debug("Amazon ProductPage initialized")

    @allure.step("Get product title")
    @log_function_call(log_result=True)
    def get_product_title(self) -> str:
        """Get product title"""
        try:
            return self.get_element_text(self.PRODUCT_TITLE)
        except Exception as e:
            self.logger.error(f"Could not get product title: {e}")
            return "Unknown Product"

    @allure.step("Get product price")
    @log_function_call(log_result=True)
    def get_product_price(self) -> str:
        """Get product price"""
        try:
            return self.get_element_text(self.PRODUCT_PRICE)
        except Exception as e:
            self.logger.debug(f"Could not get product price: {e}")
            return "Price not available"

    @allure.step("Add product to cart")
    @log_page_interaction("Add to cart")
    def add_to_cart(self) -> bool:
        """Add product to shopping cart"""
        try:
            # Scroll to add to cart button
            self.scroll_to_element(self.ADD_TO_CART_BUTTON)
            time.sleep(2)

            # Click add to cart
            if self.safe_click(self.ADD_TO_CART_BUTTON):
                self.logger.info("Clicked add to cart button")

                # Handle additional offers popup
                self._handle_popups()

                # Wait for cart to update
                time.sleep(3)
                return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to add product to cart: {e}")
            return False

    @allure.step("Handle popups and additional offers")
    def _handle_popups(self) -> bool:
        """Handle various popups that may appear after adding to cart"""
        try:
            # Handle "No thanks" for additional coverage
            if self.is_element_present(self.NO_THANKS_BUTTON, timeout=5):
                self.safe_click(self.NO_THANKS_BUTTON)
                self.logger.info("Declined additional coverage")
                time.sleep(2)
            return True
        except Exception as e:
            self.logger.debug(f"No popup to handle or handling failed: {e}")
            return False

    @allure.step("Proceed to cart")
    @log_page_interaction("Proceed to cart")
    def proceed_to_cart(self) -> bool:
        """Proceed to cart after adding product"""
        try:
            # Try to click cart sidesheet if present
            if self.is_element_present(self.CART_SIDESHEET, timeout=5):
                self.safe_click(self.CART_SIDESHEET)
            else:
                # Fallback to navigation cart
                from core_project.amazon.pages.home_page import HomePage
                home_page = HomePage(self.driver)
                home_page.open_cart()

            self.wait_for_page_to_load()
            self.logger.info("Navigated to cart")
            return True

        except Exception as e:
            self.logger.error(f"Failed to proceed to cart: {e}")
            return False

    @allure.step("Get cart items count")
    @log_function_call(log_result=True)
    def get_cart_count(self) -> int:
        """Get number of items in cart"""
        try:
            from core_project.amazon.pages.home_page import HomePage
            home_page = HomePage(self.driver)
            return home_page.get_cart_items_count()
        except Exception as e:
            self.logger.warning(f"Could not get cart count: {e}")
            return 0