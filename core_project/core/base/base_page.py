from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import allure
import time
from typing import List, Tuple, Optional
from core_project.core.utils.log_decorators import log_function_call, log_page_interaction, LoggingMixin


class BasePage(LoggingMixin):
    """Base page class with common functionality for all pages"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 15
        self._wait = WebDriverWait(self.driver, self.timeout)
        self.actions = ActionChains(self.driver)
        self.logger.debug(f"Initialized {self.__class__.__name__}")

    @log_function_call(log_args=False, log_time=True)
    def wait_for_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Custom wait for element with retry logic"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_element_located(locator))

    @log_function_call(log_args=False, log_time=True)
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Wait for element to be clickable"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    @log_function_call(log_args=False)
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Wait for element to be visible"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    @log_function_call(log_args=False)
    def click_with_retry(self, locator: Tuple[str, str], retries: int = 3) -> None:
        """Click element with retry for stale element references"""
        for attempt in range(retries):
            try:
                element = self.wait_for_element_clickable(locator)
                element.click()
                self.logger.debug(f"Successfully clicked element on attempt {attempt + 1}")
                return
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    self.logger.error(f"Failed to click element after {retries} attempts")
                    raise
                self.logger.warning(f"Stale element detected, retrying {attempt + 1}/{retries}")

    @log_page_interaction("Safe click on element")
    def safe_click(self, locator: Tuple[str, str]) -> None:
        """Safe click with JavaScript fallback"""
        try:
            self.click_with_retry(locator)
        except Exception as e:
            self.logger.warning(f"Standard click failed, trying JavaScript: {e}")
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].click();", element)

    @log_function_call(log_args=False)
    def is_element_present(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Check if element is present without throwing exception"""
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    @log_function_call(log_args=False)
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Check if element is visible"""
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    @log_function_call(log_result=True)
    def get_element_text(self, locator: Tuple[str, str]) -> str:
        """Safely get element text"""
        element = self.wait_for_element_visible(locator)
        return element.text.strip()

    @log_page_interaction("Type text into field")
    def type_text(self, locator: Tuple[str, str], text: str) -> None:
        """Type text into field with clearing"""
        element = self.wait_for_element_clickable(locator)
        element.clear()
        element.send_keys(text)
        self.logger.debug(f"Typed text into field")

    def take_screenshot(self, name: str) -> None:
        """Take screenshot and attach to Allure"""
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        self.logger.debug(f"Screenshot taken: {name}")

    @log_function_call()
    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """Scroll to element"""
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    @log_function_call(log_time=True)
    def wait_for_page_to_load(self, timeout: int = None) -> bool:
        """Wait for page to fully load"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            self.logger.warning("Page did not load completely within timeout")
            return False

    @log_function_call(log_time=True)
    def wait_for_url_contains(self, text: str, timeout: int = None) -> bool:
        """Wait for URL to contain specific text"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.url_contains(text))
        except TimeoutException:
            self.logger.warning(f"URL did not contain '{text}' within timeout")
            return False

    @log_function_call()
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url

    @log_function_call()
    def dismiss_any_popups(self):
        """Try to dismiss any potential popups"""
        try:
            # Try pressing Escape
            from selenium.webdriver.common.keys import Keys
            body = self.driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ESCAPE)
            self.logger.info("Dismissed popups with Escape key")

            # Wait a moment for popup to disappear
            self.wait_for_page_to_load(1)

        except Exception as e:
            self.logger.debug(f"Popup dismissal failed: {e}")

    @log_function_call()
    def disable_autocomplete(self):
        """Disable autocomplete on all form fields to prevent browser save prompts"""
        try:
            self.driver.execute_script("""
                var inputs = document.querySelectorAll('input');
                inputs.forEach(function(input) {
                    input.setAttribute('autocomplete', 'off');
                    input.setAttribute('autocorrect', 'off');
                    input.setAttribute('autocapitalize', 'off');
                    input.setAttribute('spellcheck', 'false');
                });
            """)
            self.logger.info("Disabled autocomplete on all form fields")
        except Exception as e:
            self.logger.debug(f"Autocomplete disable failed: {e}")