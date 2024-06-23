import base64
import pytest

from Pages.Login.login_page import LoginPage
from Utilities.read_config import AppConfiguration
from playwright.sync_api import sync_playwright
from Pages.Products.products_list_page import ProductsListPage


def get_browser(browser_name, playwright, launch_options):
    match browser_name:
        case "chromium":
            return playwright.chromium.launch(**launch_options, args=['--start-maximized'])
        case "firefox":
            return playwright.firefox.launch(**launch_options)
        case "msedge":
            return playwright.chromium.launch(channel='msedge', **launch_options, args=['--start-maximized'])
        case "webkit":
            return playwright.webkit.launch(**launch_options)
        case _:
            raise ValueError(f"Unsupported browser: {browser_name}")


@pytest.fixture()
def setup(request, setup_browser):
    configuration = AppConfiguration.get_app_configuration()
    common_info = AppConfiguration.get_common_info()
    base_url = common_info["Url"]

    # Browser options
    headless = eval(configuration["Headless"])  # convert to bool
    slow_mo = float(configuration["SlowMo"])
    launch_options = {"headless": headless, "slow_mo": slow_mo}

    # Start Playwright
    playwright = sync_playwright().start()
    browser = get_browser(setup_browser, playwright, launch_options)
    # browser = playwright.chromium.launch(**launch_options, args=['--start-maximized'])

    context_options = {'base_url': base_url}

    # Browser context settings
    if setup_browser == "firefox" or setup_browser == "webkit":
        browser_context = browser.new_context(**context_options, viewport={"width": 1920, "height": 1080})
    else:
        browser_context = browser.new_context(**context_options, no_viewport=True)

    browser_context.set_default_navigation_timeout(float(configuration["DefaultNavigationTimeout"]))
    browser_context.set_default_timeout(float(configuration["DefaultTimeout"]))

    # Create Page
    page = browser_context.new_page()

    request.cls.page = page
    page.goto(base_url)

    yield page
    page.close()
    browser.close()
    playwright.stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    screenshot_bytes = ''
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')

        if report.failed or xfail and "page" in item.funcargs:
            page = item.funcargs["setup"]

            screenshot_bytes = page.screenshot()
            extra.append(pytest_html.extras.image(base64.b64encode(screenshot_bytes).decode(), ''))

        report.extras = extra


@pytest.fixture()
def login(request) -> ProductsListPage:
    configuration = AppConfiguration.get_common_info()

    username = configuration["ValidUserName"]
    password = configuration["ValidPassword"]
    login = LoginPage(request.cls.page)
    login.login_to_application(username, password)
    return ProductsListPage(request.cls.page)


def pytest_addoption(parser):
    parser.addoption("--browser-name", action="store", default="chromium", help="Browser to run tests with (chromium, "
                                                                                "firefox, webkit, edge)")


@pytest.fixture()
def setup_browser(request):
    """
    :return: This will return the browser name to setup method
    """
    return request.config.getoption("--browser-name")
