import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time, os, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

"""
Functions for web scraping with selenium
1. Google speaker
2. Google institute
3. Google institute on Google Map

"""

chromedriver = "D:\\chromedriver\\chromedriver.exe" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

# Open automated Chrome with fictionDB webpage
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.google.com")


def google_speaker(speaker):
    keyword = speaker
    speaker_dict={}
    headers = ["speaker","profession","birth","born"]

    # Selenium begins
    driver.get("https://www.google.com")
    search_bar = driver.find_element_by_xpath("//input[@name='q'][@type='text']")
    search_bar.clear()
    search_bar.send_keys(keyword)
    #     print(speaker)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(2)

    # Set default value of result
    profession, birth, born = np.nan, np.nan, np.nan

    # Find profession
    try:
        profession = driver.find_element_by_xpath("//div[@data-attrid='subtitle']").text
    except:
        pass

    if profession is np.nan:
        try:
            description = driver.find_element_by_xpath("//div[@data-attrid='description']").text
            profession = re.findall("(?<=was )(.*)(?= who)", description)[0]
        except:
            pass

    # Find birth info    
    try:
        birth = driver.find_element_by_xpath("//div[@class='rVusze']").text
    except:
        pass

    # Extract age and birth blace from birth info
#     # Age
#     try:
#         age = re.findall("age \d+", birth)[0].split(' ')[-1]
#     except:
#         pass

    # Year born
    try:
        born = re.findall("Born: .* \d+", birth)[0].split(', ')[-1]
    except:
        pass

#     # Birth place
#     try:
#         origin = " ".join(birth.split(', ')[-2:])
#     except:
#         pass

    speak_dict = dict(zip(headers,[speaker,profession,birth,born]))

    return speak_dict
