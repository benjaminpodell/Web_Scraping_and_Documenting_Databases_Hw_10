# All code very similar to what I have in Jupyter notebook with a few changes to render for visual studio. (Not Fully working)

from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as stir_the_soup
import pandas as pd 
import requests
import shutil
import time

##########################################################################################################
def init_browser():
    executable_path = {"executable_path": "/Users/btech/chromedriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_information = {}

##########################################################################################################
    url_1 = "https://mars.nasa.gov/news/"
    browser.visit(url_1)
    html = browser.html
    soup = stir_the_soup(html, 'html.parser')

    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
  
    mars_information["news_date"] = news_date
    mars_information["news_title"] = news_title
    mars_information["summary"] = news_p

##########################################################################################################
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)
    html = browser.html
    soup = stir_the_soup(html, 'html.parser')
    image = soup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov" + image

########################################################################################################## 
    url_3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_3)

    html = browser.html
    soup = stir_the_soup(html, 'html.parser')
    article = soup.find("div", class_="js-tweet-text-container")
    mars_weather = article.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)

##########################################################################################################
    url_4 = "https://space-facts.com/mars/"
    browser.visit(url_4)

    grab=pd.read_html(url_4)
    mars_info=pd.DataFrame(grab[0])
    mars_info.columns=['Mars','Data']
    mars_table=mars_info.set_index("Mars")
    mars_data = mars_table.to_html(classes='mars_data')
    mars_data = mars_data.replace('\n', ' ')

    mars_information["mars_table"] = mars_data

##########################################################################################################
    url_5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_5)
    html = browser.html
    soup = stir_the_soup(html, 'html.parser')
    mars_hemisphere=[]

    for x in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[x].click()
        html = browser.html
        soup = stir_the_soup(html, 'html.parser')
        
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary = {"title":img_title,"img_url":img_url}
        mars_hemisphere.append(dictionary)

    mars_information['mars_hemisphere'] = mars_hemisphere

##########################################################################################################      
    return mars_information