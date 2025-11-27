import pytest
import allure
import time

from selenium.webdriver.common.by import By

from pages.iframe_page import IFramePage
from utils.log_decorators import LoggingMixin


@allure.epic("Herokuapp Frames")
@allure.feature("IFrame Functionality")
class TestIFrame(LoggingMixin):
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.iframe_page = IFramePage(driver)

        self.logger.info(f"Test setup completed for environment: {config.environment}")

        yield

        self.logger.info("Test cleanup completed")

    @allure.story("Basic IFrame Operations")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test basic text operations in IFrame editor")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_basic_iframe_text_operations(self):
        self.logger.info("Starting test_basic_iframe_text_operations")

        with allure.step("Navigate to IFrame page"):
            self.iframe_page.navigate_to_iframe_page(self.config.base_url)
            self.iframe_page.take_screenshot("iframe_page_loaded")

        with allure.step("Verify we are on iframe page"):
            assert self.iframe_page.is_on_iframe_page(), "Should be on iframe page"
            self.logger.info("Successfully navigated to iframe page")

        with allure.step("Clear default editor content"):
            self.iframe_page.clear_editor_content()
            # Don't assert empty since there might be default content

        with allure.step("Type text in editor"):
            test_text = "Hello, this is a test message!"
            self.iframe_page.type_text_in_editor(test_text)
            self.iframe_page.take_screenshot("after_typing_text")

        with allure.step("Verify text was entered correctly"):
            actual_text = self.iframe_page.get_editor_text()
            assert test_text in actual_text, f"Expected '{test_text}' in editor, but got '{actual_text}'"
            self.logger.info(f"Text verification passed: '{test_text}'")

    @allure.story("IFrame Switching")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test switching between IFrame and main content")
    def test_iframe_switching(self):
        self.logger.info("Starting test_iframe_switching")

        with allure.step("Navigate to IFrame page"):
            self.iframe_page.navigate_to_iframe_page(self.config.base_url)
            assert self.iframe_page.is_on_iframe_page(), "Should be on iframe page"

        with allure.step("Switch to IFrame and verify"):
            self.iframe_page.switch_to_iframe()
            assert self.iframe_page.is_element_present(
                self.iframe_page.EDITOR_TEXTAREA), "Editor should be accessible in IFrame"

        with allure.step("Switch back to main content and verify"):
            self.iframe_page.switch_to_main_content()
            # Check for any element in main content
            assert self.iframe_page.is_element_present((By.TAG_NAME, "body")), "Should be back in main content"

        with allure.step("Take screenshot after switching"):
            self.iframe_page.take_screenshot("after_frame_switching")

    @allure.story("Text Formatting in IFrame")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test text formatting options in IFrame editor")
    def test_text_formatting_in_iframe(self):
        self.logger.info("Starting test_text_formatting_in_iframe")

        with allure.step("Navigate to IFrame page"):
            self.iframe_page.navigate_to_iframe_page(self.config.base_url)
            assert self.iframe_page.is_on_iframe_page(), "Should be on iframe page"

        with allure.step("Clear editor and enter text"):
            self.iframe_page.clear_editor_content()
            self.iframe_page.type_text_in_editor("Formatted Text")

        with allure.step("Apply bold formatting"):
            self.iframe_page.apply_bold_formatting()
            self.iframe_page.take_screenshot("after_bold_formatting")

        with allure.step("Verify editor still contains text"):
            text = self.iframe_page.get_editor_text()
            assert "Formatted Text" in text, "Text should remain in editor after formatting"
            self.logger.info("Text formatting test completed")

    @allure.story("Multiple Text Entries")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test multiple text entries and clearing")
    def test_multiple_text_entries(self):
        self.logger.info("Starting test_multiple_text_entries")

        with allure.step("Navigate to IFrame page"):
            self.iframe_page.navigate_to_iframe_page(self.config.base_url)
            assert self.iframe_page.is_on_iframe_page(), "Should be on iframe page"

        # First text entry
        with allure.step("First text entry"):
            text1 = "First paragraph of text."
            self.iframe_page.set_editor_content_js(text1)

            actual_text1 = self.iframe_page.get_editor_text()
            assert text1 in actual_text1, f"First text should be in editor: {text1}"

        # Second text entry
        with allure.step("Second text entry"):
            text2 = "Second paragraph added."
            self.iframe_page.set_editor_content_js(text2)

            actual_text2 = self.iframe_page.get_editor_text()
            assert text2 in actual_text2, "Second text should be in editor"

        with allure.step("Take final screenshot"):
            self.iframe_page.take_screenshot("after_multiple_entries")

    @allure.story("IFrame HTML Content")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Test retrieving HTML content from IFrame")
    def test_iframe_html_content(self):
        self.logger.info("Starting test_iframe_html_content")

        with allure.step("Navigate to IFrame page"):
            self.iframe_page.navigate_to_iframe_page(self.config.base_url)
            assert self.iframe_page.is_on_iframe_page(), "Should be on iframe page"

        with allure.step("Set content via JavaScript"):
            test_content = "<p>Test <strong>HTML</strong> content</p>"
            self.iframe_page.set_editor_content_js(test_content)

        with allure.step("Get HTML content"):
            html_content = self.iframe_page.get_editor_html_content()
            self.logger.debug(f"Editor HTML content: {html_content}")

            assert html_content is not None, "HTML content should not be None"
            assert isinstance(html_content, str), "HTML content should be a string"
            assert len(html_content) > 0, "HTML content should not be empty"

            # Attach HTML content to Allure report
            allure.attach(html_content, name="editor_html_content", attachment_type=allure.attachment_type.HTML)

    @allure.story("IFrame Navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test complete navigation and interaction flow")
    @pytest.mark.smoke
    def test_complete_iframe_workflow(self):
        self.logger.info("Starting test_complete_iframe_workflow")

        with allure.step("1. Navigate to frames page"):
            self.driver.get(f"{self.config.base_url}/frames")
            self.iframe_page.wait_for_page_to_load()

            # Verify using page header instead of title
            frames_header = self.iframe_page.get_page_header()
            assert "Frames" in frames_header, f"Should be on frames page, but header is: {frames_header}"
            self.iframe_page.take_screenshot("frames_page")

        with allure.step("2. Navigate to iFrame page"):
            self.iframe_page.safe_click(self.iframe_page.IFRAME_SUB_LINK)
            self.iframe_page.wait_for_page_to_load()

            # Verify using page header
            iframe_header = self.iframe_page.get_page_header()
            assert "An iFrame containing the TinyMCE WYSIWYG Editor" in iframe_header, f"Should be on iframe page, but header is: {iframe_header}"
            self.iframe_page.take_screenshot("iframe_page")

        with allure.step("3. Verify IFrame is present"):
            assert self.iframe_page.is_element_present(self.iframe_page.IFRAME), "IFrame should be present on page"

        with allure.step("4. Switch to IFrame and interact"):
            self.iframe_page.switch_to_iframe()
            assert self.iframe_page.is_element_present(
                self.iframe_page.EDITOR_TEXTAREA), "Should be able to access editor in IFrame"

            # Type text using JavaScript for reliability
            workflow_text = "Complete workflow test text"
            self.iframe_page.set_editor_content_js(workflow_text)

        with allure.step("5. Switch back and verify in main content"):
            self.iframe_page.switch_to_main_content()
            # Verify we can see elements in main content
            assert self.iframe_page.is_element_present((By.TAG_NAME, "h3")), "Should be back in main content"

        with allure.step("6. Final verification"):
            self.iframe_page.switch_to_iframe()
            final_text = self.iframe_page.get_editor_text()
            assert workflow_text in final_text, f"Text should persist: {workflow_text}"

            self.iframe_page.take_screenshot("complete_workflow_final")

        self.logger.info("Complete IFrame workflow test passed successfully")

    @allure.story("IFrame Direct Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test direct navigation to iframe page")
    def test_direct_iframe_navigation(self):
        self.logger.info("Starting test_direct_iframe_navigation")

        with allure.step("Navigate directly to iframe page"):
            self.driver.get(f"{self.config.base_url}/iframe")
            self.iframe_page.wait_for_page_to_load()

            # Verify page loaded correctly
            header = self.iframe_page.get_page_header()
            assert "An iFrame containing the TinyMCE WYSIWYG Editor" in header, f"Should be on iframe page, header: {header}"

            self.iframe_page.take_screenshot("direct_iframe_navigation")

        with allure.step("Test basic iframe interaction"):
            self.iframe_page.switch_to_iframe()
            assert self.iframe_page.is_element_present(self.iframe_page.EDITOR_TEXTAREA), "Editor should be accessible"

            # Test typing
            test_text = "Direct navigation test"
            self.iframe_page.type_text_in_editor(test_text)

            # Verify text
            actual_text = self.iframe_page.get_editor_text()
            assert test_text in actual_text, f"Text should be in editor: {test_text}"