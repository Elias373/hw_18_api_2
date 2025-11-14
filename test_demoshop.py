import requests
import allure
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have
from conftest import WEB_URL, API_URL


def test_add_item_to_cart_via_api_and_verify_in_ui(browser_management):
    # Для корзины и тп нужна сессия для хранения всех кук, в отличие от авторизации где необходима одна кука или токен
    session = requests.Session()

    with step("Add item to cart via API"):
        response = session.post(
            url=API_URL + "/addproducttocart/catalog/31/1/1"
        )

        assert response.status_code == 200
        json_response = response.json()


        allure.attach(body=str(json_response), name="API Response", attachment_type=AttachmentType.TEXT)
        allure.attach(body=str(session.cookies), name="Session Cookies", attachment_type=AttachmentType.TEXT)

        print("✅ Item added to cart via API")

    with step("Transfer cookies to browser"):
        browser.open(WEB_URL)

        cookies_added = []
        for cookie in session.cookies:
            browser.driver.add_cookie({
                'name': cookie.name,
                'value': cookie.value,
                'path': '/'
            })
            cookies_added.append(cookie.name)

        browser.driver.refresh()

        allure.attach(body=str(cookies_added), name="Cookies Transferred", attachment_type=AttachmentType.TEXT)

        print(f"✅ Cookies transferred: {cookies_added}")


    with step("Open cart and verify item via UI"):
        browser.open(WEB_URL + "/cart")
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))

        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="Cart with item",
            attachment_type=AttachmentType.PNG)


        print("✅ Item verified in cart via UI")

