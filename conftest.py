import pytest
from selene import browser

WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"


@pytest.fixture(scope="function", autouse=True)
def browser_management():
    browser.config.base_url = WEB_URL
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield

    browser.quit()