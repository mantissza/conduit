from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from pathlib import Path


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


#  Új bejegyzés létrehozásához, valamint a módosítási felület felülírásához egyaránt használható
def fill_the_content_blank(content_list_cp):
    title, subtitle, content, tag = content_list_cp[0], content_list_cp[1], content_list_cp[2], content_list_cp[3]
    #  Új bejegyzés űrlap kitöltése
    input_data_article = [title, subtitle, content, tag]
    for i in range(len(input_data_article)-2):
        title_obj = driver.find_element_by_xpath("//fieldset[@class='form-group'][%i]/input" % (i + 1))
        title_obj.clear()
        title_obj.send_keys(input_data_article[i])
    content_obj = driver.find_element_by_xpath("//fieldset[@class='form-group'][3]/textarea")
    content_obj.clear()
    content_obj.send_keys(input_data_article[2])
    #  Régi tagek törlése
    # tag_old = driver.find_elements_by_xpath('//fieldset[@class="form-group"][4]//i[@class="ti-icon-close"]')
    # print(len(tag_old))
    # for j in range(len(tag_old)):
    #     driver.find_element_by_xpath('//fieldset[@class="form-group"][4]//i[@class="ti-icon-close"][%j]' % (j + 1)).click()
    #     time.sleep(2)
    tag_obj = driver.find_element_by_xpath('//fieldset[@class="form-group"][4]//input')
    tag_obj.clear()
    tag_obj.send_keys(input_data_article[3])
    time.sleep(3)


def new_content(cont_list):
    #  Új bejegyzés létrehozása
    new_article = driver.find_element_by_class_name('ion-compose')
    new_article.click()
    time.sleep(5)

    fill_the_content_blank(cont_list)

    #  Bejegyzés feltöltése
    driver.find_element_by_tag_name("button").click()
    time.sleep(5)


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

    #  Példa bejegyzés létrehozása
    sample_content = ['MathGuy', 'Checkmate, gamer...',
                      'Toxic productivity or self-improvement? Choose wisely.', 'martian']
    new_content(sample_content)

    #  Módosítás folyamata
    mod_btn = driver.find_element_by_xpath("//a[contains(@href,'editor/%s')]" % sample_content[0].lower())
    mod_btn.click()
    time.sleep(5)
    sample_content_mod = ['Barbie', 'Shopping, makeup...', 'No waaay... tldr; duuuh', 'rosegold']
    fill_the_content_blank(sample_content_mod)
    time.sleep(5)
    driver.find_element_by_tag_name("button").click()
    time.sleep(5)

    #  Felülírt/módosított bejegyzésbe került főcím ellenőrzése
    excepted_article_title = sample_content_mod[0]
    current_article_title = driver.find_element_by_xpath('//div[@class="banner"]//h1').text
    assert current_article_title == excepted_article_title

    #  Felülírt/módosított bejegyzésbe került bejegyzés ellenőrzése
    excepted_article_content = sample_content_mod[2]
    current_article_content = driver.find_element_by_xpath('//div[@class="col-xs-12"]//p').text
    assert current_article_content == excepted_article_content

    #  Felülírt/módosított bejegyzésbe került tag ellenőrzése
    excepted_article_tag_list = sample_content_mod[3]
    current_article_tag_list = driver.find_element_by_xpath('//div[@class="tag-list"]/a[2]').text
    assert current_article_tag_list == excepted_article_tag_list

finally:

    #  KIJELENTKEZÉS
    log_out_icon = driver.find_element_by_class_name('ion-android-exit')
    log_out_icon.click()

    #  Böngésző bezárása
    driver.close()
