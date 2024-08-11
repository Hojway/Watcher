from flask import Flask, flash, redirect, render_template, request
from flask_session import Session
from helpers import newegg, apology
from cs50 import SQL
from statistics import mode, mean
from datetime import date


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL('sqlite:///database.db')


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # Check for valid web-site
        web_site = request.form.get("web-site")
        if not web_site:
            return apology("Invalid input, please choose web-site")

        # check for valid input search
        search_item = str(request.form.get("search_item"))

        if not search_item:
            return apology("Please enter the name of searching product")

        # Chech for valid result of search
        results = newegg(search_item)
        if not results:
            return apology(f"There no such product in {web_site}")

        #Creating list to extract all prices from  search result
        prices = []

        try:
            for price in results:
                prices.append(price["price"])
        except:
            return apology("  THE WEB-SITE THINGS THAT YOU ARE A ROBOT, 302")

        # Find Min
        Min = min(prices)
        # Find Max
        Max = max(prices)
        # Find Quantity
        length = len(prices)
        # Find Averaging
        average = round(mean(prices))
        # Find Mode
        Mode = mode(prices)

        return render_template("results.html", results=results[:100], min=Min, max=Max, length=length, average=average, mode=Mode, search_item=search_item)
    else:
        return render_template("index.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        current_date = date.today()

        # Check for valid track chechbox
        tracks = request.form.getlist("track")

        if not tracks:
            return apology("For adding items to track please choose item")

        if len(tracks) > 5:
            return apology("Too many items to track")

        # Extracting link, name and price from the chexkbox
        new_links =[]
        d = {}
        for track in tracks:
            d["link"] = str(track).split("&&")[0]
            d["name"] = str(track).split("&&")[1]
            d["price"] = str(track).split("&&")[2]
            new_links.append(d.copy())

        # Checking new items to the items from database
        old_links = db.execute("SELECT link, name FROM product")

        if not old_links:
            for i in new_links:
                db.execute("INSERT INTO product (link, name) VALUES (?, ?)", i["link"], i["name"])
                product_id = db.execute("SELECT id FROM product WHERE link = ?",  i["link"])[0]["id"]
                db.execute("INSERT INTO track (product_id, date, price) VALUES (?, ?, ?)", product_id, current_date, i["price"])

        else:
            for n in new_links:
                if len(old_links) < 5:
                    c = 0
                    for o in old_links:
                        if n["link"] == o["link"]:
                            c += 1

                    if c == 0:
                        db.execute("INSERT INTO product (link, name) VALUES (?, ?)", n["link"], n["name"])
                        product_id = db.execute("SELECT id FROM product WHERE link = ?",  n["link"])[0]["id"]
                        db.execute("INSERT INTO track (product_id, date, price) VALUES (?, ?, ?)", product_id, current_date, n["price"])
                else:
                    skipped = n["name"]
                    return apology(f"The item: {skipped} was not added, there are already 5 items are trscking")

        return redirect("/tracking")
    return render_template("results.html")

@app.route("/tracking", methods=["GET", "POST"])
def tracking():
    if request.method == "POST":

        # Check link for valid
        links = request.form.getlist("link")
        if not links:
            return apology("To delete tracking item please choose them")

        # Idenify every id from checkbox links and delete one by one from database
        for link in links:
            id = db.execute("SELECT id FROM product WHERE link = ?", link)[0]["id"]
            db.execute("DELETE FROM track WHERE product_id = ?", id)
            db.execute("DELETE FROM product WHERE id = ?", id)
        return redirect("/tracking")
    else:
        # Display tracking items from database
        products = db.execute("SELECT * FROM product")

        # Creating a list of lists with the number of items
        prod_list = [[] for _ in range(len(products))]

        # Looping through every item and adding name, link, date and price
        for i, product in enumerate(products):
            prod_list[i].append(product["link"])
            prod_list[i].append(product["name"])
            tracks = db.execute("SELECT date, price FROM track WHERE product_id = ? ORDER BY date", product["id"])
            d_l = []
            for track in tracks:
                d_l.append(track["date"])
            prod_list[i].append(d_l)
            p_l = []
            for track in tracks:
                p_l.append(track["price"])
            prod_list[i].append(p_l)


        return render_template("tracking.html", prod_list=prod_list)

if __name__ == '__main__':
    app.run(debug=True)

