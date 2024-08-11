from bs4 import BeautifulSoup
import requests
import re

from flask import render_template


def apology(message):

    return render_template("apology.html", message=message)

# The function may not work with some devices, because the web site can detect a bot and redirect to the checking for robot page
def newegg(product):

    url_product = product.replace(' ', '+')

    url = f"https://www.newegg.ca/p/pl?d={url_product}"

    try:
        page = requests.get(url).text

        doc = BeautifulSoup(page, "html.parser")

        page_text = doc.find(class_="list-tool-pagination-text").strong
    except:
        return apology("302, THE WEB-SITE THINGS THAT YOU ARE A BOT")

    pages = int((str(page_text).split("/")[-2]).split(">")[-1][:-1])

    result = []
    limit = 0
    for page in range(1, pages + 1):
        url = f"https://www.newegg.ca/p/pl?d={url_product}&page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        div = doc.find(class_="item-cells-wrap border-cells short-video-box items-grid-view four-cells expulsion-one-cell")
        items = div.find_all(text=re.compile(product))


        for item in items:
            parent = item.parent

            if parent.name != "a":
                continue

            link = parent['href']
            next_parent = item.find_parent(class_="item-container")
            price = next_parent.find(class_="price-current").strong

            if price != None:
                price = price.string

                result.append({"link" : link, "name" : item, "price" : int(price.replace(",", ""))})

        # Checking to limit of the page scrolling
        limit += 1
        if limit == 5:
            return result

    return result


