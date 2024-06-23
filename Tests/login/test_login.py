from Pages.Login.login_page import LoginPage
from Tests.test_base import BaseTest
from Utilities.read_config import AppConfiguration
from playwright.sync_api import expect


class TestLogin(BaseTest):

    configuration = AppConfiguration.get_common_info()

    def get_user_credentials(self, user_type):
        return {
            "username": self.configuration[user_type + "UserName"],
            "password": self.configuration[user_type + "Password"]
        }

    def test_login_with_valid_credentials(self):
        """
        Verify login with valid credentials.
        """
        self.login_page = LoginPage(self.page)
        creds = self.get_user_credentials("Valid")

        # Perform login
        self.login_page.login_to_application(creds["username"], creds["password"])

        # Verify that the user is navigated to the Products page
        title = self.login_page.screen_title()
        expect(title).to_have_text('Products')

    def test_login_with_invalid_credentials(self):
        """
        Verify login with invalid credentials.
        """
        expected_error_msg = "Epic sadface: Username and password do not match any user in this service"

        self.login_page = LoginPage(self.page)
        creds = self.get_user_credentials("Invalid")

        # Perform login
        self.login_page.login_to_application(creds["username"], creds["password"])

        # Verify that the appropriate error message is displayed
        actual_msg = self.login_page.get_error_locator()
        expect(actual_msg).to_have_text(expected_error_msg)

    def test_login_with_locked_user(self):
        """
        Verify login with a locked user.
        """
        expected_error_msg = "Epic sadface: Sorry, this user has been locked out."

        self.login_page = LoginPage(self.page)
        creds = self.get_user_credentials("Locked")

        # Perform login
        self.login_page.login_to_application(creds["username"], creds["password"])

        # Verify that the appropriate error message is displayed
        actual_msg = self.login_page.get_error_locator()
        expect(actual_msg).to_have_text(expected_error_msg)
