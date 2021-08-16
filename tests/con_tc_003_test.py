from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--disable-gpu')


def test_tc_003_cookie():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url = "http://localhost:1667/"

    driver.get(url)
    time.sleep(5)

    excepted_text = "We use cookies to ensure you get the best experience on our website. Learn More..."
    current_text = driver.find_element_by_xpath('//*[@id="cookie-policy-panel"]/div/div[1]').text
    assert current_text == excepted_text

    excepted_decline_btn = "I decline!"
    current_decline_btn = driver.find_element_by_xpath('//*[@class="cookie__bar__buttons__button cookie__bar__buttons__button--decline"]/div').text
    assert current_decline_btn == excepted_decline_btn

    excepted_accept_btn = driver.find_element_by_xpath('//*[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]/div').text
    current_accept_btn = "I accept!"
    assert current_accept_btn == excepted_accept_btn

    excepted_link = "https://cookiesandyou.com/"
    current_link = driver.find_element_by_xpath('//*[@id="cookie-policy-panel"]/div/div[1]/div/a').get_attribute('href')
    assert current_link == excepted_link

    #  Böngésző bezárása
    driver.close()
