import time
from selenium.webdriver.common.keys import Keys
import constants
from pyrobot import Robot, Keys
import os

robot = Robot()
neo_pin = os.environ.get("neo_pin")


# Collect daily interest, if it hasn't already been collected, and withdraw enough neopoints to place bets
def go_to_bank(driver, bet_amount_10x):
    driver.get("http://www.neopets.com/bank.phtml")
    time.sleep(2)

    try:
        collect_interest = driver.find_element_by_xpath(constants.collect_interest_xpath)
        collect_interest.click()
        time.sleep(2)
        print("Collected interest.")
    except Exception:
        print("Interest not collected.")
    finally:
        withdrawal_input = driver.find_element_by_xpath(constants.withdrawal_input_xpath)
        withdrawal_input.send_keys(bet_amount_10x)

        # Insert pin, if account is protected by pin
        # pin_input = driver.find_element_by_xpath(constants.pin_input_xpath)
        # pin_input.send_keys(neo_pin)

        time.sleep(1)
        driver.find_element_by_xpath(constants.withdrawal_button_xpath).click()
        time.sleep(2)
        robot.press_and_release(Keys.enter)
        time.sleep(3)
