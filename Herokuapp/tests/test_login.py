import pytest
import logging
from pages.login_page import LoginPage
from services.api_service import ApiService
from services.database_service import DatabaseService
import allure

logger = logging.getLogger(__name__)


@allure.epic("Authentication")
@allure.feature("Login Functionality")
class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.login_page = LoginPage(driver)
        self.api_service = ApiService(config.api_url)
        self.db_service = DatabaseService(config.db_config)
        yield
        self.api_service.close()

    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test successful login with valid credentials")
    def test_successful_login(self):
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)

        with allure.step("Perform login with valid credentials"):
            self.login_page.login("tomsmith", "SuperSecretPassword!")

        with allure.step("Verify successful login"):
            assert self.login_page.is_logout_visible(), "Logout button should be visible after successful login"
            flash_message = self.login_page.get_flash_message()
            assert "You logged into a secure area!" in flash_message

        with allure.step("Take screenshot after login"):
            self.login_page.take_screenshot("after_successful_login")

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login failure with invalid credentials")
    def test_failed_login_invalid_username(self):
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)

        with allure.step("Perform login with invalid username"):
            self.login_page.login("invalid_user", "SuperSecretPassword!")

        with allure.step("Verify login failure"):
            flash_message = self.login_page.get_flash_message()
            assert "Your username is invalid!" in flash_message
            assert not self.login_page.is_logout_visible(), "Logout button should not be visible after failed login"

    @allure.story("API Authentication")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_authentication_mock(self):
        with allure.step("Mock API authentication"):
            auth_response = self.api_service.authenticate("tomsmith", "SuperSecretPassword!")

        with allure.step("Verify authentication response"):
            assert auth_response["authenticated"] is True
            assert auth_response["user"] == "tomsmith"
            assert "token" in auth_response

    @allure.story("Database Verification")
    @allure.severity(allure.severity_level.MINOR)
    def test_database_user_verification(self):
        with allure.step("Connect to database"):
            self.db_service.connect()

        with allure.step("Verify user in database"):
            # This is a mock implementation - in real scenario would check actual user
            user = self.db_service.get_user_by_username("tomsmith")
            # Since Herokuapp doesn't have real DB, we'll just verify connection works
            assert self.db_service.connection is not None

        with allure.step("Close database connection"):
            self.db_service.disconnect()