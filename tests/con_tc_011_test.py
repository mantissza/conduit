from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import tempfile
from pathlib import Path
from unittest.mock import patch


chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--disable-gpu')


def test_tc_011_logout():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url = "http://localhost:1667/"

    ####################################################
    #               PYTHON FUNCTIONS
    ####################################################

    #  Teszt felhasználó belépésének folyamata
    def sign_in_test_user(user):
        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        sign_in.click()
        for i in range(len(user)-1):
            driver.find_element_by_xpath("//fieldset[%i]/input" % (i + 1)).send_keys(user[i+1])
        driver.find_element_by_tag_name("button").click()

    def navbar_check(excepted_length, filename):
        #  Egy oldalon megjelenő maximális menüpontok számának vizsgálata
        excepted_nav_item = excepted_length
        current_nav_item = len(driver.find_elements_by_class_name('nav-link'))
        assert current_nav_item == excepted_nav_item

        #  Megjelenő bejegyzések címeinek összevetése egy külső txt listával.
        current_nav_item_list = []
        for i in range(current_nav_item):
            # elem = driver.find_element_by_xpath('//*[@class="nav-link"][%i]' % (i + 1)).text
            elem = driver.find_elements_by_class_name('nav-link')[i].text
            current_nav_item_list.append(elem)

        excepted_nav_item_list = []
        f = open(filename, 'r')
        for i in range(int(f.readline())):
            elem = f.readline().replace('\n', '')
            excepted_nav_item_list.append(elem)

        #  A két navigációs elemeket tartalmazó lista hosszának összevetése
        assert len(current_nav_item_list) == len(excepted_nav_item_list)

        #  A két navigációs elemeket tartalmazó lista tartalmának összevetése
        for i in range(len(current_nav_item_list)):
            #  print(current_nav_item_list[i] + "==" + excepted_nav_item_list[i])
            assert current_nav_item_list[i] == excepted_nav_item_list[i]

    ####################################################
    #                   SELENIUM
    ####################################################

    driver.get(url)
    time.sleep(5)

    #  Bemeneti értékek
    test_username = 'testuser1'
    test_email = 'testuser1@example.com'
    test_password = 'Abcd123$'
    test_user = [test_username, test_email, test_password]

    #  Űrlap kitöltése
    sign_in_test_user(test_user)

    #  Töltőképernyő miatti várakozás
    time.sleep(5)

    #  Bejelentkezés sikerének ellenőrzése
    excepted_username = test_user[0]
    current_username = driver.find_element_by_xpath("//*[@class='nav-item'][4]/a").text
    assert current_username == excepted_username

    #  Bejelentkezést követő ellenőrzés
    TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'
    navbar_check(7, TEST_DATA_DIR / 'navitems_login.txt')

    #  KIJELENTKEZÉS ikonra kattint
    log_out_icon = driver.find_element_by_class_name('ion-android-exit')
    log_out_icon.click()

    #  Kijelentkezést követő ellenőrzés
    navbar_check(4, TEST_DATA_DIR / 'navitems_logout.txt')

    #  Böngésző bezárása
    driver.close()
