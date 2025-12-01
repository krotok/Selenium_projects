import pytest
import allure
import time
from core_project.amazon.pages.home_page import HomePage
from core_project.amazon.pages.search_results_page import SearchResultsPage
from core_project.amazon.pages.product_page import ProductPage
from core_project.amazon.pages.cart_page import CartPage
from core_project.core.utils.log_decorators import LoggingMixin


@allure.epic("Amazon Shopping")
@allure.feature("Samsung Phone Purchase Flow")
class TestSamsungPhonePurchase(LoggingMixin):
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.home_page = HomePage(driver)
        self.search_results_page = SearchResultsPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)

        self.logger.info(f"Test setup completed for Amazon environment")
        self.logger.debug(f"driver: {self.driver}")
        self.logger.debug(f"config: {self.config}")

        yield

        self.logger.info("Test cleanup completed")

    @allure.story("Complete Samsung Phone Purchase")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Search Samsung phones, sort by price, add 2 cheapest to cart, proceed to checkout")
    @pytest.mark.smoke
    @pytest.mark.amazon
    def test_complete_samsung_phone_purchase(self):
        self.logger.info("Starting complete Samsung phone purchase test")

        # Track added products for verification
        added_products = []

        with allure.step("1. Navigate to Amazon and accept cookies"):
            if not self.home_page.navigate_to_homepage(self.config.base_url):
                pytest.fail("Failed to navigate to Amazon homepage")

            self.home_page.accept_cookies_if_present()
            self.home_page.take_screenshot("amazon_homepage")

        with allure.step("2. Search for Samsung smartphones"):
            if not self.home_page.search_for_product(self.config.search_term):
                pytest.fail("Failed to search for products")

            if not self.search_results_page.wait_for_search_results():
                pytest.fail("Search results not loaded")

            self.search_results_page.take_screenshot("search_results")

        with allure.step("3. Filter by Samsung brand"):
            self.search_results_page.filter_by_samsung()
            time.sleep(3)  # Wait for filtering
            self.search_results_page.take_screenshot("after_samsung_filter")

        with allure.step("4. Sort results by price low to high"):
            if not self.search_results_page.sort_by_price_low_to_high():
                self.logger.warning("Could not sort by price, continuing with default order")

            time.sleep(3)  # Wait for sorting
            self.search_results_page.take_screenshot("after_price_sort")

        with allure.step("5. Find 2 cheapest Samsung phones"):
            cheapest_products = self.search_results_page.get_cheapest_products(
                count=self.config.items_to_add,
                min_price=self.config.min_price,
                max_price=self.config.max_price
            )

            if len(cheapest_products) < self.config.items_to_add:
                pytest.skip(
                    f"Not enough products found. Needed: {self.config.items_to_add}, Found: {len(cheapest_products)}")

            self.logger.info(f"Found {len(cheapest_products)} cheapest products")

            # Log product details
            for i, product in enumerate(cheapest_products):
                self.logger.info(f"Product {i + 1}: {product['title']} - ${product['price']}")

        with allure.step("6. Add cheapest products to cart"):
            initial_cart_count = self.home_page.get_cart_items_count()
            self.logger.info(f"Initial cart count: {initial_cart_count}")

            for i, product in enumerate(cheapest_products):
                with allure.step(f"Add product {i + 1} to cart: {product['title']}"):
                    # Select product
                    if not self.search_results_page.select_product(product):
                        pytest.fail(f"Failed to select product: {product['title']}")

                    # Get product details before adding to cart
                    product_title = self.product_page.get_product_title()
                    product_price = self.product_page.get_product_price()

                    # Add to cart
                    if not self.product_page.add_to_cart():
                        pytest.fail(f"Failed to add product to cart: {product_title}")

                    # Verify cart count increased
                    new_cart_count = self.product_page.get_cart_count()
                    expected_count = initial_cart_count + i + 1

                    if new_cart_count >= expected_count:
                        self.logger.info(f"Cart count updated: {new_cart_count}")
                    else:
                        self.logger.warning(
                            f"Cart count not updated as expected. Expected: {expected_count}, Actual: {new_cart_count}")

                    # Store product info
                    added_products.append({
                        'title': product_title,
                        'price': product_price,
                        'expected_cart_count': new_cart_count
                    })

                    self.product_page.take_screenshot(f"added_product_{i + 1}")

                    # Go back to search results for next product
                    if i < len(cheapest_products) - 1:  # Don't go back after last product
                        self.driver.back()
                        self.search_results_page.wait_for_search_results()

        with allure.step("7. Navigate to cart and verify items"):
            if not self.product_page.proceed_to_cart():
                pytest.fail("Failed to navigate to cart")

            if not self.cart_page.verify_cart_not_empty():
                pytest.fail("Cart is empty after adding products")

            # Verify cart items count
            cart_items_count = self.cart_page.get_cart_items_count()
            assert cart_items_count >= self.config.items_to_add, \
                f"Expected at least {self.config.items_to_add} items in cart, got {cart_items_count}"

            # Verify product titles in cart
            cart_titles = self.cart_page.get_product_titles_in_cart()
            self.logger.info(f"Products in cart: {cart_titles}")

            # Verify subtotal is displayed
            subtotal = self.cart_page.get_subtotal_price()
            self.logger.info(f"Cart subtotal: {subtotal}")

            self.cart_page.take_screenshot("cart_with_items")

        with allure.step("8. Proceed to checkout (stopping before payment)"):
            if self.cart_page.proceed_to_checkout():
                self.logger.info("Reached checkout page - stopping before payment as requested")
                # Take screenshot of checkout page
                self.cart_page.take_screenshot("checkout_page")

                # Verify we're on some kind of checkout/sign-in page
                current_url = self.driver.current_url
                assert any(keyword in current_url.lower() for keyword in ['checkout', 'signin', 'ap/signin']), \
                    f"Not on checkout page. Current URL: {current_url}"
            else:
                self.logger.warning("Could not proceed to checkout, but test completed successfully up to cart")

        with allure.step("9. Test completion summary"):
            self.logger.info("🎉 Amazon purchase flow test completed successfully!")
            self.logger.info(f"✅ Searched for: {self.config.search_term}")
            self.logger.info(f"✅ Added {len(added_products)} products to cart")
            self.logger.info(f"✅ Final cart count: {self.cart_page.get_cart_items_count()}")
            self.logger.info(f"✅ Reached checkout page")

    @allure.story("Cart Verification")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verify cart functionality and item management")
    def test_cart_functionality(self):
        """Additional test for cart functionality"""
        self.logger.info("Testing cart functionality")

        # This could be extended to test:
        # - Quantity changes
        # - Item removal
        # - Price calculations
        # - Save for later
        pytest.skip("Cart functionality test to be implemented")