from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
import os
import pytest


@pytest.fixture
def driver(request):
    wd = EventFiringWebDriver(webdriver.Chrome(), MyListener())
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        pass

    def after_find(self, by, value, driver):
        pass

    def on_exception(self, exception, driver):
        print(exception)
        driver.get_screenshot_as_file('screen.png')


    def before_quit(self, driver):
        print('Finished')


def test_6(driver):
    wait = WebDriverWait(driver, 4)
    driver.get('http://localhost/litecart/admin')

    driver.find_element_by_css_selector('input[class=form-control][name=username]').send_keys('admin')
    driver.find_element_by_css_selector('input[class=form-control][name=password]').send_keys('admin')
    driver.find_element_by_css_selector('button[class="btn btn-default"][name=login]').click()

    driver.find_element_by_css_selector('body div ul li#app-catalog').click()
    buttons = driver.find_elements_by_css_selector('main ul a[class="btn btn-default"]')
    add_new_product = [el for el in buttons if 'Add New Product' in el.get_attribute('textContent')][0]
    add_new_product.click()

    driver.find_element_by_css_selector('ul[class="nav nav-tabs"] a[data-toggle=tab][href="#tab-general"]').click()
    name = "Duckling"
    code = "81555"
    gender = 'Male'
    sku = 'duck_sku'
    mpn = 'duck_mpn'
    gtin = 'duck_gtin'
    taric = 'duck_tarinc'
    manufacturer = '1'
    keyword = 'duck_keyword'
    valid_from = '04.06.2019'
    valid_to = '04.06.2020'
    image = os.path.abspath('0009.jpg')
    driver.find_element_by_css_selector('input[class=form-control][type=file]').send_keys(image)
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="name[en]"]').send_keys(name)
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="code"]').send_keys(code)
    driver.find_element_by_css_selector('input[type=checkbox][name="product_groups[]"][value="1-1"]').click()
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="sku"]').send_keys(sku)
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="mpn"]').send_keys(mpn)
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="gtin"]').send_keys(gtin)
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="taric"]').send_keys(taric)
    Select(driver.find_element_by_css_selector('select.form-control[name=manufacturer_id]')).select_by_value(manufacturer)
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="keywords"]').send_keys(keyword)
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="date_valid_from"]').send_keys(valid_from)
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="date_valid_to"]').send_keys(valid_to)
    btn_statuses = driver.find_elements_by_css_selector('label[class*="btn btn-default"]')
    enabled_btn = [status for status in btn_statuses if "Enabled" in status.get_attribute('textContent')][0]
    enabled_btn.click()

    driver.find_element_by_css_selector('ul[class="nav nav-tabs"] a[data-toggle=tab][href="#tab-information"]').click()
    short_description = "This is a duckling short description"
    description = "This is a duckling description."
    driver.find_element_by_css_selector('div.tab-content input.form-control[name="short_description[en]"]').send_keys(short_description)
    driver.find_element_by_css_selector('div[contenteditable="true"]').send_keys(description)

    driver.find_element_by_css_selector('ul[class="nav nav-tabs"] a[data-toggle=tab][href="#tab-prices"]').click()
    purchase_price = '25.00'
    price = '20'
    currency = 'USD'
    driver.find_element_by_css_selector('input[name=purchase_price]').clear()
    driver.find_element_by_css_selector('input[name=purchase_price]').send_keys(purchase_price)
    Select(driver.find_element_by_css_selector('select[name=purchase_price_currency_code]')).select_by_value(currency)
    driver.find_element_by_css_selector('input.form-control[name="prices[USD]"]').send_keys(price)

    driver.find_element_by_css_selector('button[type=submit][name=save]').click()

    rows = driver.find_elements_by_css_selector('table tr a[href]')
    [row for row in rows if name in row.get_attribute('textContent')][0].click()

    assert 'Enabled' in driver.find_element_by_css_selector('label[class="btn btn-default active"]'
                                                            ).get_attribute('textContent')
    assert driver.find_element_by_css_selector('input.form-control[name="name[en]"]').get_attribute('value') == name
    assert driver.find_element_by_css_selector('input.form-control[name="code"]').get_attribute('value') == code
    assert driver.find_element_by_css_selector('input.form-control[name="code"]').get_attribute('value') == code
    assert driver.find_element_by_css_selector('input[type=checkbox][name="product_groups[]"][checked=checked]'
                                               ).get_attribute('value') == '1-1'
    assert driver.find_element_by_css_selector('input.form-control[name="sku"]').get_attribute('value') == sku
    assert driver.find_element_by_css_selector('input.form-control[name="mpn"]').get_attribute('value') == mpn
    assert driver.find_element_by_css_selector('input.form-control[name="gtin"]').get_attribute('value') == gtin
    assert driver.find_element_by_css_selector('input.form-control[name="taric"]').get_attribute('value') == taric
    assert driver.find_element_by_css_selector('select.form-control[name=manufacturer_id] option[selected="selected"]'
                                               ).get_attribute('value') == '1'
    assert driver.find_element_by_css_selector('input.form-control[name="keywords"]').get_attribute('value') == keyword
    assert driver.find_element_by_css_selector('input.form-control[name="date_valid_from"]').get_attribute('value') == '2019-06-04'
    assert driver.find_element_by_css_selector('input.form-control[name="date_valid_to"]').get_attribute('value') == '2020-06-04'
    assert 'Enabled' in driver.find_element_by_css_selector('label[class="btn btn-default active"]').get_attribute('textContent')

    driver.find_element_by_css_selector('ul[class="nav nav-tabs"] a[data-toggle=tab][href="#tab-information"]').click()
    assert  driver.find_element_by_css_selector('div.tab-content input.form-control[name="short_description[en]"]'
                                                ).get_attribute('value') == short_description
    assert driver.find_element_by_css_selector('div[contenteditable="true"]').get_attribute('textContent') == description

    driver.find_element_by_css_selector('ul[class="nav nav-tabs"] a[data-toggle=tab][href="#tab-prices"]').click()
    assert driver.find_element_by_css_selector('input[name=purchase_price]').get_attribute('value') == purchase_price
    assert driver.find_element_by_css_selector('input.form-control[name="prices[USD]"]').get_attribute('value') == price
    assert driver.find_element_by_css_selector('select[name=purchase_price_currency_code] option[selected=selected]'
                                               ).get_attribute('value') == currency

    driver.find_element_by_css_selector('i[class="fa fa-sign-out fa-lg"]').click()
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'body div[id=box-login]')))