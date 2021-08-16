from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import random
import string


chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--disable-gpu')


def test_tc_001_registration():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url = "http://localhost:1667/"

    #  Random karaktersor generátor.
    def charset_rand(length):
        result = ''
        while len(result) != length:
            result += random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase)  # charset
        return result

    #  Új felhasználó hozzáadásának művelete
    def add_new_user(user):
        for i in range(len(user)):
            driver.find_element_by_xpath("//fieldset[%i]/input" % (i + 1)).send_keys(user[i])
        driver.find_element_by_tag_name("button").click()

    #  Létezik e a keresett xpath? fg
    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    driver.get(url)
    time.sleep(5)

    #  Bemeneti értékek
    #  Fontos: Password must be 8 characters long and include 1 number, 1 uppercase letter, and 1 lowercase letter.
    domain = random.choice(['com', 'hu', 'ru', 'de', 'cz'])
    rand_username = charset_rand(random.randint(6, int(15)))
    rand_email = (charset_rand(random.randint(6, int(15))) + '@' +
                  charset_rand(random.randint(6, int(15))) + '.' + domain).lower()
    rand_password = charset_rand(random.randint(8, int(30))) + '1aA'
    rand_user = [rand_username, rand_email, rand_password]
    # print(randUser)

    time.sleep(5)
    sign_up = driver.find_element_by_xpath("//*[contains(@href,'register')]")
    sign_up.click()
    time.sleep(5)
    sign_up.click()
    #  sign_up = driver.find_element_by_xpath("//a[@href='#/register' and @class='nav-link']")
    #  sign_up = driver.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[3]/a')
    if check_exists_by_xpath("//i[contains(@class,'ion-android-exit')]"):
        driver.find_element_by_class_name('ion-android-exit').click()
        time.sleep(5)
        sign_up.click()

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
    time.sleep(2)

    #  Az új felhasználó automatikusan bejelentkezik regisztrációt követően. => Bejelentkezés sikerének ellenőrzése.
    excepted_username = rand_user[0]
    current_username = driver.find_element_by_xpath("//*[@class='nav-item'][4]/a").text
    assert current_username == excepted_username

    #  KIJELENTKEZÉS
    log_out_icon = driver.find_element_by_class_name('ion-android-exit')
    log_out_icon.click()
    time.sleep(2)

    #  Böngésző bezárása
    driver.close()
