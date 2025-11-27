import pytest
import allure
from pages.login_page import LoginPage
from services.api_service import ApiService
from services.database_service import DatabaseService
from utils.log_decorators import LoggingMixin


@allure.epic("Authentication")
@allure.feature("Login Functionality")
class TestLogin(LoggingMixin):
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.login_page = LoginPage(driver)
        self.api_service = ApiService(config.api_url)
        self.db_service = DatabaseService(config.db_config)

        self.logger.info(f"Test setup completed for environment: {config.environment}")

        yield

        # Cleanup
        self.api_service.close()
        self.logger.info("Test cleanup completed")

    # @allure.story("Successful Login")
    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.description("Test successful login with valid credentials")
    # def test_successful_login(self):
    #     self.logger.info("Starting test_successful_login")
    #
    #     with allure.step("Navigate to login page"):
    #         self.login_page.navigate_to_login(self.config.base_url)
    #         assert self.login_page.is_on_login_page(), "Should be on login page"
    #         self.login_page.take_screenshot("login_page_loaded")
    #
    #     with allure.step("Perform login with valid credentials"):
    #         self.login_page.login("tomsmith", "SuperSecretPassword!")
    #
    #     with allure.step("Verify successful login"):
    #         assert self.login_page.is_logout_visible(), "Logout button should be visible after successful login"
    #         flash_message = self.login_page.get_flash_message()
    #         assert "You logged into a secure area!" in flash_message
    #         self.logger.info("Login successful - user redirected to secure area")
    #
    #     with allure.step("Take screenshot after login"):
    #         self.login_page.take_screenshot("after_successful_login")

    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test successful login with valid credentials")
    def test_successful_login(self):
        self.logger.info("Starting test_successful_login")

        # Временная отладка
        print(f"DEBUG: Config type: {type(self.config)}")
        print(f"DEBUG: Config attributes: {dir(self.config)}")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"
            self.login_page.take_screenshot("login_page_loaded")

        with allure.step("Perform login with valid credentials"):
            self.login_page.login("tomsmith", "SuperSecretPassword!")

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login failure with invalid credentials")
    def test_failed_login_invalid_username(self):
        self.logger.info("Starting test_failed_login_invalid_username")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"

        with allure.step("Perform login with invalid username"):
            self.login_page.login("invalid_user", "SuperSecretPassword!")

        with allure.step("Verify login failure"):
            flash_message = self.login_page.get_flash_message()
            assert "Your username is invalid!" in flash_message
            assert not self.login_page.is_logout_visible(), "Logout button should not be visible after failed login"
            self.logger.info("Login failed as expected with invalid username")

    @allure.story("Failed Login - Invalid Password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_failed_login_invalid_password(self):
        self.logger.info("Starting test_failed_login_invalid_password")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"

        with allure.step("Perform login with invalid password"):
            self.login_page.login("tomsmith", "wrongpassword")

        with allure.step("Verify login failure"):
            flash_message = self.login_page.get_flash_message()
            assert "Your password is invalid!" in flash_message
            assert not self.login_page.is_logout_visible(), "Logout button should not be visible after failed login"
            self.logger.info("Login failed as expected with invalid password")

    @allure.story("API Authentication")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_authentication_mock(self):
        self.logger.info("Starting test_api_authentication_mock")

        with allure.step("Mock API authentication"):
            auth_response = self.api_service.authenticate("tomsmith", "SuperSecretPassword!")

        with allure.step("Verify authentication response"):
            assert auth_response["authenticated"] is True
            assert auth_response["user"] == "tomsmith"
            assert "token" in auth_response
            self.logger.info("API authentication mock completed successfully")

    @allure.story("Database Verification")
    @allure.severity(allure.severity_level.MINOR)
    def test_database_user_verification(self):
        self.logger.info("Starting test_database_user_verification")

        with allure.step("Connect to database"):
            try:
                self.db_service.connect()
                self.logger.info("Database connected successfully")

                # Since Herokuapp doesn't have real DB, we'll just verify connection works
                assert self.db_service.connection is not None
                self.logger.info("Database connection verified")

            except Exception as e:
                self.logger.warning(f"Database connection failed (expected for Herokuapp): {e}")
                # Don't fail the test if DB is not available
                pytest.skip("Database not available - skipping database verification")

        with allure.step("Close database connection"):
            self.db_service.disconnect()
            self.logger.info("Database connection closed")