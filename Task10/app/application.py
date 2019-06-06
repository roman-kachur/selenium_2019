from selenium import webdriver
from Task10.pages.home_page import HomePage
from Task10.pages.campaign_products_page import CampaignProductsPage
from Task10.pages.cart_page import CartPage
from Task10.tests import data_provider
import pytest
import time

class LitecartApp:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.base_url = 'http://localhost/litecart'
        self.home_page = HomePage(self.driver)
        self.campaign_products_page = CampaignProductsPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def campaign_products(self):
        self.campaign_products_page.open(self.base_url)

    def add_items_to_cart(self):
        for item in range(data_provider.items_to_add):
            self.campaign_products_page.add_items_to_cart()

    def purge_cart(self):
        self.cart_page.purge()

    def quit(self):
        time.sleep(3)
        self.driver.quit()
