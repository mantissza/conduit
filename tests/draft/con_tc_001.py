from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import random
import string
import sys

chrome_options = Options()
chrome_options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
URL = "http://localhost:1667/#/"

####################################################
#               PYTHON FUNCTIONS
####################################################



####################################################
#                   SELENIUM
####################################################
try:
    driver.get(URL)

finally:
    driver.close()
