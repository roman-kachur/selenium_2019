from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.microsoft import EdgeDriverManager

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

def test_google():
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver.Edge(EdgeDriverManager().install())
    
    #driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    #driver = webdriver.Ie('c:\\ProgramData\\msedgedriver.exe')

    driver.get('https://google.com.ua')
    driver.find_element_by_name('q').send_keys('webdriver', Keys.RETURN)
    #driver.find_element_by_name('btnG').click()
    WebDriverWait(driver, 3).until(ec.title_is('webdriver - Пошук Google'))
    driver.quit()


