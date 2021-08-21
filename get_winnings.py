import sqlite3
import datetime
from bs4 import BeautifulSoup
import re
import constants
import os

# This is the table, for reference
# cur.execute('''CREATE TABLE food_club
#                 (date TEXT,
#                 round TEXT,
#                 amount_bet INT,
#                 winnings_odds INT,
#                 winnings_amount INT,
#                 roi INT,
#                 boochi_winnings_odds INT)''')

con = sqlite3.connect('neopets.db')
cur = con.cursor()


def input_winnings(round_number, winnings_odds, winnings_amount, roi):
    cur.execute("UPDATE food_club SET winnings_odds = ?, winnings_amount = ?, roi = ? WHERE round = ?",
                (winnings_odds, winnings_amount, roi, round_number))
    con.commit()
    print("Input winnings into database successfully.")


# Determine if there are winnings from previous round. If so, collect. Then input winnings or not into database
def get_winnings(driver):
    driver.get("http://www.neopets.com/pirates/foodclub.phtml?type=collect")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # # Get round number based on date
    # base_round = 8047
    # base_date = datetime.date(2021, 5, 19)
    # delta_date = constants.today - base_date
    # time_now = datetime.datetime.now().time()
    # gates_closed = datetime.time(15, 0, 0, 0)
    # if time_now < gates_closed:
    #     round_number = base_round + delta_date.days
    # else:
    #     round_number = base_round + delta_date.days + 1
    # print(round_number)
    no_winnings_text = driver.find_element_by_xpath(constants.no_winnings_xpath).text
    previous_round = cur.execute("SELECT round FROM food_club ORDER BY round DESC LIMIT 1").fetchone()[0]
    # Assign values to variables based on if there are winnings or not
    if no_winnings_text == "You do not have any winning bets!":
        winnings_amount = 0
        winnings_odds = 0
        roi = 0
        input_winnings(previous_round, winnings_odds, winnings_amount, roi)
    # Save HTML of winnings page to parse and get numbers to assign to variables (to input into db)
    else:
        winnings_page_html = driver.page_source
        with open("winnings.html", "w", encoding="utf8") as winnings_table:
            winnings_table.write(winnings_page_html)
        with open(os.environ.get("winnings_html_path"), encoding="utf8") as winnings_table:
            soup = BeautifulSoup(winnings_table, 'html.parser')
            winnings_odds_list = soup.find_all("table")[8].find_all("tr")
            winnings_odds = 0
            # Loop through tds in case there are multiple winning bets from previous round
            for n in range(2, len(winnings_odds_list) - 1):
                winnings_odds_list = soup.find_all("table")[8].find_all("tr")[n].find_all("td")[3].text
                winnings_odds_split = int(winnings_odds_list.split(":")[0])
                winnings_odds += winnings_odds_split
            find_total_winnings = re.search("(Total Winnings.+\D)([0-9]+)(\sNP)", str(soup))
            total_winnings = int(find_total_winnings.group(2))
            print(f"Winnings: f{total_winnings}")
        fetch_bet_tuple = cur.execute("SELECT * FROM food_club ORDER BY round DESC LIMIT 1")
        fetch_bet = fetch_bet_tuple.fetchone()
        print(f"Previous bet: {fetch_bet}")
        bet_amount = fetch_bet[0]
        roi = round(((total_winnings - bet_amount) / total_winnings) * 100, 2)
        # Call function input_winnings to insert the variables we just assigned
        input_winnings(previous_round, winnings_odds, total_winnings, roi)
        # Collect winnings before moving forward to place bets
        # TODO only collect winnings if it's not 7 days before end of month
        collect_winnings = driver.find_element_by_xpath(constants.collect_winnings_xpath)
        collect_winnings.click()
    print("Got winnings info.")
    # Print data to look at before new bet information is inserted
    fetch_data = cur.execute("SELECT * from food_club")
    data = fetch_data.fetchall()
    print(f"All data: {data}")
    con.close()


