from yahoo_fin import stock_info
import csv
from numpy import int_
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime
from plyer import notification
from decimal import *
import requests

colrow = [[] for i in range(0, 9)]
visited = [[] for i in range(0, 9)]

with open('symbol.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        for i in range(0, 9):
            colrow[i].append(row[i])
            visited[i].append(0)

for i in range(0, 9):
    colrow[i] = colrow[i][1:]

names = ["SHARES", "SYMBOL", "LONG TERM STOPLOSS", "SHORT TERM STOPLOSS",
         "BUY SIGNAL", "SHORT TERM BREAKOUT", "BREAKOUT 1", "BREAKOUT 2", "TARGET"]

def telegram_messenger(ind, curPrice, title):
    message = f'  {colrow[0][ind]} \n Price :- {curPrice} \n Time:- {datetime.now().hour}:{datetime.now().minute} \n Date:- {datetime.now().day}/{datetime.now().month}/{datetime.now().year}'
    notification.notify(title=title, message=message,
                        app_icon=None, timeout=10, toast=False)
    mess_url = f'https://api.telegram.org/{token}/sendMessage?chat_id={chat_id}&text={title + message}'
    requests.get(mess_url)

def comp(x, y):
    x = Decimal(x)
    if(len(y)==0): y = Decimal(0)
    else:
        y = Decimal(y)
    return x.compare(y)

while True:
    ind = 0
    for symbol in colrow[1]:
        curPrice = stock_info.get_live_price(symbol)
        if len(colrow[2][ind])!=0 and visited[2][ind] == 0 and comp(curPrice, colrow[2][ind]) <= 0:
            title = f"{names[2]} IS HIT\n"
            telegram_messenger(ind, curPrice, title)
            visited[2][ind] = 1
        elif len(colrow[2][ind])!=0 and len(colrow[3][ind])!=0 and visited[3][ind] == 0 and comp(curPrice, colrow[2][ind]) > 0 and comp(curPrice, colrow[3][ind]) <= 0:
            title = f"{names[3]} IS HIT\n"
            telegram_messenger(ind, curPrice, title)
            visited[3][ind] = 1
        elif len(colrow[3][ind])!=0 and len(colrow[4][ind])!=0 and visited[4][ind] == 0 and comp(curPrice, colrow[3][ind]) > 0 and comp(curPrice, colrow[4][ind]) <= 0:
            title = f"{names[4]} IS HIT\n"
            telegram_messenger(ind, curPrice, title)
            visited[4][ind] = 1
        elif len(colrow[4][ind])!=0 and len(colrow[5][ind])!=0 and visited[5][ind] == 0 and comp(curPrice, colrow[5][ind]) >= 0 and comp(curPrice, colrow[6][ind]) < 0:
            title = f"{names[5]} IS HIT\n"
            telegram_messenger(ind, curPrice, title)
            visited[5][ind] = 1
        elif len(colrow[6][ind])!=0 and len(colrow[7][ind])!=0 and visited[6][ind] == 0 and comp(curPrice, colrow[6][ind]) >= 0 and comp(curPrice, colrow[7][ind]) < 0:
            title = f"{names[6]} IS HIT\n"
            telegram_messenger(ind, curPrice, title)
            visited[6][ind] = 1
        elif len(colrow[7][ind])!=0 and len(colrow[8][ind])!=0 and visited[7][ind] == 0 and comp(curPrice, colrow[7][ind]) >= 0 and comp(curPrice, colrow[8][ind]) < 0:
            title = f"{names[7]} IS HIT\n"
            telegram_messenger(ind, curPrice, title)
            visited[7][ind] = 1
        elif len(colrow[8][ind])!=0 and visited[8][ind] == 0 and comp(curPrice, colrow[8][ind]) >= 0 :
            title = f"{names[8]} IS HIT\n"
            telegram_messenger(ind, curPrice, title)
            visited[8][ind] = 1
        ind += 1

