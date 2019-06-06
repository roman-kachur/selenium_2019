from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from Task10.tests import data_provider
import random

class CampaignProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self, base_url):
        self.driver.get(base_url)
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#campaign-products"]')))
        return self

    def add_items_to_cart(self):
        cart_locator = 'div#cart span.quantity'
        quantity = random.choice(data_provider.quantities)
        choice = random.choice(data_provider.sizes)
        prev_cart_items = int(self.driver.find_element_by_css_selector(cart_locator).text)
        self.driver.find_element_by_css_selector('div#box-campaign-products div[data-id="1"]').click()

        Select(self.driver.find_element_by_css_selector('select[name="options[Size]"]')).select_by_value(choice)
        self.driver.find_element_by_css_selector('input[name=quantity]').clear()

        self.driver.find_element_by_css_selector('input[name=quantity]').send_keys(str(quantity))
        self.driver.find_element_by_css_selector('button[name=add_cart_product]').click()
        self.driver.find_element_by_css_selector('div[aria-label=Close]').click()

        self.wait.until(ec.text_to_be_present_in_element((By.CSS_SELECTOR, cart_locator), str(prev_cart_items + quantity)))
        new_cart_items = int(self.driver.find_element_by_css_selector(cart_locator).text)
        assert new_cart_items - prev_cart_items == quantity
        return self
