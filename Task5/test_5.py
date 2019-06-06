from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

import time

def is_element_present(driver, locator):
    return len(driver.find_elements_by_xpath(locator)) > 0

def test_5():
    driver =webdriver.Chrome()
    driver.implicitly_wait(2)
    wait = WebDriverWait(driver, 4)

    driver.get('http://localhost/litecart')
    campaign_css = 'body div ul li a[href="#campaign-products"] '
    driver.find_element_by_css_selector(campaign_css).click()


    first_product_css = 'div#main div#box-campaign-products div[data-id="1"] '
    first_product_name_css = first_product_css + 'div.name'
    first_product_regprice_css = first_product_css + 's.regular-price'
    first_product_disprice_css = first_product_css + 'strong.campaign-price'

    first_product_main_name = driver.find_element_by_css_selector(first_product_name_css).get_attribute('textContent')
    first_product_main_regprice = driver.find_element_by_css_selector(first_product_regprice_css).get_attribute(
        'textContent')
    first_product_main_disprice = driver.find_element_by_css_selector(first_product_disprice_css).get_attribute(
        'textContent')
    first_product_main_regprice_style = (
        driver.find_element_by_css_selector(first_product_regprice_css).value_of_css_property('color'),
        driver.find_element_by_css_selector(first_product_regprice_css).value_of_css_property('text-decoration-line') )

    driver.find_element_by_css_selector(first_product_css).click()
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#box-product.box')))

    first_product_item_name = driver.find_element_by_css_selector('h1.title').get_attribute('textContent')
    first_product_item_regprice = driver.find_element_by_css_selector('#box-product del.regular-price').get_attribute('textContent')
    first_product_item_disprice = driver.find_element_by_css_selector('div#box-product strong.campaign-price').get_attribute(
        'textContent')
    first_product_item_regprice_style = (
        driver.find_element_by_css_selector('#box-product del.regular-price').value_of_css_property('color'),
        driver.find_element_by_css_selector('#box-product del.regular-price').value_of_css_property('text-decoration-line'))


    time.sleep(3)
    driver.find_element_by_css_selector('body div[aria-label="Close"]').click()
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#page')))

    assert first_product_main_name == first_product_item_name
    assert first_product_main_regprice == first_product_item_regprice
    assert first_product_main_disprice == first_product_item_disprice
    assert first_product_main_regprice_style == first_product_item_regprice_style

    time.sleep(3)
    driver.quit()