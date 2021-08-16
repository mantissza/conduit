from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from pathlib import Path


chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--disable-gpu')


def test_tc_007_content_creation_from_input_file():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url = "http://localhost:1667/"

    #  Teszt felhasználó belépésének folyamata
    def sign_in_test_user(user):
        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        sign_in.click()
        for i in range(len(user)-1):
            driver.find_element_by_xpath("//fieldset[%i]/input" % (i + 1)).send_keys(user[i+1])
        driver.find_element_by_tag_name("button").click()

    def new_content(content_list):
        title, subtitle, content, tag = content_list[0], content_list[1], content_list[2], content_list[3]

        #  Új bejegyzés létrehozása
        new_article = driver.find_element_by_class_name('ion-compose')
        new_article.click()
        time.sleep(5)

        #  Új bejegyzés űrlap kitöltése
        input_data_article = [title, subtitle, content, tag]
        for i in range(len(input_data_article)-2):
            driver.find_element_by_xpath("//fieldset[@class='form-group'][%i]/input" % (i + 1)).send_keys(input_data_article[i])
        driver.find_element_by_xpath("//fieldset[@class='form-group'][3]/textarea").send_keys(input_data_article[2])
        driver.find_element_by_xpath('//fieldset[@class="form-group"][4]//input').send_keys(input_data_article[3])

        #  Bejegyzés feltöltése
        driver.find_element_by_tag_name("button").click()
        time.sleep(5)

        #  Feltöltött bejegyzésbe került főcím ellenőrzése
        excepted_article_title = input_data_article[0]
        current_article_title = driver.find_element_by_xpath('//div[@class="banner"]//h1').text
        assert current_article_title == excepted_article_title

        #  Feltöltött bejegyzésbe került bejegyzés ellenőrzése
        excepted_article_content = input_data_article[2]
        current_article_content = driver.find_element_by_xpath('//div[@class="col-xs-12"]//p').text
        assert current_article_content == excepted_article_content

        #  Feltöltött bejegyzésbe került tag ellenőrzése
        excepted_article_tag_list = input_data_article[3]
        current_article_tag_list = driver.find_element_by_xpath('//div[@class="tag-list"]/a[1]').text
        assert current_article_tag_list == excepted_article_tag_list

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

    #  Kiíratjuk listába a content.txt-ben szereplő elemeket, hogy feldolgozhatóvá váljon.
    list_of_contents = []
    TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'
    f = open(TEST_DATA_DIR / 'content.txt', 'r')
    for i in range(int(f.readline())):
        elem = f.readline().replace('\n', '')
        elem_list = elem.split(';')
        list_of_contents.append(elem_list)

    #  Tartalom feldolgozása listából.
    for i in range(len(list_of_contents)):
        new_content(list_of_contents[i])

    #  KIJELENTKEZÉS
    log_out_icon = driver.find_element_by_class_name('ion-android-exit')
    log_out_icon.click()

    #  Böngésző bezárása
    driver.close()
