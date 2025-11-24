import pytest
import logging
import allure
from pages.dynamic_loading_page import DynamicLoadingPage
from services.wiremock_service import WireMockService

logger = logging.getLogger(__name__)


@allure.epic("Dynamic Content")
@allure.feature("Dynamic Loading")
class TestDynamicLoading:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.dynamic_loading_page = DynamicLoadingPage(driver)
        self.wiremock_service = WireMockService()
        yield

    @allure.story("Example 1 Loading")
    @allure.severity(allure.severity_level.NORMAL)
    def test_example_1_loading(self):
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

    @allure.story("Example 2 Loading")
    @allure.severity(allure.severity_level.NORMAL)
    def test_example_2_loading(self):
        with allure.step("Navigate to dynamic loading page"):
            self.dynamic_loading_page.navigate_to_dynamic_loading(self.config.base_url)

        with allure.step("Select example 2"):
            self.dynamic_loading_page.select_example_2()

        with allure.step("Start loading process"):
            self.dynamic_loading_page.start_loading()

        with allure.step("Verify loading indicator appears"):
            assert self.dynamic_loading_page.is_loading_indicator_visible(), "Loading indicator should be visible"

        with allure.step("Wait for loading to complete"):
            self.dynamic_loading_page.wait_for_loading_to_complete(timeout=15)

        with allure.step("Verify result text"):
            result_text = self.dynamic_loading_page.get_result_text()
            assert result_text == "Hello World!", f"Expected 'Hello World!', but got '{result_text}'"

    @allure.story("WireMock Integration")
    @allure.severity(allure.severity_level.NORMAL)
    def test_dynamic_content_with_wiremock(self):
        with allure.step("Setup WireMock stub for dynamic content"):
            success = self.wiremock_service.create_dynamic_content_stub(delay=2)
            assert success, "Failed to create WireMock stub"

        with allure.step("Reset WireMock mappings after test"):
            self.wiremock_service.reset_mappings()