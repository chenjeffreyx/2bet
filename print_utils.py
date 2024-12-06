import json

from datetime import datetime

def print_rows(rows):
    for row in rows:
        print(row)

def print_bet_dict(dict):
    print(json.dumps(dict, indent=4))

def print_new_bet(data):
    print('=========================== [2BET] NEW BET ===========================')
    print_curr_time()
    print_bet_dict(data)
    print('======================================================================')

def print_tracked_bets(data):
    print('========================= [2BET] TRACKED BETS ========================')
    print_curr_time()
    print_bet_dict(data)
    print('======================================================================')

def print_curr_time():
    from datetime import datetime
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
