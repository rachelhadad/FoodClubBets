from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import os
import time
import constants
from get_bet_table import get_betting_table
from get_winnings import get_winnings
import sqlite3
from go_to_bank import go_to_bank
from random import randint

chrome_driver_path = constants.chrome_driver_path
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
con = sqlite3.connect('neopets.db')
cur = con.cursor()


def get_betting_info():
    with open(os.environ.get('bet_table_path')) as bet_table:
        soup = BeautifulSoup(bet_table, 'html.parser')
    # Make blank dict for {arenas: contenders}
    bet_dictionary = {f"bet{i}": {'arenas': [], 'contenders': []} for i in range(1, 11)}
    combined_dictionary = {f"bet{i}": {} for i in range(1, 11)}
    for n in range(1, 11):
        # Get arenas as list for bet_arenas (to use in combined_dictionary) and bet_dictionary
        bet = soup.find_all("table")[1].find_all("tr")[n + 1].find_all("td")[1]
        bet_arenas_list = soup.find_all("table")[1].find_all("tr")[n + 1].find_all("td")[1].find_all("b")
        bet_arenas = [arena.text for arena in bet_arenas_list]
        for num in range(len(bet_arenas)):
            bet_dictionary[f"bet{n}"]["arenas"].append(bet_arenas[num])

        # Get contenders as list for bet_contenders (to use in combined_dictionary) and bet_dictionary
        bet_string = str(bet)
        bet_string = bet_string.split("<br/>")
        bet_string2 = []
        for each in bet_string:
            bet_string2.append(each.split("</b>: "))
        bet_contenders = [bet_string2[num][1] for num in range(len(bet_string2) - 1)]
        for num in range(len(bet_contenders)):
            bet_dictionary[f"bet{n}"]["contenders"].append(bet_contenders[num])
            combined_dictionary[f"bet{n}"].update({bet_arenas[i]: bet_contenders[i] for i in range(len(bet_arenas))})
    return bet_dictionary, combined_dictionary


# Get arena, contenders, and bet amount, then place each bet
# Time_sleep implemented throughout for purpose of making function behave at a more human pace
def place_bets(driver):
    # Get betting info
    result = get_betting_info()
    bet_dictionary = result[0]
    combined_dictionary = result[1]

    # Confirm enough np on hand to place bets. If not, go to bank
    driver.get("http://www.neopets.com/pirates/foodclub.phtml?type=bet")
    bet_amount = driver.find_element_by_xpath(constants.GET_BET_AMOUNT_XPATH).text
    bet_amount_10x = int(bet_amount) * 10
    fetch_np_on_hand = driver.find_element_by_xpath(constants.np_on_hand_xpath).text
    np_on_hand = int(fetch_np_on_hand.replace(',', ''))
    if np_on_hand < bet_amount_10x:
        go_to_bank(driver, bet_amount_10x)
        # Place bets
        driver.get("http://www.neopets.com/pirates/foodclub.phtml?type=bet")
    time.sleep(randint(1, 4))

    # Click checkbox only for arenas that are included in each bet
    for n in range(1, 11):
        arena_names = bet_dictionary[f"bet{n}"]["arenas"]
        # Scroll to bottom of page so everything is visible to click
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        # Click checkbox and select contender
        for arena in arena_names:
            driver.find_element_by_xpath(constants.arena_xpath_dictionary[arena]["checkbox"]).click()
            time.sleep(randint(1, 3))
            # Find contender dropbox
            dropdown = Select(driver.find_element_by_xpath(constants.arena_xpath_dictionary[arena]["dropbox"]))
            time.sleep(randint(1, 3))
            # Match contender with arena, select by contender's value
            dropdown.select_by_value(constants.CONTENDER_VALUES[combined_dictionary[f"bet{n}"][arena]])
        # Get and enter bet amount
        place_bet_input = driver.find_element_by_xpath(constants.PLACE_BET_AMOUNT_XPATH)
        place_bet_input.send_keys(bet_amount)
        time.sleep(randint(1, 4))
        place_bet_button = driver.find_element_by_xpath(constants.PLACE_BET_BUTTON_XPATH)
        place_bet_button.click()
        print(f"Bet {n} placed.")
        time.sleep(randint(1, 4))
        if n <= 9:
            place_bet_link = driver.find_element_by_xpath(constants.place_bet_link_xpath)
            place_bet_link.click()
            time.sleep(randint(1, 4))
        else:
            time.sleep(randint(1, 4))
    # Insert bet info into database
    amount_bet = int(bet_amount)*10
    round_number = driver.find_element_by_xpath(constants.round_number).text
    cur.execute("INSERT INTO food_club VALUES (?, ?, ?, ?, ?, ?, ?)",
                (round_number, constants.today, amount_bet, "", "", "", ""))

    # Get boochi_target winnings to compare to my winnings (in hopes of avoiding FOMO)
    driver.get("http://www.neopets.com//~boochi_target")
    boochi_page_html = driver.page_source
    with open("boochi_target.html", "w") as boochi_page_file:
        boochi_page_file.write(boochi_page_html)
    with open("boochi_target.html", "r") as boochi_page_file:
        soup = BeautifulSoup(boochi_page_file, "html.parser")
        table = soup.find_all("b")[2].text
        boochi_winnings_odds_split = table.split(":")[0]
        if boochi_winnings_odds_split == "skipped" or boochi_winnings_odds_split == "Skipped":
            boochi_winnings_odds = int(0)
        else:
            boochi_winnings_odds = int(boochi_winnings_odds_split)
    cur.execute("UPDATE food_club SET boochi_winnings_odds = ? WHERE date = ?",
                (boochi_winnings_odds, constants.yesterday,))
    con.commit()

    # Print database information
    bets_data = cur.execute("SELECT * FROM food_club ORDER BY round DESC LIMIT 2")
    data = bets_data.fetchall()
    print(f"Data: {data}")
    fetch_winnings_sum = cur.execute("SELECT SUM(winnings_amount) FROM food_club").fetchone()
    winnings_sum = int(fetch_winnings_sum[0])
    print("Total winnings: " + "{:,}".format(winnings_sum))
    fetch_cost_sum = cur.execute("SELECT SUM(amount_bet) FROM food_club").fetchone()
    cost_sum = int(fetch_cost_sum[0])
    print("Total bets: " + "{:,}".format(cost_sum))
    delta_cost = winnings_sum - cost_sum
    print("Delta: " + "{:,}".format(delta_cost))
    roi = delta_cost / cost_sum
    print("Roi: " + "{0:.0%}".format(roi))
    fetch_winnings_odds_sum = cur.execute("SELECT SUM(winnings_odds) FROM food_club").fetchone()
    fethch_boochi_winnings_odds_sum = cur.execute("SELECT SUM(boochi_winnings_odds) FROM food_club").fetchone()
    print(f"Sum of winnings odds: {fetch_winnings_odds_sum}")
    print(f"Sum of boochi odds: {fethch_boochi_winnings_odds_sum}")


chauffeur = get_betting_table()
get_winnings(chauffeur)
place_bets(chauffeur)
con.close()
