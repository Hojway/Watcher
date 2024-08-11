import sqlite3
from datetime import date, datetime
from random import randint
from bs4 import BeautifulSoup
import requests
import re
import os

# This script automaticly works everyday by using crontab
# 0 0 * * * ~/Applications/anaconda3/bin/python3 ~/Desktop/CS50/final_project/update_tracking.py

# The function may not work with some devices, because the web site can detect a bot and redirect to the checking for robot page
def current_price(link):
    url = f"{link}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    price = doc.find(class_="price-current").strong.string
    return price


# Get the absolute path of the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the SQLite database file
db_path = os.path.join(current_dir, 'database.db')

# Connect to the SQLite database
con = sqlite3.connect(db_path)

db = con.cursor()

today = date.today()

# Makeing a list of ids from adtabase
ids = []
all_ids = db.execute('SELECT DISTINCT product_id FROM track').fetchall()
for id in all_ids:
    ids.append(id[0])

for item_id in ids:
    items = db.execute('SELECT * FROM track WHERE product_id = ? ORDER BY date', (item_id,)).fetchall()

    # Check for number of each item
    if len(items) > 6:
        old_date = items[0][1]
        old_link = db.execute('SELECT link FROM product WHERE id = ?', (item_id,)).fetchall()[0][0]

        # Extracting new price by scraping item's web-site
        new_price = current_price(old_link)

        # Updateing date and price
        db.execute('UPDATE track SET date = ?, price = ? WHERE product_id = ? AND date = ?', (today, new_price, item_id, old_date))
    else:
        db.execute('INSERT INTO track (product_id, date, price) VALUES (?, ?, ?)', (item_id, today, new_price))

con.commit()
con.close()
