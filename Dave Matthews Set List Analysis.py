import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re 
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dataFrame = pd.DataFrame()

def get_links():
    link_driver = webdriver.Chrome()
    link_driver.get('https://dmbalmanac.com/TourShow.aspx')
    table = link_driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table')
    # print(table.text)
    tours = table.find_elements(By.TAG_NAME,'a')
    links = []
    for tour in tours:
        link = tour.get_attribute("href")
        if re.match(r".*TourShowInfo.*", link):
            links.append(link)        
    return(links)

def get_shows(links):
    show_driver = webdriver.Chrome()
    show_links = []
    for link in links:
        show_driver.get(link)
        show_list = show_driver.find_elements(By.TAG_NAME, 'a')
        for show in show_list:
            show_url = show.get_attribute("href")
            if re.match(r".*TourShowSet.*", show_url):
                show_links.append(show_url)
    return(show_links)

def get_venues_dates(links):
    show_driver = webdriver.Chrome()
    show_venues = []
    show_dates = []
    for link in links:
        show_driver.get(link)
        show_list = show_driver.find_elements(By.TAG_NAME, 'a')
        for show in show_list:
            url = show.get_attribute("href")
            # print(venue_url)
            if re.match(r".*venuestats.*",url):
                venue = show.text
                show_venues.append(venue)
            elif re.match(r".*TourShowSet.*",url):
                date = show.text
                show_dates.append(date)            
    return(show_venues, show_dates)

# def get_dates(links):
    # show_driver = webdriver.Chrome()
    # show_dates = []
    # for link in links:
        # show_driver.get(link)
        # show_list = show_driver.find_elements(By.TAG_NAME, 'a')
        # for show in show_list:
            # date_url = show.get_attribute("href")
            # print(date_url)
            # if re.match(r".*TourShowSet.*",date_url):
                # date = show.text
                # show_dates.append(date)
    # print(show_dates)            
    # return(show_dates)

def get_songs(show_links):
    song_driver = webdriver.Chrome()
    for show_link in show_links:
        songs = []
        song_driver.get(show_link)
        setlist = song_driver.find_elements(By.TAG_NAME,'a')
        for song in setlist:
            song_name = song.get_attribute("class")
            if re.match(r"lightorange", song_name):
                song_title = song.text
                songs.append(song_title)
        print(songs)
    return(songs)
links = ['https://dmbalmanac.com/TourShowInfo.aspx?tid=8181&where=2024']
venues, dates = get_venues_dates(links)
while ("" in dates):
    dates.remove("")
# print(f"Dates: {len(dates)}")
shows = get_shows(links)
print(f"Shows: {len(shows)}")
# venues = get_venues(links)
# print(f"Venues: {len(venues)}")
print(venues)
songs = get_songs(shows)
print(songs)
dataFrame["Dates"] = dates
dataFrame.Dates.replace("",np.nan, inplace=True)
dataFrame.Dates.dropna()
dataFrame["Venues"] = venues
dataFrame.to_csv('DMB.csv', index=False)