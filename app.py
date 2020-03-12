from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    print(mars)
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    print(mars_data)
    mongo.db.mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)
    

if __name__ == "__main__":
    app.run(debug=True)


