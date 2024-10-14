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

driver = webdriver.Chrome()
driver.get('https://playbill.com/vault')
year_dd = driver.find_element(By.TAG_NAME, 'select')
year_options = year_dd.find_elements(By.TAG_NAME, 'option')
view_button = driver.find_element(By.XPATH, '//*[@id="season-selector-form"]/button')
time.sleep(2)
year_options[0].click()
view_button.click()
time.sleep(2)
the_soup = BeautifulSoup(driver.page_source,'html.parser')
show_titles_list = the_soup.find_all(attrs={'class':re.compile("col-1")})
show_opening_dates_list = the_soup.find_all(attrs={'class':re.compile("col-2")})
show_titles = []
show_opening_dates = []
for title in show_titles_list:
    title = title.text.strip()
    show_titles.append(title)
for date in show_opening_dates_list:
    date = date.text.strip()
    show_opening_dates.append(date)
# driver.back()
# time.sleep(2)

for i in range(1, len(year_options)):
    year_dd = driver.find_element(By.TAG_NAME, 'select')
    year_options = year_dd.find_elements(By.TAG_NAME, 'option')
    year_options[i].click()
    time.sleep(2)
    view_button = driver.find_element(By.CSS_SELECTOR,'body > div.bsp-site-wrapper > div.bsp-site.bsp-onDomInsert-inserted-60.pb-banner-item > div > div.pb-contrast-layout > div > div > div.bsp-column-main > div > div > form > div > div.bsp-column-fourth.results-select.week-count > div > div > input[type=submit]')
    view_button.click()
    time.sleep(5)
    the_soup = BeautifulSoup(driver.page_source,'html.parser')
    show_titles_list = the_soup.find_all(attrs={'class':re.compile("col-1")})
    show_opening_dates_list = the_soup.find_all(attrs={'class':re.compile("col-2")})
    for title in show_titles_list:
        title = title.text.strip()
        # title = clean(title)
        show_titles.append(title)
    for date in show_opening_dates_list:
        date = date.text.strip()
        # date = clean(date)
        show_opening_dates.append(date)
    # driver.back()
    time.sleep(2)
driver.close()

print(f'# of show titles: {len(show_titles)}')
print(f'# of opening dates: {len(show_opening_dates)}')
df['Title'] = [title for title in show_titles if title]
df['Opening Date'] = [date for date in show_opening_dates if date]
print(df)

