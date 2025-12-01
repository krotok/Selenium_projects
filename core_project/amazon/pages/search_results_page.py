import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../core'))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from core_project.core.base.base_page import BasePage
import allure
import time
from core_project.core.utils.log_decorators import log_page_interaction, log_function_call


class SearchResultsPage(BasePage):
    """Amazon search results page with sorting and product selection"""

    # Locators
    SEARCH_RESULTS = (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h2 a span")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".a-price-whole")
    PRODUCT_LINK = (By.CSS_SELECTOR, "h2 a")
    SORT_DROPDOWN = (By.ID, "s-result-sort-select")
    PRICE_LOW_TO_HIGH = (By.ID, "s-result-sort-select_1")
    LOADING_SPINNER = (By.CSS_SELECTOR, ".s-result-list-save-ons-loading")
    FILTER_BY_BRAND = (By.XPATH, "//span[text()='Brand']")
    SAMSUNG_CHECKBOX = (By.XPATH, "//span[text()='Samsung']/preceding-sibling::input")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.debug("Amazon SearchResultsPage initialized")

    @allure.step("Wait for search results to load")
    def wait_for_search_results(self, timeout: int = 20) -> bool:
        """Wait for search results to load completely"""
        try:
            self.wait_for_element(self.SEARCH_RESULTS, timeout=timeout)
            # Wait for loading to complete
            self.wait_for_element_to_disappear(self.LOADING_SPINNER, timeout=10)
            self.logger.debug("Search results loaded successfully")
            return True
        except Exception as e:
            self.logger.error(f"Search results not loaded: {e}")
            return False

    @allure.step("Sort results by price low to high")
    @log_page_interaction("Sort by price low to high")
    def sort_by_price_low_to_high(self) -> bool:
        """Sort search results by price ascending"""
        try:
            if self.is_element_present(self.SORT_DROPDOWN):
                # Click sort dropdown
                self.safe_click(self.SORT_DROPDOWN)
                time.sleep(1)

                # Select price low to high
                if self.is_element_present(self.PRICE_LOW_TO_HIGH):
                    self.safe_click(self.PRICE_LOW_TO_HIGH)
                    self.wait_for_page_to_load()
                    self.logger.info("Sorted results by price: low to high")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to sort results: {e}")
            return False

    @allure.step("Filter by Samsung brand")
    @log_page_interaction("Filter by Samsung brand")
    def filter_by_samsung(self) -> bool:
        """Filter results by Samsung brand"""
        try:
            if self.is_element_present(self.FILTER_BY_BRAND):
                # Ensure brand section is expanded
                self.scroll_to_element(self.FILTER_BY_BRAND)

                # Click Samsung checkbox
                if self.is_element_present(self.SAMSUNG_CHECKBOX):
                    self.safe_click(self.SAMSUNG_CHECKBOX)
                    time.sleep(3)  # Wait for results to filter
                    self.logger.info("Filtered results by Samsung brand")
                    return True
            return False
        except Exception as e:
            self.logger.debug(f"Could not filter by Samsung: {e}")
            return False

    @allure.step("Get all search results")
    @log_function_call(log_result=True)
    def get_search_results(self) -> list:
        """Get all search result elements"""
        try:
            results = self.driver.find_elements(*self.SEARCH_RESULTS)
            self.logger.debug(f"Found {len(results)} search results")
            return results
        except Exception as e:
            self.logger.error(f"Error getting search results: {e}")
            return []

    @allure.step("Extract product info from result")
    def extract_product_info(self, result_element) -> dict:
        """Extract product information from result element"""
        try:
            # Get product title
            title_element = result_element.find_element(*self.PRODUCT_TITLE)
            title = title_element.text.strip()

            # Get product price
            price = "0"
            try:
                price_element = result_element.find_element(*self.PRODUCT_PRICE)
                price = price_element.text.strip().replace(',', '')
            except:
                pass  # Price might not be available

            # Get product link
            link_element = result_element.find_element(*self.PRODUCT_LINK)
            product_url = link_element.get_attribute('href')

            product_info = {
                'title': title,
                'price': float(price) if price.replace('.', '').isdigit() else 0,
                'url': product_url,
                'element': result_element
            }

            return product_info

        except Exception as e:
            self.logger.debug(f"Error extracting product info: {e}")
            return None

    @allure.step("Get cheapest products")
    @log_function_call(log_result=True)
    def get_cheapest_products(self, count: int = 2, min_price: float = 100, max_price: float = 1000) -> list:
        """Get the cheapest available products within price range"""
        self.logger.info(f"Looking for {count} cheapest products between ${min_price}-${max_price}")

        try:
            results = self.get_search_results()
            valid_products = []

            for i, result in enumerate(results[:20]):  # Check first 20 results
                try:
                    product_info = self.extract_product_info(result)
                    if product_info and product_info['price'] >= min_price and product_info['price'] <= max_price:
                        valid_products.append(product_info)
                        self.logger.debug(f"Valid product found: {product_info['title']} - ${product_info['price']}")
                except Exception as e:
                    self.logger.debug(f"Error processing result {i}: {e}")
                    continue

            # Sort by price and return cheapest ones
            valid_products.sort(key=lambda x: x['price'])
            cheapest = valid_products[:count]

            self.logger.info(f"Found {len(cheapest)} cheapest products")
            return cheapest

        except Exception as e:
            self.logger.error(f"Error finding cheapest products: {e}")
            return []

    @allure.step("Select product by index")
    @log_page_interaction("Select product")
    def select_product(self, product_info: dict) -> bool:
        """Select a product from search results"""
        try:
            # Scroll to the product
            self.scroll_to_element(self.PRODUCT_LINK)

            # Click on the product
            product_info['element'].find_element(*self.PRODUCT_LINK).click()
            self.wait_for_page_to_load()

            self.logger.info(f"Selected product: {product_info['title']}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to select product: {e}")
            return False

    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = 10) -> bool:
        """Wait for element to disappear from DOM"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.invisibility_of_element_located(locator))
        except:
            return True  # Element already disappeared or not present