from playwright.sync_api import Page, Locator

from Pages.Products.products_list_page import ProductsListPage
from Pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._selectors = self._Selectors()

    def set_username(self, value: str):
        self.current_page.fill(self._selectors.USERNAME, value)

    def set_password(self, value: str):
        self.current_page.fill(self._selectors.PASSWORD, value)

    def click_login(self):
        self.current_page.click(self._selectors.LOGIN_BUTTON)

    def login_to_application(self, username: str, password: str) -> ProductsListPage:
        self.set_username(username)
        self.set_password(password)
        self.click_login()
        return ProductsListPage(self.current_page)

    def get_error_locator(self) -> Locator:
        return self.current_page.locator(self._selectors.ERROR_MSG)

    def get_login_button_locator(self) -> Locator:
        return self.current_page.locator(self._selectors.LOGIN_BUTTON)

    class _Selectors:
        USERNAME = "#user-name"
        PASSWORD = "#password"
        LOGIN_BUTTON = "#login-button"
        ERROR_MSG = "[data-test='error']"



