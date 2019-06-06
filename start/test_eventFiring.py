from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
import pytest


@pytest.fixture
def driver(request):
    wd = EventFiringWebDriver(webdriver.Chrome(), MyListener())
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd

def test_event(driver):
    driver.get('https://google.com.ua')
    driver.find_element_by_name('q123').send_keys('webdriver', Keys.RETURN)
    #driver.find_element_by_name('btnG').click()
    WebDriverWait(driver, 3).until(ec.title_is('webdriver - Пошук Google'))

class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(by, value)
    def after_find(self, by, value, driver):
        print(by, value, 'found')
    def on_exception(self, exception, driver):
        print(exception)
        driver.get_screenshot_as_file('screen.png')
    def before_quit(self, driver):
        print('Finished')