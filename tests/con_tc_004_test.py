from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--disable-gpu')


def test_tc_004_data_list():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url = "http://localhost:1667/"

    ####################################################
    #               PYTHON FUNCTIONS
    ####################################################

    #  Teszt felhasználó belépésének folyamata
    def sign_in_test_user(user):
        time.sleep(5)
        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        sign_in.click()
        for i in range(len(user)-1):
            driver.find_element_by_xpath("//fieldset[%i]/input" % (i + 1)).send_keys(user[i+1])
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

    #  Bejelentkezés sikerének ellenőrzése.
    excepted_username = test_user[0]
    current_username = driver.find_element_by_xpath("//*[@class='nav-item'][4]/a").text
    assert current_username == excepted_username

    #  Bal felső sarokban található conduit ikon vizsgálata, főoldalra navigálás
    excepted_conduit_link = "http://localhost:1667/#/"
    current_conduit_link = driver.find_element_by_xpath('//*[@id="app"]/nav/div/a').get_attribute('href')
    print(current_conduit_link)
    assert current_conduit_link == excepted_conduit_link
    driver.find_element_by_xpath('//*[@id="app"]/nav/div/a').click()
    time.sleep(5)

    #  Egy oldalon megjelenő maximális bejegyzések számának vizsgálata
    excepted_page_per_content = 11
    current_page_per_content = len(driver.find_elements_by_class_name('article-preview'))
    assert current_page_per_content == excepted_page_per_content

    #  Megjelenő bejegyzések címeinek összevetése egy külső txt listával.
    current_content_title_list = []
    for i in range(current_page_per_content):
        elem = driver.find_element_by_xpath('//*[@class="article-preview"][%i]/a/h1' % (i + 1)).text
        current_content_title_list.append(elem)

    excepted_content_title_list = []
    f = open('titles.txt', 'r')
    for i in range(int(f.readline())):
        elem = f.readline().replace('\n', '')
        excepted_content_title_list.append(elem)

    #  A két lista hosszának összevetése
    assert len(current_content_title_list) == len(excepted_content_title_list)

    #  A két lista tartalmának összevetése
    for i in range(len(current_content_title_list)):
        #  print(current_content_title_list[i] + "==" + excepted_content_title_list[i])
        assert current_content_title_list[i] == excepted_content_title_list[i]

    #  Böngésző bezárása
    driver.close()
