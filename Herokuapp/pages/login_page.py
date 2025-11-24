from selenium.webdriver.common.by import By
from .base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button.secondary.radius")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_login(self, base_url: str) -> None:
        """Navigate to login page"""
        self.driver.get(f"{base_url}/login")
        logger.info("Navigated to login page")

    def enter_username(self, username: str) -> None:
        """Enter username"""
        username_field = self.wait_for_element(self.USERNAME_INPUT)
        username_field.clear()
        username_field.send_keys(username)
        logger.debug(f"Entered username: {username}")

    def enter_password(self, password: str) -> None:
        """Enter password"""
        password_field = self.wait_for_element(self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        logger.debug("Entered password")

    def click_login(self) -> None:
        """Click login button"""
        self.click_with_retry(self.LOGIN_BUTTON)
        logger.info("Clicked login button")

    def login(self, username: str, password: str) -> None:
        """Complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_flash_message(self) -> str:
        """Get flash message text"""
        return self.get_element_text(self.FLASH_MESSAGE)

    def is_logout_visible(self) -> bool:
        """Check if logout button is visible (indicates successful login)"""
        return self.is_element_present(self.LOGOUT_BUTTON)

    def logout(self) -> None:
        """Logout from application"""
        self.click_with_retry(self.LOGOUT_BUTTON)
        logger.info("User logged out")