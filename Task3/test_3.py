from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

def test_3():
    driver =webdriver.Chrome()
    driver.implicitly_wait(2)
    wait = WebDriverWait(driver, 4)
    driver.get('http://localhost/litecart/admin')

    driver.find_element_by_css_selector('input[class=form-control][name=username]').send_keys('admin')
    driver.find_element_by_css_selector('input[class=form-control][name=password]').send_keys('admin')

    driver.find_element_by_css_selector('button[class="btn btn-default"][name=login]').click()

    #wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'i[class="fa fa-sign-out fa-lg"]')))
    driver.find_element_by_css_selector('i[class="fa fa-sign-out fa-lg"]').click()

    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'body div[id=box-login]')))
    driver.quit()