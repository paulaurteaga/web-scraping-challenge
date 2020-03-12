from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    # NASA Mars News
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    html_news = browser.html
    soup_news = BeautifulSoup(html_news, 'html.parser')
    description = (soup_news.find('div', class_="rollover_description_inner")).text
    title_string=soup_news.find('img',class_='img-lazy')['alt']

    # JPL Mars Space Images 
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    html_img = browser.html
    soup_img = BeautifulSoup(html_img, 'html.parser')
    image_url=soup_img.find('article', class_='carousel_item')['style']
    url_array=image_url.split("'")
    img_url=url_array[1]
    entire_url="https://www.jpl.nasa.gov" + img_url

    ## Mars Weather
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    time.sleep(4)
    html_weather = browser.html
    soup_weather = BeautifulSoup(html_weather, 'html.parser')
    print(soup_weather)
    post=soup_weather.find('div',class_="ProfileHeaderCard").p
    text=post.text

    # Mars Facts
    url_facts = "https://space-facts.com/mars/"
    tables = pd.read_html(url_facts)[0]
    table = tables.to_html()
    # Mars Hemisphers
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    html_hemi = browser.html
    soup_hemi = BeautifulSoup(html_hemi, 'html.parser')
    results=soup_hemi.find_all('div',class_='item')
    base_url="https://astrogeology.usgs.gov"
    images_url=[]
    titles=[]
    for result in results:
        titles.append(result.h3.text)
        images_url.append( base_url+result.a['href'])
    hemisphere_image_urls = []
    counter = 0
    for x in images_url:
        hemisphere_image_urls.append({"title":titles[counter],"img_url":images_url[counter]})
        counter = counter+1 

    dict = {"Header":title_string,
    "Description":description,
    "Image":entire_url,
    "Weather":text,
    "Facts":table,
    "Hemispheres":hemisphere_image_urls}

    return dict;

if __name__ == "__main__":
    scrape()

