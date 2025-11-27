import pytest
import allure
from pages.iframe_page import IFramePage
from utils.log_decorators import LoggingMixin


@allure.epic("Herokuapp Frames")
@allure.feature("Simple IFrame Tests")
class TestIFrameSimple(LoggingMixin):

    def test_simple_iframe_navigation(self, driver, config):
        """Simple test to verify basic iframe functionality"""
        self.logger.info("Starting simple iframe navigation test")

        iframe_page = IFramePage(driver)

        # Navigate directly to iframe page
        driver.get(f"{config.base_url}/iframe")
        iframe_page.wait_for_page_to_load()

        # Take screenshot
        iframe_page.take_screenshot("simple_iframe_page")

        # Verify page loaded
        header = iframe_page.get_page_header()
        self.logger.info(f"Page header: {header}")

        assert "An iFrame containing the TinyMCE WYSIWYG Editor" in header
        self.logger.info("Simple iframe test passed")

    def test_iframe_basic_interaction(self, driver, config):
        """Test basic interaction with iframe editor"""
        self.logger.info("Starting basic iframe interaction test")

        iframe_page = IFramePage(driver)

        # Navigate to iframe page
        driver.get(f"{config.base_url}/iframe")
        iframe_page.wait_for_page_to_load()

        # Switch to iframe and type text
        iframe_page.switch_to_iframe()

        # Clear and type text
        iframe_page.clear_editor_content()
        test_text = "Hello from automated test!"
        iframe_page.type_text_in_editor(test_text)

        # Get text back
        actual_text = iframe_page.get_editor_text()
        self.logger.info(f"Editor text: {actual_text}")

        # Basic assertion - text should be in editor
        assert test_text in actual_text

        iframe_page.take_screenshot("after_text_input")
        self.logger.info("Basic iframe interaction test passed")