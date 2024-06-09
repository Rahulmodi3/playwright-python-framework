from Tests.test_base import BaseTest
from playwright.sync_api import expect


class TestInventory(BaseTest):

    def test_add_to_cart(self, login):
        """
        Verify that a product can be added to the cart.
        """
        product_name = "Sauce Labs Fleece Jacket"
        self.product_page = login

        # Verify the cart is initially empty
        cart_icon = self.product_page.get_cart_icon_locator()
        expect(cart_icon).to_have_text("")

        # Add product to cart
        self.product_page.add_product_to_cart(product_name)

        # Verify the cart icon shows 1 item
        cart_icon = self.product_page.get_cart_icon_locator()
        expect(cart_icon).to_have_text("1")

        # Verify the "Remove" button is visible for the added product
        remove_button = self.product_page.get_remove_button_locator(product_name)
        expect(remove_button).to_be_visible()

    def test_add_multiple_products_to_cart(self, login):
        """
        Verify that multiple products can be added to the cart.
        """
        product1_name = "Sauce Labs Fleece Jacket"
        product2_name = "Sauce Labs Onesie"
        self.product_page = login

        # Add first product to cart
        self.product_page.add_product_to_cart(product1_name)
        # Add second product to cart
        self.product_page.add_product_to_cart(product2_name)

        # Verify the cart icon shows 2 items
        cart_icon = self.product_page.get_cart_icon_locator()
        expect(cart_icon).to_have_text("2")

    def test_remove_product_from_cart(self, login):
        """
        Verify that a product can be removed from the cart.
        """
        product_name = "Sauce Labs Fleece Jacket"
        self.product_page = login

        # Add product to cart
        self.product_page.add_product_to_cart(product_name)
        # Remove product from cart
        self.product_page.remove_product_from_cart(product_name)

        # Verify the cart is empty
        cart_icon = self.product_page.get_cart_icon_locator()
        expect(cart_icon).to_have_text("")
