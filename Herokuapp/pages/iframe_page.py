from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchFrameException
from .base_page import BasePage
import allure
import time
from utils.log_decorators import log_page_interaction, log_function_call


class IFramePage(BasePage):
    # Locators
    IFRAME_LINK = (By.LINK_TEXT, "Frames")
    IFRAME_SUB_LINK = (By.LINK_TEXT, "iFrame")
    IFRAME = (By.ID, "mce_0_ifr")
    EDITOR_TEXTAREA = (By.ID, "tinymce")
    BOLD_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Bold']")
    ITALIC_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Italic']")
    FORMAT_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Format']")
    HEADINGS_MENU = (By.CSS_SELECTOR, "div[title='Headings']")
    HEADING_1 = (By.CSS_SELECTOR, "div[title='Heading 1']")
    EDITOR_CONTENT = (By.CSS_SELECTOR, "body#tinymce p")
    FILE_MENU = (By.CSS_SELECTOR, "button[aria-label='File']")
    NEW_DOCUMENT = (By.CSS_SELECTOR, "div[title='New document']")
    PAGE_HEADER = (By.TAG_NAME, "h3")

    def __init__(self, driver):
        super().__init__(driver)  # Важно: вызываем конструктор родителя
        self.logger.debug("IFramePage initialized")

    @allure.step("Navigate to IFrame page")
    @log_page_interaction("Navigate to IFrame page")
    def navigate_to_iframe_page(self, base_url: str) -> None:
        """Navigate to IFrame page"""
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

    @allure.step("Clear text editor content")
    @log_page_interaction("Clear text editor")
    def clear_editor_content(self) -> None:
        """Clear all content from text editor"""
        self.switch_to_iframe()
        try:
            textarea = self.wait_for_element(self.EDITOR_TEXTAREA)
            # Use JavaScript to clear content more reliably
            self.driver.execute_script("arguments[0].innerHTML = '';", textarea)
            self.logger.info("Cleared text editor content")
        finally:
            self.switch_to_main_content()

    @allure.step("Type text in editor: {text}")
    @log_page_interaction("Type text in editor")
    def type_text_in_editor(self, text: str) -> None:
        """Type text in the text editor"""
        self.switch_to_iframe()
        try:
            textarea = self.wait_for_element(self.EDITOR_TEXTAREA)
            textarea.click()  # Ensure focus
            textarea.send_keys(text)
            self.logger.info(f"Typed text in editor: {text}")
        finally:
            self.switch_to_main_content()

    @allure.step("Get editor text content")
    @log_function_call(log_result=True)
    def get_editor_text(self) -> str:
        """Get text content from editor"""
        self.switch_to_iframe()
        try:
            # Try to get text from the editor body
            textarea = self.wait_for_element(self.EDITOR_TEXTAREA)
            text = textarea.text
            self.logger.debug(f"Retrieved editor text: {text}")
            return text
        except Exception as e:
            self.logger.warning(f"Could not get editor text: {e}")
            return ""
        finally:
            self.switch_to_main_content()

    @allure.step("Apply bold formatting")
    @log_page_interaction("Apply bold formatting")
    def apply_bold_formatting(self) -> None:
        """Apply bold formatting to text"""
        self.switch_to_main_content()
        try:
            if self.is_element_present(self.BOLD_BUTTON):
                self.safe_click(self.BOLD_BUTTON)
                self.logger.info("Applied bold formatting")
            else:
                self.logger.warning("Bold button not found")
        finally:
            self.switch_to_iframe()

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

    @allure.step("Verify on frames page")
    @log_function_call(log_result=True)
    def is_on_frames_page(self) -> bool:
        """Check if currently on frames page"""
        try:
            header = self.get_page_header()
            return "Frames" in header
        except:
            return False

    @allure.step("Verify on iframe page")
    @log_function_call(log_result=True)
    def is_on_iframe_page(self) -> bool:
        """Check if currently on iframe page"""
        try:
            header = self.get_page_header()
            return "An iFrame containing the TinyMCE WYSIWYG Editor" in header
        except:
            return False

    @allure.step("Get editor HTML content")
    @log_function_call(log_result=True)
    def get_editor_html_content(self) -> str:
        """Get HTML content from editor"""
        self.switch_to_iframe()
        try:
            textarea = self.wait_for_element(self.EDITOR_TEXTAREA)
            html_content = textarea.get_attribute('innerHTML')
            self.logger.debug(f"Retrieved editor HTML content")
            return html_content
        finally:
            self.switch_to_main_content()

    @allure.step("Set editor content via JavaScript")
    @log_page_interaction("Set editor content via JS")
    def set_editor_content_js(self, content: str) -> None:
        """Set editor content using JavaScript"""
        self.switch_to_iframe()
        try:
            textarea = self.wait_for_element(self.EDITOR_TEXTAREA)
            self.driver.execute_script("arguments[0].innerHTML = arguments[1];", textarea, content)
            self.logger.info(f"Set editor content via JS: {content}")
        finally:
            self.switch_to_main_content()

    @allure.step("Wait for editor to be ready")
    @log_function_call(log_time=True)
    def wait_for_editor_ready(self, timeout: int = 10) -> bool:
        """Wait for editor to be ready for interaction"""
        self.switch_to_iframe()
        try:
            return self.wait_for_element_clickable(self.EDITOR_TEXTAREA, timeout) is not None
        finally:
            self.switch_to_main_content()