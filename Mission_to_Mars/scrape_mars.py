#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from twitter_scraper import get_tweets
from html.parser import HTMLParser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from splinter import Browser
import requests
from PIL import Image
import cssutils
import twitter_scraper
import pandas as pd
import time


# In[ ]:


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


# In[8]:


def scrape():
    browser = init_browser()

    #NASA
    url = "https://mars.nasa.gov/news.html/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    news = soup.find("div", class_="list_text")
    news_title = soup.find("div", class_="content_title").text
    first_paragraph = news.find("div", class_="article_teaser_body").text
    
    #JPL
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_html = browser.html
    soup = bs(jpl_html, 'html.parser')
    img_tag = soup.find("div", class_="carousel_items")
    img_tag = img_tag.find("article")['style'].split("('", 1)[1].split("')")[0]
    img_url = 'https://www.jpl.nasa.gov' + str(img_tag)
    
    #Weather
    tweet_url = "https://twitter.com/marswxreport"
    browser.visit(tweet_url)
    tweet_html = browser.html
    soup = bs(tweet_html, 'html')
    tweets = []
    for tweet in get_tweets('@MarsWxReport', pages=1):
        tweeet = tweet['text']
        tweets.append(tweeet)
    
    #Facts
    mars_url = "https://space-facts.com/mars/"
    tables = pd.read_html(mars_url)
    tables = pd.DataFrame(tables[0])
    tables.columns = ["", "values"]
    tables = tables.to_html()   
    
    #Hemis
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemis_short_url = "https://astrogeology.usgs.gov/"
    browser.visit(hemis_url)
    hemis_html = browser.html
    soup = bs(hemis_html, 'html')
    hemisphere_imageurls = []
    for i in range(4):
        label = soup.find_all("img", class_="thumb")[i]["src"]
        title = soup.find_all("h3")[i].text
        pic_url = hemis_short_url + label
        hemis_pic = {"title": title, "img_url": pic_url}
        hemisphere_imageurls.append(hemis_pic)
    hemisphere_imageurls

    #Summary
    mars = {
        "title": news_title, 
        "content": first_paragraph,
        "jpl_pic": img_url,
        "tweet": tweets[0],
        "facts": tables,
        "hemispheres": hemisphere_imageurls
    }

    return mars