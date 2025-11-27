import pytest
import allure
from pages.dynamic_loading_page import DynamicLoadingPage
from services.wiremock_service import WireMockService
from utils.log_decorators import LoggingMixin


@allure.epic("Dynamic Content")
@allure.feature("Dynamic Loading")
class TestDynamicLoading(LoggingMixin):
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.dynamic_loading_page = DynamicLoadingPage(driver)
        self.wiremock_service = WireMockService()

        self.logger.info(f"Test setup completed for environment: {config.environment}")

        yield

        self.logger.info("Test cleanup completed")

    @allure.story("Example 1 Loading")
    @allure.severity(allure.severity_level.NORMAL)
    def test_example_1_loading(self):
        self.logger.info("Starting test_example_1_loading")

        with allure.step("Navigate to dynamic loading page"):
            self.dynamic_loading_page.navigate_to_dynamic_loading(self.config.base_url)

        with allure.step("Select example 1"):
            self.dynamic_loading_page.select_example_1()

        with allure.step("Start loading process"):
            self.dynamic_loading_page.start_loading()

        with allure.step("Wait for loading to complete"):
            self.dynamic_loading_page.wait_for_loading_to_complete()

        with allure.step("Verify result text"):
            result_text = self.dynamic_loading_page.get_result_text()
            assert result_text == "Hello World!", f"Expected 'Hello World!', but got '{result_text}'"
            self.logger.info(f"Dynamic loading completed with result: {result_text}")

    @allure.story("Example 2 Loading")
    @allure.severity(allure.severity_level.NORMAL)
    def test_example_2_loading(self):
        self.logger.info("Starting test_example_2_loading")

        with allure.step("Navigate to dynamic loading page"):
            self.dynamic_loading_page.navigate_to_dynamic_loading(self.config.base_url)

        with allure.step("Select example 2"):
            self.dynamic_loading_page.select_example_2()

        with allure.step("Start loading process"):
            self.dynamic_loading_page.start_loading()

        with allure.step("Verify loading indicator appears"):
            assert self.dynamic_loading_page.is_loading_indicator_visible(), "Loading indicator should be visible"
            self.logger.info("Loading indicator is visible")

        with allure.step("Wait for loading to complete"):
            self.dynamic_loading_page.wait_for_loading_to_complete(timeout=15)

        with allure.step("Verify result text"):
            result_text = self.dynamic_loading_page.get_result_text()
            assert result_text == "Hello World!", f"Expected 'Hello World!', but got '{result_text}'"
            self.logger.info(f"Dynamic loading completed with result: {result_text}")

    @allure.story("WireMock Integration")
    @allure.severity(allure.severity_level.NORMAL)
    def test_dynamic_content_with_wiremock(self):
        self.logger.info("Starting test_dynamic_content_with_wiremock")

        with allure.step("Setup WireMock stub for dynamic content"):
            success = self.wiremock_service.create_dynamic_content_stub(delay=2)
            assert success, "Failed to create WireMock stub"
            self.logger.info("WireMock stub created successfully")

        with allure.step("Reset WireMock mappings after test"):
            self.wiremock_service.reset_mappings()
            self.logger.info("WireMock mappings reset")