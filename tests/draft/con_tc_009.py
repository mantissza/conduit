from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
url = "http://localhost:1667/"


####################################################
#               PYTHON FUNCTIONS
####################################################

#  Létezik e a keresett xpath? fg
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

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
    sample_content = ['Math Guy', 'Checkmate, gamer...',
                      'Toxic productivity or self-improvement? Choose wisely.', 'martian']
    new_content(sample_content)

    #  Létezik a Törlésre szolgáló gomb?
    is_exist_delete_btn = check_exists_by_xpath('//button/span[contains(text(), "Delete")]')
    assert is_exist_delete_btn

    #  Létrehozást követő törlés folyamata
    del_btn = driver.find_element_by_xpath('//button[contains(@class,"btn-outline-danger")]')
    del_btn.click()
    time.sleep(5)

    #  Saját bejegyzések között ellenőrizzük, hogy valóban törölve lett-e a tétel.
    user_menu = driver.find_element_by_xpath('//a[contains(@href,"%s")]' % test_username)
    user_menu.click()
    time.sleep(5)

    #  A bejegyzés címét alakítsuk sub url formátumúvá
    format_title_to_href = sample_content[0].lower().replace(' ', '-')

    #  A felhasználó egyéni feedjére belépve ellenőrizzük, hogy létezik-e még post az imánt megszűnt url-el.
    is_exist_deleted_post = check_exists_by_xpath('//a[contains(@href,"%s")]' % format_title_to_href)
    assert is_exist_deleted_post


finally:

    #  KIJELENTKEZÉS
    log_out_icon = driver.find_element_by_class_name('ion-android-exit')
    log_out_icon.click()

    #  Böngésző bezárása
    driver.close()
