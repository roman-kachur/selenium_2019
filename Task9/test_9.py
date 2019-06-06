from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
import time
import pytest

class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        pass

    def after_find(self, by, value, driver):
        pass

    def on_exception(self, exception, driver):
        print(exception)
        driver.get_screenshot_as_file('screen-'+str(int(time.time()*1000))+'.png')

    def before_quit(self, driver):
        print('Finished')

DEFAULT_TIMEOUT = 2

@pytest.fixture
def driver(request):
    wd = EventFiringWebDriver(webdriver.Chrome(), MyListener())
    wd.implicitly_wait(DEFAULT_TIMEOUT)
    request.addfinalizer(wd.quit)
    return wd

def is_element_present(driver, locator):
    return len(driver.find_elements_by_xpath(locator)) > 0

def is_not_element_present(driver, locator):
    try:
        driver.implicitly_wait(0)
        return len(driver.find_elements_by_xpath(locator)) == 0
    finally:
        driver.implicitly_wait(DEFAULT_TIMEOUT)

def test_9(driver):
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT * 2)
    driver.get('http://localhost/litecart/admin')

    driver.find_element_by_css_selector('input[class=form-control][name=username]').send_keys('admin')
    driver.find_element_by_css_selector('input[class=form-control][name=password]').send_keys('admin')
    driver.find_element_by_css_selector('button[class="btn btn-default"][name=login]').click()

    root_locator = '//ul[@id="box-apps-menu"]'
    wait.until(ec.visibility_of_element_located((By.XPATH, root_locator)))

    outer_box = root_locator + '/li'
    outer_items = len(driver.find_elements_by_xpath(outer_box))

    for item in range(1, outer_items + 1):
        category = outer_box + '[' + str(item) + ']'
        driver.find_element_by_xpath(category).click()
        assert is_element_present(driver, '//h1')
        print(category)

        subcategory = category + '/ul'
        if not is_not_element_present(driver, subcategory):
            inner_box = subcategory + '/li'
            inner_items = len(driver.find_elements_by_xpath(inner_box))
            for sub_item in range(1, inner_items + 1):
                subitem = inner_box + '[' + str(sub_item) + ']'
                driver.find_element_by_xpath(subitem).click()
                assert is_element_present(driver, '//h1')
                print('\t',subitem)

    driver.find_element_by_css_selector('i[class="fa fa-sign-out fa-lg"]').click()
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'body div[id=box-login]')))
    driver.quit()