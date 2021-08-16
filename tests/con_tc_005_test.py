from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--disable-gpu')


def test_tc_005_pages_of_global_feed():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url = "http://localhost:1667/"

    ####################################################
    #               PYTHON FUNCTIONS
    ####################################################

    #  Teszt felhasználó belépésének folyamata
    def sign_in_test_user(user):
        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        sign_in.click()
        for i in range(len(user) - 1):
            driver.find_element_by_xpath("//fieldset[%i]/input" % (i + 1)).send_keys(user[i + 1])
        driver.find_element_by_tag_name("button").click()

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

    #  Összes aktuálisan elérhető oldal száma
    num_of_pages = len(driver.find_elements_by_class_name('page-link'))

    #  Alapértelmezett oldalak helyzete: 1. oldal aktív, az összes többi inaktív.
    for i in range(num_of_pages):
        current_page = driver.find_element_by_xpath('//li[@data-test="page-link-%i"]' % (i + 1))
        if i == 0:
            assert current_page.get_attribute('class') == 'page-item active'
        else:
            assert current_page.get_attribute('class') != 'page-item active'

    #  Lapozzunk el az elérhető oldalak végéig, és ellenőrizzük, hogy mindig a kiválasztott kerül-e kijelölésre
    for i in range(num_of_pages):
        current_page = driver.find_element_by_xpath('//li[@data-test="page-link-%i"]' % (i + 1))
        current_page_link = driver.find_element_by_xpath('//li[@data-test="page-link-%i"]/a' % (i + 1))
        current_page_link.click()
        time.sleep(3)
        #  Ellenőrizzük, hogy az aktuálisan klikkelt link kerül-e kiválasztásra (active class státuszba)
        assert current_page.get_attribute('class') == 'page-item active'

    #  Böngésző bezárása
    driver.close()
