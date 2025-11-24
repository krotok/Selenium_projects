from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Callable, Tuple
import logging

logger = logging.getLogger(__name__)


class CustomWaits:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element_to_have_text(self, locator: Tuple[str, str], text: str, timeout: int = None) -> bool:
        """Wait for element to have specific text"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                lambda driver: driver.find_element(*locator).text == text
            )
        except TimeoutException:
            logger.warning(f"Element did not have text '{text}' within timeout")
            return False

    def wait_for_element_to_contain_text(self, locator: Tuple[str, str], text: str, timeout: int = None) -> bool:
        """Wait for element to contain specific text"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                lambda driver: text in driver.find_element(*locator).text
            )
        except TimeoutException:
            logger.warning(f"Element did not contain text '{text}' within timeout")
            return False

    def wait_for_element_to_be_stale(self, element, timeout: int = None) -> bool:
        """Wait for element to become stale (removed from DOM)"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.staleness_of(element))
        except TimeoutException:
            logger.warning("Element did not become stale within timeout")
            return False

    def wait_for_page_to_load(self, timeout: int = None) -> bool:
        """Wait for page to fully load"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not load completely within timeout")
            return False