from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import random
import string
import sys


####################################################
#  PYTHON FUNCTIONS
####################################################


####################################################
#               FUNCTION TEST
####################################################


####################################################
#         LOGIN
####################################################

def test_TC01_regist():
    opt = Options()
    opt.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
    URL = "http://localhost:1667/#/"
    driver.get(URL)
    assert True


####################################################
#       LOG OUT
####################################################
# logout_btn = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li/a')
#
# logout_btn.click()

####################################################
# The END of the whole process #
####################################################

#  driver.close()

