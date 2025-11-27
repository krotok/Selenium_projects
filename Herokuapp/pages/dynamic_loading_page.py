from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure
import time
from utils.log_decorators import log_page_interaction, log_function_call


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
        self.logger.debug("DynamicLoadingPage initialized")

    @allure.step("Navigate to dynamic loading page")
    @log_page_interaction("Navigate to dynamic loading")
    def navigate_to_dynamic_loading(self, base_url: str) -> None:
        """Navigate to dynamic loading page"""
        self.driver.get(f"{base_url}/dynamic_loading")
        self.wait_for_page_to_load()
        self.logger.info(f"Navigated to dynamic loading page: {base_url}/dynamic_loading")

    @allure.step("Select example 1")
    @log_page_interaction("Select example 1")
    def select_example_1(self) -> None:
        """Select example 1"""
        self.safe_click(self.EXAMPLE_1_LINK)
        self.wait_for_page_to_load()
        self.logger.info("Selected example 1")

    @allure.step("Select example 2")
    @log_page_interaction("Select example 2")
    def select_example_2(self) -> None:
        """Select example 2"""
        self.safe_click(self.EXAMPLE_2_LINK)
        self.wait_for_page_to_load()
        self.logger.info("Selected example 2")

    @allure.step("Start loading process")
    @log_page_interaction("Start loading")
    def start_loading(self) -> None:
        """Click start button to initiate loading"""
        self.safe_click(self.START_BUTTON)
        self.logger.info("Started loading process")

    @allure.step("Wait for loading to complete")
    @log_function_call(log_time=True)
    def wait_for_loading_to_complete(self, timeout: int = 10) -> None:
        """Wait for loading to complete and text to appear"""
        self.wait_for_element(self.FINISH_TEXT, timeout)
        self.logger.info("Loading completed successfully")

    @allure.step("Get result text")
    @log_function_call(log_result=True)
    def get_result_text(self) -> str:
        """Get the final result text"""
        text = self.get_element_text(self.FINISH_TEXT)
        self.logger.debug(f"Result text: {text}")
        return text

    @allure.step("Check if loading indicator is visible")
    @log_function_call(log_result=True)
    def is_loading_indicator_visible(self) -> bool:
        """Check if loading indicator is visible"""
        is_visible = self.is_element_present(self.LOADING_INDICATOR, timeout=2)
        self.logger.debug(f"Loading indicator visible: {is_visible}")
        return is_visible