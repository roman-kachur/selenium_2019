from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def purge(self):
        cart_locator = 'div#cart span.quantity'
        self.driver.find_element_by_css_selector('div#cart').click()
        items = len(self.driver.find_elements_by_css_selector('table tr.item'))
        for i in range(items):
            table = self.driver.find_element_by_css_selector('table[class*="items table"]')
            remove_buttons = self.driver.find_elements_by_css_selector('tr.item button[name=remove_cart_item]')
            assert len(remove_buttons) > 0
            remove_buttons[0].click()
            self.wait.until(ec.staleness_of(table))

        self.driver.find_element_by_css_selector('p a[href]').click()
        assert int(self.driver.find_element_by_css_selector(cart_locator).text) == 0