#################################################################################
##################            DESCRIPTION                    ####################
#################################################################################

# FETCHES SAMPLE OF 12K FOLLOWERS FOR LIST OF COMPETITORS
# CREATES CSV FILE FOR EACH COMPETITOR WITH ALL THE FOLLOWERS USERNAMES

#################################################################################
##################            REQUIREMENTS                   ####################
#################################################################################

# DOWNLOAD DRIVER EXECUTABLE FOR YOUR BROWSER - SPECIFY PATH TO EXEC
# INSERT INSTAGRAM CREDENTIALS
# DEFINE COMPETITORS (IG USERNAMES)

#################################################################################

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random

#Define Competitors
path_to_exec = 'path/to/exec'
competitors = []
ig_usr = ''
ig_pwd = ''

#Login into Instagram
def login(driver):
    usr = ig_usr
    pwd = ig_pwd
    #Access random page to prompt logic
    driver.get('https://www.instagram.com/blueapron/followers')
    time.sleep(2)
    driver.find_element_by_name("username").send_keys(usr)
    driver.find_element_by_name("password").send_keys(pwd)
    time.sleep(1)
    driver.find_elements(By.XPATH, '//button')[0].click()
    time.sleep(2)

#Extract followers info once they have loaded
def extract_foll_info(driver, account, var):
    css_sel = "body > div:nth-child(13)"
    foll_box = driver.find_element_by_css_selector(css_sel)
    xpath = '/html/body/div[4]/div/div[2]/div/div[2]/ul/div'
    links = foll_box.find_element_by_xpath(xpath).text
    links_final = [link.split('\n')[0] for link in links.split('\nFollow\n')]
    if var == True:
        df_followers = pd.DataFrame({'followers': links_final})
        csv_name = './followees/followers_' + str(account) + '.csv'
        df_followers.to_csv(csv_name, sep='\t')
        print('Fetched all info and created csv file')
    elif var == False:
        return links_final
        print('Fetced all info for ' + str(account))

#Loads 15k followers for an account
def fetch_followers(driver, account):
    global foll_list
    driver.get('https://www.instagram.com/' + str(account))
    time.sleep(2)
    driver.find_element_by_partial_link_text('followers').click()
    time.sleep(2)
    followers = int((driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title')).replace(",",""))
    driver.execute_script("followersbox = document.getElementsByClassName('_gs38e')[0];")
    count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))
    i = 1
    while count < 12000:
        driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")
        count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))
        time.sleep(2.5)
        if random.randint(1,20) == 5:
            time.sleep(random.randint(4,8))
            print('Random pause: ' + str(i) + '. Followers to go: ' + str((12000 - count)))
            i += 1
    extract_foll_info(driver, account, True)
    print('Process Complete for ' + str(account))


#Starting Chrome Browser
driver = webdriver.Chrome(path_to_exec) #'/Users/alessandro.vitelli/Downloads/chromedriver')
login(driver)

#Looping through competitors accounts and extracting followers (15k sample)
global_following = []
for competitor in competitors:
    followers = fetch_followers(driver, competitor)
    print('Fetched followers for ' + str(competitor)
