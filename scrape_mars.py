from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

    url="https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup_weather = BeautifulSoup(response.text, 'html.parser')
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
    #results=soup_hemi.find_all('img',class_='thumb')
    results=soup_hemi.find_all('h3')
    base_url="https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/"
    images_url=[]
    titles=[]
    end="tif/full.jpg"
    for result in results:
        titles.append(result.text)
        #titles.append(result['alt'])
        #images_url.append( result['src']+end)
    count=0
    for thumb in titles:
        browser.find_by_css('img.thumb')[count].click()
        #images_url.append(browser.find_by_text('Sample')['href'])
        images_url.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count=count+1
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

#if __name__ == "__main__":
    #scrape()

