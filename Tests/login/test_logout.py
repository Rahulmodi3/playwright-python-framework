from Utilities.read_config import AppConfiguration
from Tests.test_base import BaseTest
from playwright.sync_api import expect


class TestLogout(BaseTest):

    def test_logout(self, login):
        """
        Verify that a user can log out successfully.
        :param login: pass login fixture for login into application
        """
        configuration = AppConfiguration.get_common_info()
        self.product_page = login

        # Click on the burger menu and log out
        self.product_page.click_burger_menu()
        self.login_page = self.product_page.click_logout()

        # Verify the login button is visible on the login page
        expect(self.login_page.get_login_button_locator()).to_be_visible()
        # Verify the URL is the login page URL
        expect(self.login_page.current_page).to_have_url(configuration["Url"])

