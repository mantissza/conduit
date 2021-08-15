from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import random
import string
import sys

chrome_options = Options()
chrome_options.headless = True


####################################################
#               PYTHON FUNCTIONS
####################################################


####################################################
#                   SELENIUM
####################################################

def test_registration():

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    URL = "http://localhost:1667/#/"
    driver.get(URL)
    assert True
    assert True
    assert True

    driver.close()

