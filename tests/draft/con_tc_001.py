from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
import string


chrome_options = Options()
chrome_options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
url = "http://localhost:1667/"


####################################################
#               PYTHON FUNCTIONS
####################################################


#  Random karaktersor generátor.
def charset_rand(length):
    result = ''
    while len(result) != length:
        result += random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase)  # charset
    return result


#  Új felhasználó hozzáadásának művelete
def add_new_user(user):
    sign_up = driver.find_element_by_xpath("//a[@href='#/register']")
    sign_up.click()
    for i in range(len(user)):
        driver.find_element_by_xpath("//fieldset[%i]/input" % (i + 1)).send_keys(user[i])
    driver.find_element_by_tag_name("button").click()


####################################################
#                   SELENIUM
####################################################


try:
    driver.get(url)
    time.sleep(5)

    #  Bemeneti értékek
    domain = random.choice(['com', 'hu', 'ru', 'de', 'cz'])
    rand_username = charset_rand(random.randint(6, int(15)))
    rand_email = (charset_rand(random.randint(6, int(15))) + '@' + charset_rand(random.randint(6, int(15))) + '.' + domain).lower()
    rand_password = charset_rand(random.randint(6, int(30)))
    rand_user = [rand_username, rand_email, rand_password]
    # print(randUser)

    #  Űrlap kitöltése
    add_new_user(rand_user)

    #  Töltőképernyő miatti várakozás
    time.sleep(5)

    #  Sikeres regisztrációról szóló popup üzenet elemeinek ellenőrzése
    excepted_title = "Welcome!"
    excepted_text = "Your registration was successful!"
    current_title = driver.find_element_by_xpath("//*[@class='swal-title']").text
    current_text = driver.find_element_by_xpath("//*[@class='swal-text']").text
    assert current_title == excepted_title
    assert current_text == excepted_text
    driver.find_element_by_xpath("//*[@class='swal-button swal-button--confirm']").click()

    #  Az új felhasználó automatikusan bejelentkezik regisztrációt követően. => Bejelentkezés sikerének ellenőrzése.
    excepted_username = rand_user[0]
    current_username = driver.find_element_by_xpath("//*[@class='nav-item'][4]/a").text
    assert current_username == excepted_username

finally:
    #  KIJELENTKEZÉS
    log_out_icon = driver.find_element_by_class_name('ion-android-exit')
    log_out_icon.click()
    time.sleep(2)
    #  Böngésző bezárása
    driver.close()
