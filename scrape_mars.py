import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import tweepy
from config import (consumer_key, 
                    consumer_secret, 
                    access_token, 
                    access_token_secret)

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
def scrape():
    browser = init_browser()
    # mars news
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup = bs(html,"lxml")
    news_title = soup.find("div",class_="bottom_gradient").h3.text
    news_p = soup.find('div', class_="rollover_description_inner").text.strip()
    # JPL images
    url = "https://www.jpl.nasa.gov/spaceimages"
    browser.visit(url)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(2)
    browser.click_link_by_partial_text("more info")
    time.sleep(1)
    html = browser.html 
    image_soup = bs(html,"lxml")
    original_url = "https://www.jpl.nasa.gov"
    image_url = image_soup.find("figure",class_="lede").a.img["src"]
    featured_image_url = original_url+image_url
    # mars weather
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    public_tweet = api.user_timeline("@MarsWxReport")
    mars_weather=public_tweet[0]["text"]
    # mars facts
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Description","Value"]
    df = df.set_index("Description")
    html_table = df.to_html()
    html_table.replace("\n","")
    df.to_html("table.html")
    # mars hemisprees
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html 
    mars_soup = bs(html,"lxml")
    results = mars_soup.find_all("div",class_="description")
    base_url = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = []
    for result in results:
        try:
            img_dict = {}
            img_dict["title"]=result.a.h3.text
            href = result.find("a",class_="itemLink product-item")
            link = base_url+href["href"]
            browser.visit(link)
            time.sleep(2)
            mars_html = browser.html
            img_soup = bs(mars_html,"lxml")
            img = img_soup.find('div', class_='downloads').find('li').a['href']
            img_dict["img_url"]=img
            hemisphere_image_urls.append(img_dict)
        except:
            continue
        browser.click_link_by_partial_href(result.a["href"])
    mars_dict = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "mars_table":html_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    return mars_dict