from selenium.webdriver.common.by import By
from .base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class DynamicLoadingPage(BasePage):
    # Locators
    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    LOADING_INDICATOR = (By.ID, "loading")
    FINISH_TEXT = (By.ID, "finish")
    EXAMPLE_1_LINK = (By.XPATH, "//a[contains(text(),'Example 1')]")
    EXAMPLE_2_LINK = (By.XPATH, "//a[contains(text(),'Example 2')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_dynamic_loading(self, base_url: str) -> None:
        """Navigate to dynamic loading page"""
        self.driver.get(f"{base_url}/dynamic_loading")
        logger.info("Navigated to dynamic loading page")

    def select_example_1(self) -> None:
        """Select example 1"""
        self.click_with_retry(self.EXAMPLE_1_LINK)
        logger.info("Selected example 1")

    def select_example_2(self) -> None:
        """Select example 2"""
        self.click_with_retry(self.EXAMPLE_2_LINK)
        logger.info("Selected example 2")

    def start_loading(self) -> None:
        """Click start button to initiate loading"""
        self.click_with_retry(self.START_BUTTON)
        logger.info("Started loading process")

    def wait_for_loading_to_complete(self, timeout: int = 10) -> None:
        """Wait for loading to complete and text to appear"""
        self.wait_for_element(self.FINISH_TEXT, timeout)
        logger.info("Loading completed")

    def get_result_text(self) -> str:
        """Get the final result text"""
        return self.get_element_text(self.FINISH_TEXT)

    def is_loading_indicator_visible(self) -> bool:
        """Check if loading indicator is visible"""
        return self.is_element_present(self.LOADING_INDICATOR, timeout=2)