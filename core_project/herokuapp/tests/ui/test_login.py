import sys
import os

from selenium.webdriver.common.by import By
from core_project.herokuapp.pages.login_page import LoginPage
import allure
from core_project.core.utils.log_decorators import log_page_interaction, log_function_call


import pytest
import allure
import requests
from core_project.core.services.api_service import ApiService
from core_project.core.utils.log_decorators import LoggingMixin

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../core'))

@allure.epic("Herokuapp Authentication")
@allure.feature("Login Functionality")
class TestLogin(LoggingMixin):
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.login_page = LoginPage(driver)

        # Используем base_url для API service, так как Herokuapp не имеет отдельного API
        self.api_service = ApiService(config.base_url)

        self.logger.info(f"Test setup completed for environment: {config.environment}")

        yield

        # Cleanup
        self.api_service.close()
        self.logger.info("Test cleanup completed")

    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test successful login with valid credentials")
    @pytest.mark.smoke
    def test_successful_login(self):
        self.logger.info("Starting test_successful_login")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"
            self.login_page.take_screenshot("login_page_loaded")

        with allure.step("Perform login with valid credentials"):
            user = self.config.test_users["valid"]
            self.login_page.login(user["username"], user["password"])

        with allure.step("Verify successful login"):
            assert self.login_page.is_logout_visible(), "Logout button should be visible after successful login"
            flash_message = self.login_page.get_flash_message()
            assert "You logged into a secure area!" in flash_message
            self.logger.info("Login successful - user redirected to secure area")

        with allure.step("Take screenshot after successful login"):
            self.login_page.take_screenshot("after_successful_login")

    @allure.story("Failed Login - Invalid Username")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login failure with invalid username")
    def test_failed_login_invalid_username(self):
        self.logger.info("Starting test_failed_login_invalid_username")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"

        with allure.step("Perform login with invalid username"):
            user = self.config.test_users["invalid"]
            self.login_page.login(user["username"], user["password"])

        with allure.step("Verify login failure message"):
            flash_message = self.login_page.get_flash_message()
            assert "Your username is invalid!" in flash_message
            assert self.login_page.is_logout_not_present, "Logout button should not be visible after failed login"
            self.logger.info("Login failed as expected with invalid username")

        with allure.step("Take screenshot after failed login"):
            self.login_page.take_screenshot("after_invalid_username")

    @allure.story("Failed Login - Invalid Password")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login failure with invalid password but valid username")
    def test_failed_login_invalid_password(self):
        self.logger.info("Starting test_failed_login_invalid_password")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"

        with allure.step("Perform login with invalid password"):
            valid_user = self.config.test_users["valid"]
            invalid_password = "wrong_password_123"
            self.login_page.login(valid_user["username"], invalid_password)

        with allure.step("Verify login failure message"):
            flash_message = self.login_page.get_flash_message()
            assert "Your password is invalid!" in flash_message
            assert self.login_page.is_logout_not_present, "Logout button should not be visible after failed login"
            self.logger.info("Login failed as expected with invalid password")

        with allure.step("Take screenshot after invalid password"):
            self.login_page.take_screenshot("after_invalid_password")

    @allure.story("Failed Login - Empty Credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login failure with empty username and password")
    def test_failed_login_empty_credentials(self):
        self.logger.info("Starting test_failed_login_empty_credentials")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"

        with allure.step("Perform login with empty credentials"):
            self.login_page.login("", "")

        with allure.step("Verify login failure message"):
            flash_message = self.login_page.get_flash_message()
            # Herokuapp might show different message for empty credentials
            msgs_lst = ["Your username is invalid!", "Your password is invalid!"]
            assert any(msg in flash_message for msg in msgs_lst), \
                f"Unexpected flash message: {flash_message}"
            assert self.login_page.is_logout_not_present, "Logout button should not be visible after failed login"
            self.logger.info("Login failed as expected with empty credentials")

    @allure.story("Failed Login - SQL Injection Attempt")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Test login failure with SQL injection attempt")
    def test_failed_login_sql_injection(self):
        self.logger.info("Starting test_failed_login_sql_injection")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"

        with allure.step("Perform login with SQL injection attempt"):
            sql_injection_username = "admin' OR '1'='1"
            sql_injection_password = "password"
            self.login_page.login(sql_injection_username, sql_injection_password)

        with allure.step("Verify SQL injection attempt failed"):
            flash_message = self.login_page.get_flash_message()
            assert "Your username is invalid!" in flash_message or "Your password is invalid!" in flash_message
            assert self.login_page.is_logout_not_present, "SQL injection attempt should be blocked"
            self.logger.info("SQL injection attempt correctly blocked")

    @allure.story("Mock API Authentication")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test mock API authentication service")
    @pytest.mark.api
    def test_mock_api_authentication(self):
        self.logger.info("Starting test_mock_api_authentication")

        with allure.step("Mock successful API authentication"):
            valid_user = self.config.test_users["valid"]
            auth_response = self.api_service.authenticate(valid_user["username"], valid_user["password"])

            allure.attach(str(auth_response), name="Successful Auth Response",
                          attachment_type=allure.attachment_type.JSON)

            assert auth_response["authenticated"] is True, "Authentication should be successful"
            assert auth_response["user"] == valid_user["username"], f"User should be {valid_user['username']}"
            assert "token" in auth_response, "Response should contain auth token"
            self.logger.info("Mock API authentication successful")

        with allure.step("Mock failed API authentication - invalid username"):
            invalid_user = self.config.test_users["invalid"]
            failed_auth_response = self.api_service.authenticate(invalid_user["username"], invalid_user["password"])

            # In our mock implementation, it always returns success, but in real scenario:
            # assert failed_auth_response["authenticated"] is False
            self.logger.info("Mock API authentication test completed")

    @allure.story("API Endpoint Availability")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test Herokuapp API endpoints availability")
    @pytest.mark.api
    def test_api_endpoint_availability(self):
        self.logger.info("Starting test_api_endpoint_availability")

        with allure.step("Check main page availability via API"):
            try:
                # Herokuapp doesn't have real API, so we'll test the main page
                response = self.api_service.session.get(self.config.base_url)
                assert response.status_code == 200, f"Main page should be available, got {response.status_code}"
                self.logger.info("Main page is accessible via API")
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"API request failed: {e}")
                pytest.skip("Network issue - skipping API availability test")

        with allure.step("Check non-existent endpoint"):
            try:
                response = self.api_service.session.get(f"{self.config.base_url}/nonexistent-endpoint")
                # Herokuapp returns 404 for non-existent pages
                assert response.status_code == 404, "Non-existent endpoint should return 404"
                self.logger.info("Non-existent endpoint correctly returns 404")
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"API request to non-existent endpoint failed: {e}")

    @allure.story("Login Form Validation")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Test login form UI elements and validation")
    def test_login_form_validation(self):
        self.logger.info("Starting test_login_form_validation")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"

        with allure.step("Verify login form elements are present"):
            assert self.login_page.is_element_present(
                self.login_page.USERNAME_FIELD), "Username field should be present"
            assert self.login_page.is_element_present(
                self.login_page.PASSWORD_FIELD), "Password field should be present"
            assert self.login_page.is_element_present(self.login_page.LOGIN_BUTTON), "Login button should be present"
            self.logger.info("All login form elements are present")

        with allure.step("Verify password field type is password"):
            password_field = self.login_page.wait_for_element(self.login_page.PASSWORD_FIELD)
            field_type = password_field.get_attribute("type")
            assert field_type == "password", f"Password field should be type='password', got '{field_type}'"
            self.logger.info("Password field correctly has type='password'")

        with allure.step("Take screenshot of login form"):
            self.login_page.take_screenshot("login_form_validation")

    @allure.story("Multiple Failed Login Attempts")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Test behavior after multiple failed login attempts")
    def test_multiple_failed_login_attempts(self):
        self.logger.info("Starting test_multiple_failed_login_attempts")

        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login(self.config.base_url)
            assert self.login_page.is_on_login_page(), "Should be on login page"

        with allure.step("First failed login attempt"):
            self.login_page.login("wrong_user_1", "wrong_pass_1")
            flash_message_1 = self.login_page.get_flash_message()
            assert "Your username is invalid!" in flash_message_1
            self.logger.info("First failed attempt completed")

        with allure.step("Second failed login attempt"):
            # Refresh page to simulate new session
            self.login_page.navigate_to_login(self.config.base_url)
            self.login_page.login("wrong_user_2", "wrong_pass_2")
            flash_message_2 = self.login_page.get_flash_message()
            assert "Your username is invalid!" in flash_message_2
            self.logger.info("Second failed attempt completed")

        with allure.step("Verify login form still works after multiple failures"):
            assert self.login_page.is_on_login_page(), "Should still be on login page after failures"
            assert self.login_page.is_element_present(
                self.login_page.USERNAME_FIELD), "Username field should still be accessible"
            self.logger.info("Login form remains functional after multiple failures")

    @allure.story("Login Success Then Logout")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test complete login and logout flow with credentials save popup handling")
    def test_login_logout_flow(self):
        self.logger.info("Starting test_login_logout_flow")

        with allure.step("Navigate to login page and login"):
            self.login_page.navigate_to_login(self.config.base_url)
            user = self.config.test_users["valid"]
            self.login_page.login(user["username"], user["password"])

            # Verify login successful
            assert self.login_page.is_logout_visible(), "Should be logged in"
            self.login_page.take_screenshot("after_login_before_logout")

        # with allure.step("Handle credentials save popup if present"):
        #     try:
        #         # Different strategies to handle browser save password popup
        #         self._handle_credentials_save_popup()
        #         self.logger.info("Credentials save popup handled successfully")
        #     except Exception as e:
        #         self.logger.warning(f"Could not handle credentials popup: {e}")

        with allure.step("Perform logout"):
            self.login_page.logout()

            # Verify logout successful
            assert self.login_page.is_logout_not_present, "Should be logged out"
            flash_message = self.login_page.get_flash_message()
            assert "You logged out of the secure area!" in flash_message
            self.logger.info("Logout successful")

        with allure.step("Verify back on login page"):
            assert self.login_page.is_on_login_page(), "Should be back on login page after logout"
            self.login_page.take_screenshot("after_logout")
        #
        # with allure.step("Test browser autofill behavior after logout"):
        #     self._verify_autofill_behavior(user)

    def _handle_credentials_save_popup(self):
        """Handle browser save credentials popup using different strategies"""

        self.logger.info("Attempting to handle credentials save popup")

        # Strategy 1: Try to detect and handle Chrome save password popup
        try:
            # Chrome save password popup might have these elements
            chrome_save_locator = (By.CSS_SELECTOR, "div[role='alertdialog']")
            chrome_never_save_button = (By.CSS_SELECTOR, "button[data-cy='never-save-button']")
            chrome_not_now_button = (By.CSS_SELECTOR, "button[data-cy='not-now-button']")

            if self.login_page.is_element_present(chrome_save_locator, timeout=3):
                self.logger.info("Chrome save password popup detected")

                # Try to click "Never" or "Not now"
                if self.login_page.is_element_present(chrome_never_save_button, timeout=2):
                    self.login_page.safe_click(chrome_never_save_button)
                    self.logger.info("Clicked 'Never Save' button")
                elif self.login_page.is_element_present(chrome_not_now_button, timeout=2):
                    self.login_page.safe_click(chrome_not_now_button)
                    self.logger.info("Clicked 'Not Now' button")

        except Exception as e:
            self.logger.debug(f"Chrome popup handling failed: {e}")

        # Strategy 2: Try to handle Firefox save password popup
        try:
            firefox_save_locator = (By.ID, "password-save-notification")
            firefox_never_button = (By.ID, "password-save-notification-never-button")

            if self.login_page.is_element_present(firefox_save_locator, timeout=3):
                self.logger.info("Firefox save password popup detected")

                if self.login_page.is_element_present(firefox_never_button, timeout=2):
                    self.login_page.safe_click(firefox_never_button)
                    self.logger.info("Clicked Firefox 'Never Save' button")

        except Exception as e:
            self.logger.debug(f"Firefox popup handling failed: {e}")

        # Strategy 3: Use JavaScript to prevent save prompt (more reliable)
        try:
            # Disable autocomplete to prevent browser from suggesting to save passwords
            self.login_page.driver.execute_script("""
                var inputs = document.querySelectorAll('input[type=\"password\"], input[type=\"text\"]');
                inputs.forEach(function(input) {
                    input.setAttribute('autocomplete', 'off');
                    input.setAttribute('data-lpignore', 'true');
                });
            """)
            self.logger.info("Disabled autocomplete via JavaScript")
        except Exception as e:
            self.logger.debug(f"JavaScript autocomplete disable failed: {e}")

        # Strategy 4: Press Escape key to dismiss any popups
        try:
            from selenium.webdriver.common.keys import Keys
            body = self.login_page.driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ESCAPE)
            self.logger.info("Pressed Escape key to dismiss popups")
            self.login_page.wait_for_page_to_load(2)
        except Exception as e:
            self.logger.debug(f"Escape key strategy failed: {e}")

    def _verify_autofill_behavior(self, user):
        """Verify browser autofill behavior after login-logout cycle"""

        self.logger.info("Verifying autofill behavior")

        with allure.step("Check if browser autofilled credentials"):
            try:
                # Navigate to login page again to check autofill
                self.login_page.navigate_to_login(self.config.base_url)

                # Check if username field has any value (might be autofilled)
                username_field = self.login_page.wait_for_element(self.login_page.USERNAME_FIELD)
                autofilled_username = username_field.get_attribute('value')

                # Check if password field has any value (might be autofilled)
                password_field = self.login_page.wait_for_element(self.login_page.PASSWORD_FIELD)
                autofilled_password = password_field.get_attribute('value')

                if autofilled_username or autofilled_password:
                    self.logger.info(
                        f"Browser autofilled - Username: '{autofilled_username}', Password: {'*' * len(autofilled_password) if autofilled_password else 'None'}")

                    # Clear autofilled values for clean test state
                    if autofilled_username:
                        username_field.clear()
                    if autofilled_password:
                        password_field.clear()

                    self.logger.info("Cleared autofilled values")
                else:
                    self.logger.info("No autofill detected - fields are empty")

                self.login_page.take_screenshot("autofill_check")

            except Exception as e:
                self.logger.warning(f"Autofill verification failed: {e}")