from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
import time
import pytest
import random

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
        #driver.get_screenshot_as_file('screen-'+str(int(time.time()*1000))+'.png')


    def before_quit(self, driver):
        print('Finished')


def test_7(driver):
    wait = WebDriverWait(driver, 4)
    driver.get('http://localhost/litecart')

    cart_locator = 'div#cart span.quantity'
    sizes = ('Small', 'Medium', 'Large')
    quantities = (1, 2, 3, 4, 5)

    for i in range(5):
        prev_cart_items = int(driver.find_element_by_css_selector(cart_locator).text)
        driver.find_element_by_css_selector('div#box-campaign-products div[data-id="1"]').click()

        Select(driver.find_element_by_css_selector('select[name="options[Size]"]')).select_by_value(random.choice(sizes))
        driver.find_element_by_css_selector('input[name=quantity]').clear()
        quantity = random.choice(quantities)
        driver.find_element_by_css_selector('input[name=quantity]').send_keys(str(quantity))
        driver.find_element_by_css_selector('button[name=add_cart_product]').click()
        driver.find_element_by_css_selector('div[aria-label=Close]').click()

        wait.until(ec.text_to_be_present_in_element((By.CSS_SELECTOR, cart_locator), str(prev_cart_items + quantity) ))
        new_cart_items = int(driver.find_element_by_css_selector(cart_locator).text)
        assert  new_cart_items - prev_cart_items == quantity

    driver.find_element_by_css_selector('div#cart').click()
    items = len(driver.find_elements_by_css_selector('table tr.item'))
    for i in range(items):
        table = driver.find_element_by_css_selector('table[class*="items table"]')
        remove_buttons = driver.find_elements_by_css_selector('tr.item button[name=remove_cart_item]')
        assert len(remove_buttons) > 0
        remove_buttons[0].click()
        wait.until(ec.staleness_of(table))

    driver.find_element_by_css_selector('p a[href]').click()
    assert int(driver.find_element_by_css_selector(cart_locator).text) == 0
