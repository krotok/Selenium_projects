import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../core'))

from selenium.webdriver.common.by import By
from core_project.core.pages.common_components import LoginPage as CoreLoginPage
import allure
from core_project.core.utils.log_decorators import log_page_interaction, log_function_call


class LoginPage(CoreLoginPage):
    """Herokuapp specific login page extending core login functionality"""

    # Herokuapp specific locators
    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button.secondary.radius")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.debug("Herokuapp LoginPage initialized")

    @allure.step("Navigate to login page")
    @log_page_interaction("Navigate to login page")
    def navigate_to_login(self, base_url: str) -> None:
        """Navigate to Herokuapp login page"""
        self.driver.get(f"{base_url}/login")
        self.wait_for_page_to_load()
        self.logger.info(f"Navigated to Herokuapp login page: {base_url}/login")

    @allure.step("Get flash message")
    @log_function_call(log_result=True)
    def get_flash_message(self) -> str:
        """Get Herokuapp specific flash message"""
        message = self.get_element_text(self.FLASH_MESSAGE)
        self.logger.debug(f"Flash message: {message}")
        return message

    @allure.step("Check if logout button is visible")
    @log_function_call(log_result=True)
    def is_logout_visible(self) -> bool:
        """Check if logout button is visible (Herokuapp specific)"""
        is_visible = self.is_element_present(self.LOGOUT_BUTTON)
        self.logger.debug(f"Logout button visible: {is_visible}")
        return is_visible

    @allure.step("Verify logout button is not present")
    @log_function_call(log_result=True)
    def is_logout_not_present(self) -> bool:
        """Verify that logout button is not present on page"""
        try:
            return not self.is_element_present(self.LOGOUT_BUTTON, timeout=2)
        except Exception as e:
            self.logger.debug(f"Error checking logout absence: {e}")
            return True  # If error the element doesn't present

    @allure.step("Check if on login page")
    @log_function_call(log_result=True)
    def is_on_login_page(self) -> bool:
        """Check if currently on Herokuapp login page"""
        try:
            return self.is_element_present(self.USERNAME_FIELD) and self.is_element_present(self.PASSWORD_FIELD)
        except:
            return False

    @allure.step("Logout from application")
    @log_page_interaction("Logout")
    def logout(self) -> None:
        """Logout from Herokuapp application"""
        if self.is_element_present(self.LOGOUT_BUTTON):
            self.safe_click(self.LOGOUT_BUTTON)
            self.wait_for_page_to_load()
            self.logger.info("User logged out from Herokuapp")