import time
import pandas as pd
import matplotlib.pyplot as plt
import re
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.DataFrame()
all_urls = []
seasons = []
driver = webdriver.Chrome()
driver.get('https://playbill.com/vault')
year_dd = driver.find_element(By.TAG_NAME, 'select')
year_options = [year for year in year_dd.find_elements(By.TAG_NAME, 'option')]
view_button = driver.find_element(By.XPATH, '//*[@id="season-selector-form"]/button')
time.sleep(7)
year_options[0].click()
view_button.click()
time.sleep(2)



for i in range(1, 3):
    year_dd = driver.find_element(By.TAG_NAME, 'select')
    year_options = year_dd.find_elements(By.TAG_NAME, 'option')
    year_options[i].click()
    seasons.append(year_options[i].text)
    time.sleep(2)
    view_button = driver.find_element(By.CSS_SELECTOR,'body > div.bsp-site-wrapper > div.bsp-site.bsp-onDomInsert-inserted-60.pb-banner-item > div > div.pb-contrast-layout > div > div > div.bsp-column-main > div > div > form > div > div.bsp-column-fourth.results-select.week-count > div > div > input[type=submit]')
    view_button.click()
    time.sleep(5)
    show_links = driver.find_elements(By.XPATH,"//a[contains(@href, 'playbill.com/production')]")
    season_shows_urls = []
    for link in show_links:
        season_shows_urls.append(link.get_attribute("href"))
        time.sleep(2)
        season_shows_urls = list(set(season_shows_urls))
        # print(season_shows_urls)
    all_urls.append(season_shows_urls)
    print(all_urls)
    print(seasons)
        # the_soup = BeautifulSoup(driver.page_source,'html.parser')
        # print(the_soup)
        # driver.back()
    # show_titles_list = the_soup.find_all(attrs={'class':re.compile("col-1")})
    # # show_opening_dates_list = the_soup.find_all(attrs={'class':re.compile("col-2")})
    # for title in show_titles_list:
        # title = title.text.strip()
        # title = clean(title)
        # show_titles.append(title)
    # for date in show_opening_dates_list:
        # date = date.text.strip()
        # date = clean(date)
        # show_opening_dates.append(date)
    # driver.back()
    time.sleep(2)
driver.close()
urls = [url for url in all_urls]
df["Show Links"] = [url for url in urls]
df["Season"] = [season for season in seasons]
print(df)
# print(f'# of show titles: {len(show_titles)}')
# # print(f'# of opening dates: {len(show_opening_dates)}')
# # df['Title'] = [title for title in show_titles if title]
# # df['Opening Date'] = [date for date in show_opening_dates if date]
df = df.explode('Show Links')
print(df)
df.to_csv('Playbill.csv', index=False)
