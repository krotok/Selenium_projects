import pytest
import allure
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Добавляем пути для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'herokuapp'))

from herokuapp.config.init import Config
from core.utils.logger import LoggerConfig


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
    parser.addoption(
        "--log-level-pytest", action="store", default="INFO", help="Log level"
    )


@pytest.fixture(scope="session")
def config(request):
    """Load Herokuapp specific configuration"""
    env = request.config.getoption("--env")
    log_level = request.config.getoption("--log-level-pytest")

    config_obj = Config(env)

    # Override log level from command line
    if log_level:
        LoggerConfig.setup_logging(log_level=log_level)

    logger = LoggerConfig.get_logger(__name__)
    logger.info(f"Herokuapp configuration loaded for environment: {env}")

    return config_obj


@pytest.fixture
def driver(request, config):
    """WebDriver fixture with custom options"""
    logger = LoggerConfig.get_logger(__name__)

    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") or config.headless

    logger.info(f"Initializing {browser} browser (headless: {headless})")

    if browser.lower() == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
    elif browser.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(config.timeout)
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