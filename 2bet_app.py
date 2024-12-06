import requests
import time
from bs4 import BeautifulSoup
import asyncio
import os

from bot import send_bet_to_staging_area, send_bet_to_testing_area

from print_utils import print_tracked_bets, print_new_bet

from dotenv import load_dotenv
load_dotenv()

PAYLOAD_2BETAG_1 = {
    'username': os.getenv('USERNAME_2BETAG_1'),
    'password': os.getenv('PASSWORD_2BETAG_1'),
}
PAYLOAD_2BETAG_2 = {
    'username': os.getenv('USERNAME_2BETAG_2'),
    'password': os.getenv('PASSWORD_2BETAG_2'),
}

LOGINS = [PAYLOAD_2BETAG_1, PAYLOAD_2BETAG_2]
SLEEP = 2 * 60

def parse_bet_table_data(table):
    header = []
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th') if el.text.strip()]
        else:
            row = [el.text.strip() for el in row.find_all('td') if el.text.strip()]
            rows.append(row)

    data = {}
    for row in rows:
        bet = {}
        for index, item in enumerate(row):
            bet[header[index]] = item
        data[row[0]] = bet

    return data

def get_pending_bets(payload):
    try:
        with requests.Session() as s:
            login_url = 'https://engine.2bet.ag/login-submit'
            pending_bets_url = 'https://engine.2bet.ag/player/open-bets'

            s.post(login_url, data=payload)
            r = s.get(pending_bets_url, timeout=100)
            soup = BeautifulSoup(r.text, 'lxml')
            table = soup.find('table', attrs={'class':'table table-bordered'})
            return parse_bet_table_data(table)
    except Exception as e:
        print(e)

def get_existing_bets():
    curr_bets = {}

    for login in LOGINS:
        pending_bets = get_pending_bets(login)
        curr_bets.update(pending_bets)

    return curr_bets

def main():
    curr_bets = get_existing_bets()

    while True:
        for login in LOGINS:
            pending_bets = get_pending_bets(login)

            if pending_bets is None:
                print('Maybe error: No pending bets')
                continue

            for key, item in pending_bets.items():
                if key not in curr_bets:
                    # Add owner key to avoid confusion
                    formatted_item = {}
                    if (login['username'] == os.getenv('USERNAME_2BETAG_1')):
                        formatted_item['Owner'] = 'Local Leaks'
                    elif (login['username'] == os.getenv('USERNAME_2BETAG_2')):
                        formatted_item['Owner'] = 'Varun'
                    formatted_item.update(item)

                    try:
                        # Group
                        asyncio.run(send_bet_to_testing_area(formatted_item))
                        # Personal
                        asyncio.run(send_bet_to_staging_area(formatted_item))

                        print_new_bet(formatted_item)
                    except Exception as e:
                        print(e)

            curr_bets.update(pending_bets)

        print_tracked_bets(curr_bets)

        time.sleep(SLEEP)

if __name__ == "__main__":
    main()
