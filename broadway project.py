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

driver = webdriver.Chrome()
driver.get('https://playbill.com/vault')
year = driver.find_element(By.NAME, 'year')
print(year.text)

driver.close()