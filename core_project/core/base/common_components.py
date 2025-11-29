from selenium.webdriver.common.by import By
from core_project.core.base.base_page import BasePage
import allure


class HeaderComponent(BasePage):
    """Common header component that can be used across different sites"""

    # Common header locators
    LOGO = (By.CLASS_NAME, "logo")
    SEARCH_BOX = (By.NAME, "q")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CART_ICON = (By.CLASS_NAME, "cart")
    USER_MENU = (By.CLASS_NAME, "user-menu")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Search for product")
    def search_product(self, search_term: str) -> None:
        """Search for a product using header search"""
        if self.is_element_present(self.SEARCH_BOX):
            self.type_text(self.SEARCH_BOX, search_term)
            self.safe_click(self.SEARCH_BUTTON)
            self.logger.info(f"Searched for: {search_term}")

    @allure.step("Navigate to login page")
    def go_to_login(self) -> None:
        """Navigate to login page via header"""
        if self.is_element_present(self.LOGIN_LINK):
            self.safe_click(self.LOGIN_LINK)
            self.wait_for_page_to_load()
            self.logger.info("Navigated to login page")

    @allure.step("Logout user")
    def logout(self) -> None:
        """Logout user via header"""
        if self.is_element_present(self.USER_MENU):
            self.safe_click(self.USER_MENU)
            if self.is_element_present(self.LOGOUT_LINK):
                self.safe_click(self.LOGOUT_LINK)
                self.wait_for_page_to_load()
                self.logger.info("User logged out")


class FooterComponent(BasePage):
    """Common footer component"""

    FOOTER_LINKS = (By.CSS_SELECTOR, "footer a")
    COPYRIGHT_TEXT = (By.CSS_SELECTOR, "footer .copyright")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Get footer links count")
    def get_footer_links_count(self) -> int:
        """Get number of links in footer"""
        links = self.driver.find_elements(*self.FOOTER_LINKS)
        return len(links)


class LoginPage(BasePage):
    """Common login page functionality that can be extended"""

    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Enter username")
    def enter_username(self, username: str) -> None:
        """Enter username"""
        if self.is_element_present(self.USERNAME_FIELD):
            self.type_text(self.USERNAME_FIELD, username)
            self.logger.debug(f"Entered username: {username}")

    @allure.step("Enter password")
    def enter_password(self, password: str) -> None:
        """Enter password"""
        if self.is_element_present(self.PASSWORD_FIELD):
            self.type_text(self.PASSWORD_FIELD, password)
            self.logger.debug("Entered password")

    @allure.step("Click login button")
    def click_login(self) -> None:
        """Click login button"""
        if self.is_element_present(self.LOGIN_BUTTON):
            self.safe_click(self.LOGIN_BUTTON)
            self.wait_for_page_to_load()
            self.logger.info("Clicked login button")

    @allure.step("Perform login")
    def login(self, username: str, password: str) -> None:
        """Complete login flow"""
        self.logger.info(f"Attempting login for user: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """Get login error message"""
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""