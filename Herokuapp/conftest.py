import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.init import Config
from services.database_service import DatabaseService
from services.wiremock_service import WireMockService
import os
import time
from utils.log_decorators import LoggerConfig
from pages.iframe_page import IFramePage


# Logging is now automatically configured via Config class

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
    # Use a different name to avoid conflict
    parser.addoption(
        "--log-level-pytest", action="store", default="INFO",
        help="Log level: DEBUG, INFO, WARNING, ERROR"
    )


@pytest.fixture(scope="session")
def config(request):
    """Load configuration based on environment"""
    env = request.config.getoption("--env")
    log_level = request.config.getoption("--log-level-pytest")

    config_obj = Config(env)

    # Override log level from command line
    if log_level:
        LoggerConfig.setup_logging(log_level=log_level)

    logger = LoggerConfig.get_logger(__name__)
    logger.info(f"Configuration loaded for environment: {env}")

    return config_obj


@pytest.fixture
def driver(request, config):
    """WebDriver fixture with custom options"""
    logger = LoggerConfig.get_logger(__name__)

    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") or config.get('headless', False)

    logger.info(f"Initializing {browser} browser (headless: {headless})")

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

    logger.info("WebDriver initialized successfully")

    yield driver

    # Take screenshot on test failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
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
            logger.info(f"Screenshot saved on failure: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")

    driver.quit()
    logger.info("WebDriver closed")


@pytest.fixture(scope="session")
def database_service(config):
    """Database service fixture"""
    logger = LoggerConfig.get_logger(__name__)
    service = DatabaseService(config.db_config)
    try:
        service.connect()
        logger.info("Database service connected")
        yield service
    finally:
        service.disconnect()
        logger.info("Database service disconnected")


@pytest.fixture
def wiremock_service():
    """WireMock service fixture"""
    logger = LoggerConfig.get_logger(__name__)
    service = WireMockService()
    logger.info("WireMock service initialized")
    yield service
    # Cleanup: reset mappings after each test
    service.reset_mappings()
    logger.info("WireMock service cleanup completed")


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
    config.addinivalue_line(
        "markers", "wiremock: tests using wiremock"
    )


@pytest.fixture(autouse=True)
def log_test_execution(request):
    """Automatically log test execution"""
    logger = LoggerConfig.get_logger(__name__)
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Finished test: {request.node.name}")

@pytest.fixture
def iframe_page(driver, config):
    """IFrame page fixture"""
    logger = LoggerConfig.get_logger(__name__)

    page = IFramePage(driver)
    logger.info("IFrame page fixture initialized")
    return page