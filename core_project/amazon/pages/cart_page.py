import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../core'))

from selenium.webdriver.common.by import By
from core_project.core.base.base_page import BasePage
import allure
# from core_project.core.utils.log_decorators import log_page_interaction, log_function_call
from core_project.core.utils import log_page_interaction, log_function_call

class CartPage(BasePage):
    """Amazon shopping cart page"""

    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, "[data-itemtype='active']")
    PRODUCT_TITLE_IN_CART = (By.CSS_SELECTOR, ".sc-product-title")
    PRODUCT_PRICE_IN_CART = (By.CSS_SELECTOR, ".sc-product-price")
    SUBTOTAL_PRICE = (By.ID, "sc-subtotal-amount-activecart")
    PROCEED_TO_CHECKOUT_BUTTON = (By.NAME, "proceedToRetailCheckout")
    DELETE_ITEM_BUTTON = (By.CSS_SELECTOR, "input[value='Delete']")
    CART_EMPTY_MESSAGE = (By.XPATH, "//h1[contains(text(), 'Your Amazon Cart is empty')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.debug("Amazon CartPage initialized")

    @allure.step("Get cart items count")
    @log_function_call(log_result=True)
    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        try:
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(items)
        except Exception as e:
            self.logger.warning(f"Could not get cart items count: {e}")
            return 0

    @allure.step("Get product titles from cart")
    @log_function_call(log_result=True)
    def get_product_titles_in_cart(self) -> list:
        """Get product titles from cart"""
        try:
            titles = []
            title_elements = self.driver.find_elements(*self.PRODUCT_TITLE_IN_CART)
            for element in title_elements:
                titles.append(element.text.strip())
            return titles
        except Exception as e:
            self.logger.debug(f"Could not get product titles: {e}")
            return []

    @allure.step("Get cart subtotal")
    @log_function_call(log_result=True)
    def get_subtotal_price(self) -> str:
        """Get cart subtotal price"""
        try:
            return self.get_element_text(self.SUBTOTAL_PRICE)
        except Exception as e:
            self.logger.debug(f"Could not get subtotal: {e}")
            return "Subtotal not available"

    @allure.step("Click proceed to checkout")
    @log_page_interaction("Proceed to checkout")
    def proceed_to_checkout(self) -> bool:
        """Click proceed to checkout button"""
        try:
            if self.safe_click(self.PROCEED_TO_CHECKOUT_BUTTON):
                self.wait_for_page_to_load()
                self.logger.info("Clicked proceed to checkout")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to proceed to checkout: {e}")
            return False

    @allure.step("Verify cart is not empty")
    @log_function_call(log_result=True)
    def verify_cart_not_empty(self) -> bool:
        """Verify that cart is not empty"""
        try:
            return self.get_cart_items_count() > 0 and not self.is_element_present(self.CART_EMPTY_MESSAGE)
        except Exception as e:
            self.logger.warning(f"Error verifying cart: {e}")
            return False

    @allure.step("Remove item from cart")
    @log_page_interaction("Remove item from cart")
    def remove_item_from_cart(self) -> bool:
        """Remove item from cart"""
        try:
            if self.is_element_present(self.DELETE_ITEM_BUTTON):
                self.safe_click(self.DELETE_ITEM_BUTTON)
                self.wait_for_page_to_load()
                self.logger.info("Removed item from cart")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove item: {e}")
            return False