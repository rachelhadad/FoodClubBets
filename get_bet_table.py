from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import constants

USERNAME = os.environ.get("neo_p1nk")
PASSWORD = os.environ.get("neo_p1nk_pw")
chrome_driver_path = constants.chrome_driver_path

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.maximize_window()


def get_betting_table():
    driver.get("http://www.neopets.com/")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/a[2]/button").click()
    time.sleep(2)
    username = driver.find_element_by_name("username")
    username.send_keys(USERNAME)
    time.sleep(1)
    password = driver.find_element_by_id("loginPassword")
    password.send_keys(PASSWORD + Keys.ENTER)
    time.sleep(2)

    driver.get("http://www.neopets.com//~coldBlackWind")

    bet_page_html = driver.page_source
    with open("bet_table.html", "w") as bet_table_file:
        bet_table_file.write(bet_page_html)
    return driver



