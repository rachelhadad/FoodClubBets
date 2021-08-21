import os
import datetime

chrome_driver_path = os.environ.get("chrome_driver_path")
SHIPWRECK_CHECKBOX_XPATH = \
    "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[3]/td[1]/input"
LAGOON_CHECKBOX_XPATH = \
    "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[4]/td[1]/input"
TI_CHECKBOX_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[5]/td[1]/input"
HIDDEN_COVE_CHECKBOX_XPATH = \
    "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[6]/td[1]/input"
HARPOON_CHECKBOX_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[7]/td[1]/input"
SHIPWRECK_DROPBOX_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[3]/td[" \
                          "2]/select"
LAGOON_DROPBOX_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[4]/td[2]/select"
TI_DROPBOX_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[5]/td[2]/select"
HIDDEN_COVE_DROPBOX_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[6]/td[" \
                            "2]/select"
HARPOOON_DROPBOX_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[1]/tbody/tr[7]/td[" \
                         "2]/select"
arena_xpath_dict = {"Shipwreck": SHIPWRECK_CHECKBOX_XPATH}
GET_BET_AMOUNT_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/p[4]/b"
PLACE_BET_AMOUNT_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/table[2]/tbody/tr[3]/td[1]/input"
PLACE_BET_BUTTON_XPATH = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[4]/form/p[3]/input[2]"
arena_xpath_dictionary = {"Shipwreck": {"checkbox": SHIPWRECK_CHECKBOX_XPATH, "dropbox": SHIPWRECK_DROPBOX_XPATH},
                          "Lagoon": {"checkbox": LAGOON_CHECKBOX_XPATH, "dropbox": LAGOON_DROPBOX_XPATH},
                          "Treasure Island": {"checkbox": TI_CHECKBOX_XPATH, "dropbox": TI_DROPBOX_XPATH},
                          "Hidden Cove": {"checkbox": HIDDEN_COVE_CHECKBOX_XPATH,
                                          "dropbox": HIDDEN_COVE_DROPBOX_XPATH},
                          "Harpoon Harry's": {"checkbox": HARPOON_CHECKBOX_XPATH,
                                              "dropbox": HARPOOON_DROPBOX_XPATH}
                          }

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
yesterday = today - datetime.timedelta(days=1)
CONTENDER_VALUES = {
    "Scurvy Dan the Blade": "1",
    "Stuff-A-Roo": "9",
    "Gooblah the Grarrl": "15",
    "Puffo the Waister": "8",
    "Federismo Corvallio": "17",
    "Ned the Skipper": "13",
    "Captain Crossblades": "11",
    "Ol' Stripey": "12",
    "Fairfax the Deckhand": "14",
    "Orvinn the First Mate": "3",
    "Peg Leg Percival": "6",
    "Squire Venable": "10",
    "Franchisco Corvallio": "16",
    "Bonnie Pip Culliford": "7",
    "Buck Cutlass": "19",
    "Admiral Blackbeard": "18",
    "Sir Edmund Ogletree": "5",
    "Young Sproggie": "2",
    "Lucky McKyriggan": "4",
    "The Tailhook Kid": "20"
}
np_on_hand_xpath = "/html/body/div[3]/div[2]/table/tbody/tr[1]/td[3]/a[2]"
place_bet_link_xpath = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[2]/a[3]"
round_number = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[3]/center[1]/table/tbody/tr[3]/td[1]/b"

# go_to_bank constants
collect_interest_xpath = "/html/body/div[12]/div[3]/div[2]/div[2]/div[2]/div/form/input[3]"
withdrawal_input_xpath = "/html/body/div[12]/div[3]/div[3]/div[2]/div[2]/form/div[1]/input[1]"
withdrawal_button_xpath = "/html/body/div[12]/div[3]/div[3]/div[2]/div[2]/form/div[1]/input[2]"
pin_input_xpath = "/html/body/div[12]/div[3]/div[3]/div[2]/div[2]/form/div[1]/input"

# get_winnings constants
no_winnings_xpath = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[3]/center[2]/form/table/tbody/tr[3]/td"
collect_winnings_xpath = "/html/body/div[3]/div[3]/table/tbody/tr/td[2]/center[3]/center[2]/form/p/input[2]"
