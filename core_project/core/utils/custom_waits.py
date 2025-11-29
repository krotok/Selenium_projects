from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Callable, Tuple
from core_project.core.utils.logger import LoggerConfig


class CustomWaits:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = LoggerConfig.get_logger(__name__)

    def wait_for_element_to_have_text(self, locator: Tuple[str, str], text: str, timeout: int = None) -> bool:
        """Wait for element to have specific text"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                lambda driver: driver.find_element(*locator).text == text
            )
        except TimeoutException:
            self.logger.warning(f"Element did not have text '{text}' within timeout")
            return False

    def wait_for_element_to_contain_text(self, locator: Tuple[str, str], text: str, timeout: int = None) -> bool:
        """Wait for element to contain specific text"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                lambda driver: text in driver.find_element(*locator).text
            )
        except TimeoutException:
            self.logger.warning(f"Element did not contain text '{text}' within timeout")
            return False