from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure
from utils.log_decorators import log_page_interaction, log_function_call


class LoginPage(BasePage):
    # Corrected locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button.secondary.radius")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.logger.debug("LoginPage initialized")

    @allure.step("Navigate to login page")
    @log_page_interaction("Navigate to login page")
    def navigate_to_login(self, base_url: str) -> None:
        """Navigate to login page"""
        self.driver.get(f"{base_url}/login")
        self.wait_for_page_to_load()
        self.logger.info(f"Navigated to login page: {base_url}/login")

    @allure.step("Enter username")
    #@allure.step("Enter username: {username}")
    @log_page_interaction("Enter username")
    def enter_username(self, username: str) -> None:
        """Enter username"""
        print(f"Username in start:{username}")
        username_field = self.wait_for_element(self.USERNAME_FIELD)
        username_field.clear()
        username_field.send_keys(username)
        self.logger.debug(f"Entered username: {username}")
        print(f"Username in finish:{username}")

    @allure.step("Enter password")
    @log_page_interaction("Enter password")
    def enter_password(self, password: str) -> None:
        """Enter password"""
        password_field = self.wait_for_element(self.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)
        self.logger.debug("Entered password")

    @allure.step("Click login button")
    @log_page_interaction("Click login button")
    def click_login(self) -> None:
        """Click login button"""
        self.click_with_retry(self.LOGIN_BUTTON)
        self.wait_for_page_to_load()
        self.logger.info("Clicked login button")

    @allure.step("Perform login")
    @log_page_interaction("Complete login")
    def login(self, username: str, password: str) -> None:
        """Complete login flow"""
        self.logger.info(f"Attempting login for user: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    @allure.step("Get flash message")
    @log_function_call(log_result=True)
    def get_flash_message(self) -> str:
        """Get flash message text"""
        message = self.get_element_text(self.FLASH_MESSAGE)
        self.logger.debug(f"Flash message: {message}")
        return message

    @allure.step("Check if logout button is visible")
    @log_function_call(log_result=True)
    def is_logout_visible(self) -> bool:
        """Check if logout button is visible (indicates successful login)"""
        is_visible = self.is_element_present(self.LOGOUT_BUTTON)
        self.logger.debug(f"Logout button visible: {is_visible}")
        return is_visible

    @allure.step("Logout from application")
    @log_page_interaction("Logout")
    def logout(self) -> None:
        """Logout from application"""
        self.click_with_retry(self.LOGOUT_BUTTON)
        self.wait_for_page_to_load()
        self.logger.info("User logged out")

    @allure.step("Check if on login page")
    @log_function_call(log_result=True)
    def is_on_login_page(self) -> bool:
        """Check if currently on login page"""
        try:
            return self.is_element_present(self.USERNAME_FIELD) and self.is_element_present(self.PASSWORD_FIELD)
        except:
            return False