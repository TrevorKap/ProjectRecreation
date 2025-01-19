import pandas as pd
import geopandas as gpd
import numpy as np
import hvplot.pandas 
import altair as alt
import matplotlib.pyplot as plt
import rasterio as rio
import osmnx as ox
pd.options.display.max_columns = 999

# Hide warnings due to issue in shapely package 
# See: https://github.com/shapely/shapely/issues/1345
np.seterr(invalid="ignore");

import requests
import time
from bs4 import BeautifulSoup
from random import sample 
import pandas as pd 
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import glob as gb 
from selenium_stealth import stealth

path = r"C:\Users\Owner\Python,Remote,Cloud\Pinnacore"
os.chdir(path)

finalfile = "RobloxSelenium" + "_" + "{:%Y_%h_%d_%H-%M-%S}".format(datetime.now()) +".csv"
finalfile



page_count=10
results = []

roblox_placeholders = ["This item found on Roblox marketplace","Last check:"]

# selectors
titleSelector = "div.item-card-name"
descSelector = "div.building-description"
linkSelector = "div.item-card-name"
saleSelector = "div.Text-c11n-8-84-3__sc-aiai24-0"
sale2Selector = "p.Text-c11n-8-84-3__sc-aiai24-0"
nhoodSelector = "h4.Text-c11n-8-84-3__sc-aiai24-0"
nhood2Selector = "h2.styledComponents__BuildingCardTitle-sc-1bj2ydz-8"

driver = webdriver.Chrome()
textDriver = webdriver.Chrome()

stealth(driver,
       languages=["en-US", "en"],
       vendor="Google Inc.",
       platform="Win32",
       webgl_vendor="Intel Inc.",
       renderer="Intel Iris OpenGL Engine",
       fix_hairline=True,
       )

stealth(textDriver,
       languages=["en-US", "en"],
       vendor="Google Inc.",
       platform="Win32",
       webgl_vendor="Intel Inc.",
       renderer="Intel Iris OpenGL Engine",
       fix_hairline=True,
       )

url ="https://www.roblox.com/catalog?Category=1&CurrencyType=3&pxMin=1&salesTypeFilter=1&SortType=2&SortAggregation=3"

url2 = "https://www.roblox.com/catalog?Category=1&salesTypeFilter=1&SortType=1&SortAggregation=3"

# Inspect the Roblox website and figure out the number pages for rental ads use
# In the charlotte example, there are a total of 20 pages so I set the range at 21

for page in range(1,page_count+1,1):
    
    print("This is page: " + str(page))

    page = str(page) + '_p/'
    

    print(f"Urls:\n")
    page_links = []
    for url in [url,url2]: # getListingType():
        print(f"\t\t{url+page}\n")
        browser = driver.get(url+page)
        html = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, 'html.parser')

        for item in soup.select(linkSelector):
            l = item.select("a")[0].attrs["href"]
            if not(l.startswith("https://")):
                l = "https://www.roblox.com"+l
            page_links.append(l)

    for link in page_links:
        ovPage = textDriver.get(link)
        textSoup = BeautifulSoup(textDriver.page_source,"html.parser")

        if len(textSoup.select("div.px-captcha-container")) > 0:
            time.sleep(0.3)
            continue
        else:
        
            title = textSoup.select(titleSelector)[0].text
            nh1 = textSoup.select(nhoodSelector)
            nh2 = textSoup.select(nhood2Selector)
            nhood = None

            # get neighborhood from among header tags
            if len(nh1) > 0:
                for blurb in nh1:
                    if "neighborhood:" in blurb.text.lower():
                        nhood = blurb.text.split(":")[1][1:]
                        # print(blurb.text.split(":")[1][1:])
                        break
            elif (len(nh2) > 0 and type(nhood) == type(None)):
                for blurb in nh2:
                    if "neighborhood:" in blurb.text.lower():
                        nhood = blurb.text.split(":")[1][1:]
                        # print(blurb.text.split(":")[1][1:])
                        break

            # getting address from title
            address = None
            for w in range(len(title)):
                if title[w].isnumeric():
                    address = title[w:]
                    break

            if len(textSoup.select(descSelector))>0 and len(textSoup.select(descSelector)[0].text)>70 and (not(any(holder in textSoup.select(descSelector)[0].text for holder in Roblox_placeholders))):
                text = textSoup.select(descSelector)[0].text
            elif len(textSoup.select(sale2Selector)[0]) and len(textSoup.select(sale2Selector)[0].text)>70 and (not(any(holder in textSoup.select(sale2Selector)[0].text for holder in Roblox_placeholders))):
                text= textSoup.select(sale2Selector)[0].text
            elif len(textSoup.select(saleSelector)[0])>0 and len(textSoup.select(saleSelector)[0].text)>70 and (not(any(holder in textSoup.select(saleSelector)[0].text for holder in Roblox_placeholders))):
                text= textSoup.select(saleSelector)[0].text
            else:
                text=""

            results.append({
            "title": title,
            "address": address,
            "neighborhood": nhood,
            "description": text,
            "url": link
            })
            print(f"title: {title}\t\taddress: {address}\t\tneighborhood: {nhood}\nlink: {link}\n\tdescription: {text}")

            time.sleep(0.3)
           


    time.sleep(0.5)
# I am going to kill myself
Robloxdata =  pd.DataFrame(results)
Roblox_csv(finalfile, index = False)

All = gb.glob(path + "/*.csv")
All


if len(All)>0:
    Roblox = (pd.read_csv(file) for file in All)  
    FinalRoblox  = pd.concat(Roblox, ignore_index=True)
else:
    import warnings
    warnings.warn(f"There are no data in {path}, try using 'Webscraping Roblox Data.ipynb'.",UserWarning,stacklevel=2)

FinalUnique = FinalRoblox.drop_duplicates()

outPath = path+"/clean"
os.chdir(outPath)
# if os.path.exists("ZillowUnique.csv"):
#     os.remove(("ZillowUnique.csv"))
FinalUnique.to_csv("RobloxUnique.csv", index=False,)
(print("compilation complete"))
os.chdir("../"+path)

url = "https://www.roblox.com/catalog?Category=1&CurrencyType=3&pxMin=1&salesTypeFilter=1&SortType=2&SortAggregation=3"
response = requests.get(url)

# Parse HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements with class 'item-card-name'
items = soup.find_all(class_='item-card-link')

# Extract and print titles
with open('roblox_items.txt', 'w', encoding='utf-8') as file:
    # Find and write each item name to the file
    items = soup.find_all(class_='item-card-name')
    for item in items:
        file.write(item.text + '\n')