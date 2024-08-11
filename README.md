# WATCHER

## CS50
>This was my final project for conclude the CS50 Introduction to Computer Sciense course.

>CS50, python, flask web framework, web development, HTML, CSS, JavaScript, sqlite3

## Features
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)

I've used Flask web framework based in Python and sqlite3 for storing data

## Explaning the project
My final project is a web-scraping website, which scrapes date from [NewEgg](https://www.newegg.com/).

### How it works
When the user searches for certain product, as a result website displays names, links and prices of all product that matches with searching request. Than he can add or remove some items to the "tracker", which tracks prices dynamic of 7 day and updates everyday automatically.

## Storing track

I use two table in in the file database.db

First table "product", which has id, link and name colunms for storing information of products

Senconf table "track", which has product_id, date and price columns and FOREIGN KEY(product_id) REFERENCES product(id), this stores prices.

## What does each files do

### helpers.py
In this file thare are two functions "newegg" and "apology"

- newegg function is an actual [NewEgg](https://www.newegg.com/) a web scraper. The function take input, which is searching item name, gets the text by using "request" and parsers thuoth "BeautifulSoup", determines the number of pages, parsers again though every page and finds item's name, link and price based on their "CSS class". The output is going to be a list of dictionaries.

- apology function takes the input as text and renders it to the apology.html paga.

### layout.html
I am using An HTML layout as a blueprint to arrange web pages.
Because I am using Flask all the logic part is an file app.py that works together with all html files.

### index.html
File index.html is main page for entering search and also has link for tracking page, when you hit the button search the request send input to app.py and checks for valid input, then generates output from newegg function (the function scrapes up to 5 page for decreasing loading time) from helpers.py, calculates statistics values as quentaty, avarage, maximum, minimum and most common price, after that it renders a results.html

### results.html
The results.html displays a table, which has names with link and price, also has statistics respectfully.
Every of row in a table is being formed by "jinja2" for loop and it can display up to 100 rows for convenience, by choosing any item clicking it's checkbox you can then press the "Add for tracking" which will add current items to the product and tracking tables. Before adding the "route(/results)" is going to check number of items, up to 5 items are valid, every item will be checked with items in the product table, if a certain items are already in the table then they will be skipped but no matched items will be added to the table and apology page is going to be rendered (also in a helpers.py), if every thing is going well, it will be redirected to tracking.html.

### tracking.html
In the tracking.html there is a table of item's name and price, which are represented with a line chart, I am using JavaScript chart library for this. Every item in the table and like results page uses "jinja2" for loop. In order to display correct data, when the "GET" request is made "route(/tracking)" gets ids from table product, then for every id it adds name, link, date and price forming a list of dictionary, eventually tracking.html will be rendered. You can delete any item from this table by clicking the checkbox and pressing "Delete", this will send the link of item and delete from database based on the link.

### update_tracking.html
This file is an actual daily data updating. When the file runs, it checks every item in the database for outdate, based on the number of every item it inserts or update date and price for them. There is a function "current price", which take a link as an input and gives current price as an output.
This file runs on my mac every day automatically by using "cron-job", for that I am using crontab like this:

| Crontab |
| :---: |
| <img src="screenshots/img1.png" width="400">  |


## Demonstration on Youtube

[My Final Project](https://youtu.be/WSUAHkeF5ew)

## About CS50

I am profoundly grateful for the Harvard CS50 course, an online learning experience that stands out as the best I have ever undertaken. Tough problem sets initially seemed hard, but they boosted my understanding of computer science. Clear explanations by instructors helped demystify complex topics

Thank you for all CS50.
