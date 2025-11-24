import pytest
import logging
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config import Config
from services.database_service import DatabaseService
from services.wiremock_service import WireMockService
import os
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--env", action="store", default="dev", help="Environment: dev or stage"
    )
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser: chrome or firefox"
    )
    parser.addoption(
        "--headless", action="store_true", help="Run tests in headless mode"
    )


@pytest.fixture(scope="session")
def config(request):
    """Load configuration based on environment"""
    env = request.config.getoption("--env")
    return Config(env)


@pytest.fixture
def driver(request, config):
    """WebDriver fixture with custom options"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") or config.get('headless', False)

    if browser.lower() == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")

        driver = webdriver.Chrome(options=options)
    elif browser.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(config.get('timeout', 10))
    driver.maximize_window()

    yield driver

    # Take screenshot on test failure
    if request.node.rep_call.failed:
        try:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(
                screenshot_dir,
                f"{request.node.name}_{int(time.time())}.png"
            )
            driver.save_screenshot(screenshot_path)
            allure.attach.file(
                screenshot_path,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logging.error(f"Failed to take screenshot: {e}")

    driver.quit()


@pytest.fixture(scope="session")
def database_service(config):
    """Database service fixture"""
    service = DatabaseService(config.db_config)
    try:
        service.connect()
        yield service
    finally:
        service.disconnect()


@pytest.fixture
def wiremock_service():
    """WireMock service fixture"""
    service = WireMockService()
    yield service
    # Cleanup: reset mappings after each test
    service.reset_mappings()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to add additional information to test reports"""
    outcome = yield
    rep = outcome.get_result()

    # Set test result for driver fixture
    setattr(item, "rep_" + rep.when, rep)


# Custom markers
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "database: mark test as database test"
    )


@pytest.fixture(autouse=True)
def log_test_execution(request):
    """Automatically log test execution"""
    logging.info(f"Starting test: {request.node.name}")
    yield
    logging.info(f"Finished test: {request.node.name}")