from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self._wait = WebDriverWait(self.driver, self.timeout)

    def wait_for_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Custom wait for element with retry logic"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Wait for element to be clickable"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def click_with_retry(self, locator: Tuple[str, str], retries: int = 3) -> None:
        """Click element with retry for stale element references"""
        for attempt in range(retries):
            try:
                element = self.wait_for_element_clickable(locator)
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise
                logger.warning(f"Stale element detected, retrying {attempt + 1}/{retries}")

    def is_element_present(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Check if element is present without throwing exception"""
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def get_element_text(self, locator: Tuple[str, str]) -> str:
        """Safely get element text"""
        element = self.wait_for_element(locator)
        return element.text.strip()

    def take_screenshot(self, name: str) -> None:
        """Take screenshot and attach to Allure"""
        import allure
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)