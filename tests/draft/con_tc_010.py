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

    # A felhasználó profilján található bejegyzések mentése fájlba
    user_profile_menu = driver.find_element_by_xpath("//*[contains(@href,'%s')]" % test_username)
    user_profile_menu.click()
    time.sleep(5)

    #  Az első oldalon található bejegyzésekre vonatkozó adatok kigyűjtése listába
    #  Listák listája (Főcím és url)
    list_of_contents = []
    title_list = driver.find_elements_by_xpath('//div[@class="profile-page"]//a[contains(@href,"articles")]/h1')
    link_list = driver.find_elements_by_xpath('//div[@class="profile-page"]//a[contains(@href,"articles")]')

    #  Lista feltöltése elemekkel
    for i in range(len(title_list)):
        list_of_contents.append([title_list[i].text, link_list[i].get_attribute('href')])

    #  Lista tartalmának file-ba való kiíratása (sava_data.txt)
    #  Megj.: Alkalmazott szeparátor: ';' Az első sorban a listaelemek darabszáma van feltüntetve
    # #  TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'
    # #  f = open(TEST_DATA_DIR / 'titles.txt', 'r')
    with open('save_data.txt', 'w') as f:
        f.write("%s\n" % str(len(list_of_contents)))
        for elem in list_of_contents:
            f.write("%s;%s\n" % (elem[0], elem[1]))

    #  Címhez kapcsolt linkrészlet ellenőrzése.
    #  (A link a megadott címből képződik oly módon,
    #  hogy át van alakítva kiskapitálissá, és ' ' helyett '-' karakter szerepel.
    for i in range(len(list_of_contents)):
        temp_sublist = list_of_contents[i]
        temp_formatted_title = temp_sublist[0].lower().replace(' ', '-')
        temp_formatted_link = str(temp_sublist[1].lower().replace(url + '#/articles/', ''))
        # print(temp_formatted_title, '==', temp_formatted_link)
        assert temp_formatted_title == temp_formatted_link


finally:
    print('The end')
    # #  KIJELENTKEZÉS
    # log_out_icon = driver.find_element_by_class_name('ion-android-exit')
    # log_out_icon.click()
    #
    # #  Böngésző bezárása
    # driver.close()
