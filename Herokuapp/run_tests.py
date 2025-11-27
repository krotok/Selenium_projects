"""
Test Runner for  Herokuapp site
Provides multiple ways to execute the test suite
"""

import subprocess
import sys
import os
import argparse
from utils.logger import LoggerConfig

# Setup logging
logger = LoggerConfig.get_logger(__name__)


def run_basic_tests(env="dev", browser="chrome", headless=False, log_level="INFO"):
    """Run basic test suite"""
    logger.info("Running basic test suite...")

    cmd = [
        "pytest",
        "tests/",
        "-v",
        "--alluredir=reports/allure-results",
        f"--env={env}",
        f"--browser={browser}",
        f"--log-level-pytest={log_level}"
    ]

    if headless:
        cmd.append("--headless")

    try:
        result = subprocess.run(cmd, check=True)
        logger.info("Basic tests completed successfully")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"Tests failed with exit code: {e.returncode}")
        return e.returncode


def run_smoke_tests(env="dev", browser="chrome", headless=False, log_level="INFO"):
    """Run only smoke tests"""
    logger.info("Running smoke tests...")

    cmd = [
        "pytest",
        "tests/",
        "-m", "smoke",
        "-v",
        "--alluredir=reports/allure-results",
        f"--env={env}",
        f"--browser={browser}",
        f"--log-level-pytest={log_level}"
    ]

    if headless:
        cmd.append("--headless")

    try:
        result = subprocess.run(cmd, check=True)
        logger.info("Smoke tests completed successfully")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"Smoke tests failed: {e}")
        return e.returncode


def run_ui_tests(env="dev", browser="chrome", headless=True, log_level="INFO"):
    """Run only UI tests"""
    logger.info("Running UI tests...")

    cmd = [
        "pytest",
        "tests/",
        "-m", "ui",
        "-v",
        "--alluredir=reports/allure-results",
        f"--env={env}",
        f"--browser={browser}",
        f"--log-level-pytest={log_level}"
    ]

    if headless:
        cmd.append("--headless")

    try:
        result = subprocess.run(cmd, check=True)
        logger.info("UI tests completed successfully")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"UI tests failed: {e}")
        return e.returncode


def run_with_allure_report(env="dev", browser="chrome", headless=False, log_level="INFO"):
    """Run tests and generate Allure report"""
    logger.info("Running tests with Allure report generation...")

    # Run tests
    cmd_run = [
        "pytest",
        "tests/",
        "-v",
        "--alluredir=reports/allure-results",
        f"--env={env}",
        f"--browser={browser}",
        f"--log-level-pytest={log_level}"
    ]

    if headless:
        cmd_run.append("--headless")

    try:
        # Execute tests
        subprocess.run(cmd_run, check=True)

        # Generate Allure report
        cmd_report = [
            "allure", "generate", "reports/allure-results",
            "-o", "reports/allure-report", "--clean"
        ]
        subprocess.run(cmd_report, check=True)

        logger.info("Allure report generated: reports/allure-report/index.html")
        return 0

    except subprocess.CalledProcessError as e:
        logger.error(f"Test execution failed: {e}")
        return e.returncode


def run_parallel_tests(env="dev", browser="chrome", headless=True, log_level="INFO"):
    """Run tests in parallel"""
    logger.info("Running tests in parallel...")

    cmd = [
        "pytest",
        "tests/",
        "-n", "2",  # 2 parallel workers
        "-v",
        "--alluredir=reports/allure-results",
        f"--env={env}",
        f"--browser={browser}",
        f"--log-level-pytest={log_level}"
    ]

    if headless:
        cmd.append("--headless")

    try:
        result = subprocess.run(cmd, check=True)
        logger.info("Parallel tests completed successfully")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"Parallel tests failed: {e}")
        return e.returncode


def run_specific_test(test_name, env="dev", browser="chrome", headless=False, log_level="INFO"):
    """Run a specific test by name"""
    logger.info(f"Running specific test: {test_name}")

    cmd = [
        "pytest",
        f"tests/{test_name}",
        "-v",
        "--alluredir=reports/allure-results",
        f"--env={env}",
        f"--browser={browser}",
        f"--log-level-pytest={log_level}",
        "-s"  # Show print statements
    ]

    if headless:
        cmd.append("--headless")

    try:
        result = subprocess.run(cmd, check=True)
        logger.info(f"Test {test_name} completed successfully")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"Test {test_name} failed: {e}")
        return e.returncode


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Herokuapp parsing')
    parser.add_argument('--mode', choices=['basic', 'smoke', 'ui', 'allure', 'parallel', 'specific'],
                        default='basic', help='Test execution mode')
    parser.add_argument('--test', help='Specific test to run (for specific mode)')
    parser.add_argument('--env', choices=['dev', 'stage'], default='dev', help='Environment')
    parser.add_argument('--browser', choices=['chrome', 'firefox'], default='chrome', help='Browser')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='INFO', help='Log level')

    args = parser.parse_args()

    # Set environment variables for pytest
    os.environ['PYTEST_CURRENT_TEST'] = '1'

    logger.info(f"Starting test execution in {args.mode} mode")
    logger.info(f"Environment: {args.env}, Browser: {args.browser}, Headless: {args.headless}")

    try:
        if args.mode == 'basic':
            return run_basic_tests(args.env, args.browser, args.headless, args.log_level)
        elif args.mode == 'smoke':
            return run_smoke_tests(args.env, args.browser, args.headless, args.log_level)
        elif args.mode == 'ui':
            return run_ui_tests(args.env, args.browser, args.headless, args.log_level)
        elif args.mode == 'allure':
            return run_with_allure_report(args.env, args.browser, args.headless, args.log_level)
        elif args.mode == 'parallel':
            return run_parallel_tests(args.env, args.browser, args.headless, args.log_level)
        elif args.mode == 'specific':
            if not args.test:
                logger.error("Please specify a test file with --test")
                return 1
            return run_specific_test(args.test, args.env, args.browser, args.headless, args.log_level)
        else:
            logger.error(f"Unknown mode: {args.mode}")
            return 1

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())