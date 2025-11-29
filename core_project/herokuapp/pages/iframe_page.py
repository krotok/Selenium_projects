from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchFrameException
from core_project.core.base.base_page import BasePage
import allure
from core_project.core.utils.log_decorators import log_page_interaction, log_function_call


class IFramePage(BasePage):
    """Herokuapp specific IFrame page"""

    # Herokuapp specific locators
    IFRAME_LINK = (By.LINK_TEXT, "Frames")
    IFRAME_SUB_LINK = (By.LINK_TEXT, "iFrame")
    IFRAME = (By.ID, "mce_0_ifr")
    EDITOR_TEXTAREA = (By.ID, "tinymce")
    BOLD_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Bold']")
    PAGE_HEADER = (By.TAG_NAME, "h3")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.debug("IFramePage initialized")

    @allure.step("Navigate to IFrame page")
    @log_page_interaction("Navigate to IFrame page")
    def navigate_to_iframe_page(self, base_url: str) -> None:
        """Navigate to Herokuapp IFrame page"""
        self.driver.get(f"{base_url}/frames")
        self.wait_for_page_to_load()
        self.logger.info(f"Navigated to frames page: {base_url}/frames")

        # Click on iFrame link
        self.safe_click(self.IFRAME_SUB_LINK)
        self.wait_for_page_to_load()
        self.logger.info("Navigated to iFrame page")

    @allure.step("Switch to IFrame")
    @log_function_call(log_time=True)
    def switch_to_iframe(self) -> None:
        """Switch to the text editor iframe"""
        try:
            iframe_element = self.wait_for_element(self.IFRAME)
            self.driver.switch_to.frame(iframe_element)
            self.logger.info("Successfully switched to IFrame")
        except NoSuchFrameException as e:
            self.logger.error(f"Failed to switch to IFrame: {e}")
            raise

    @allure.step("Switch back to main content")
    @log_function_call()
    def switch_to_main_content(self) -> None:
        """Switch back to main content from iframe"""
        self.driver.switch_to.default_content()
        self.logger.info("Switched back to main content")

    @allure.step("Get page header text")
    @log_function_call(log_result=True)
    def get_page_header(self) -> str:
        """Get the page header text"""
        try:
            header = self.wait_for_element(self.PAGE_HEADER)
            return header.text
        except Exception as e:
            self.logger.warning(f"Could not get page header: {e}")
            return ""

    @allure.step("Verify on iframe page")
    @log_function_call(log_result=True)
    def is_on_iframe_page(self) -> bool:
        """Check if currently on iframe page"""
        try:
            header = self.get_page_header()
            return "An iFrame containing the TinyMCE WYSIWYG Editor" in header
        except:
            return False