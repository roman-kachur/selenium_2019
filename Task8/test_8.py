from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
import time
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
        #driver.get_screenshot_as_file('screen-'+str(int(time.time()*1000))+'.png')


    def before_quit(self, driver):
        print('Finished')


def test_8(driver):
    wait = WebDriverWait(driver, 4)
    driver.get('http://localhost/litecart/admin')

    driver.find_element_by_css_selector('input[class=form-control][name=username]').send_keys('admin')
    driver.find_element_by_css_selector('input[class=form-control][name=password]').send_keys('admin')
    driver.find_element_by_css_selector('button[class="btn btn-default"][name=login]').click()

    driver.find_element_by_css_selector('body div ul li#app-countries').click()
    add_new_country = driver.find_element_by_css_selector('a[class="btn btn-default"]')
    assert add_new_country.text == 'Add New Country'
    add_new_country.click()

    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
    ex_links = driver.find_elements_by_css_selector('a[href] i[class="fa fa-external-link"]')
    assert len(ex_links) == 9

    current_tab = driver.current_window_handle
    current_tabs = driver.window_handles

    for link in ex_links:
        link.click()
        wait.until(ec.new_window_is_opened(current_tabs))
        updated_tabs = driver.window_handles
        new_tab = [tab for tab in updated_tabs if tab not in current_tabs][0]
        driver.switch_to_window(new_tab)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
        current_tabs = updated_tabs
        driver.switch_to.window(current_tab)

    while True:
        external_tabs = [tab for tab in driver.window_handles if tab != current_tab]
        if not external_tabs:
            driver.switch_to.window(current_tab)
            break
        driver.switch_to.window(external_tabs[-1])
        driver.close()

    driver.find_element_by_css_selector('i[class="fa fa-sign-out fa-lg"]').click()
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'body div[id=box-login]')))

