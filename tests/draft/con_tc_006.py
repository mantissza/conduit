from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from keyboard import press


chrome_options = Options()
chrome_options.headless = False
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


####################################################
#                   SELENIUM
####################################################


try:
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

    #  Új bejegyzés létrehozása
    new_article = driver.find_element_by_class_name('ion-compose')
    new_article.click()
    time.sleep(5)

    #  Új bejegyzés űrlap kitöltése
    input_data_article = ['Doge mining', 'Crypto currency and doge', 'Doge doge munch munch', ['dogecoin']]
    for i in range(len(input_data_article)-2):
        driver.find_element_by_xpath("//fieldset[@class='form-group'][%i]/input" % (i + 1)).send_keys(input_data_article[i])
    driver.find_element_by_xpath("//fieldset[@class='form-group'][3]/textarea").send_keys(input_data_article[2])
    driver.find_element_by_xpath('//fieldset[@class="form-group"][4]//input').send_keys(input_data_article[3][0])
    press('enter')

    #  Az imént hozzáadott tag ellenőrzése
    excepted_add_tag = input_data_article[3][0]
    current_add_tag = driver.find_element_by_xpath('//fieldset[@class="form-group"][4]//span').text
    assert current_add_tag == excepted_add_tag

    #  Bejegyzés feltöltése
    driver.find_element_by_tag_name("button").click()
    time.sleep(10)

    #  Feltöltött bejegyzésbe került főcím ellenőrzése
    excepted_article_title = input_data_article[0]
    current_article_title = driver.find_element_by_xpath('//div[@class="banner"]//h1').text
    assert current_article_title == excepted_article_title

    #  Feltöltött bejegyzésbe került bejegyzés ellenőrzése
    excepted_article_content = input_data_article[2]
    current_article_content = driver.find_element_by_xpath('//div[@class="col-xs-12"]//p').text
    assert current_article_content == excepted_article_content

    #  Feltöltött bejegyzésbe került tag ellenőrzése
    excepted_article_tag_list = input_data_article[3][0]
    current_article_tag_list = driver.find_element_by_xpath('//div[@class="tag-list"]/a[1]').text
    assert current_article_tag_list == excepted_article_tag_list

finally:
    #  Böngésző bezárása
    driver.close()
