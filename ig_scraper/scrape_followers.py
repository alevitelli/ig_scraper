#################################################################################
##################            DESCRIPTION                    ####################
#################################################################################

# FETCHES MAX 1.5K FOLLOWINGS FOR EACH FOLLOWER IN THE COMPETITOR'S CSV
# AGGREGATES ALL FOLLOWINGS AND CREATES CSV WITH FREQUENCIES

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
import atexit
from collections import Counter
import params as params
from utils import login, return_foll_info

is_blocked = False

#Extract followers info once they have loaded

#Loads following for an account
def fetch_following(driver, account):
    global is_blocked
    driver.get('https://www.instagram.com/' + str(account))
    time.sleep(2.5)
    driver.find_element_by_partial_link_text('following').click()
    time.sleep(2.5)
    try:
        following = int((driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text).replace(",",""))
    except:
        following = int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text)
    driver.execute_script("followersbox = document.getElementsByClassName('j6cq2')[0];") #PdwC2 HYpXt
    count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))
    i = 1
    count_2 = 0
    while count < following-10:
        driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")
        count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))
        if count > 1500 or count == count_2:
            is_blocked == True
            break
        time.sleep(3)
        if random.randint(1,20) == 5:
            time.sleep(random.randint(4,8))
            print('Random pause: ' + str(i) + '. Followers to go: ' + str((following - count)))
            count_2 = count
            i += 1
    time.sleep(3)
    return return_foll_info(driver)

def exit_handler():
    global global_following
    flat_glob_foll = [item for sublist in global_following for item in sublist]
    count_glob_foll = Counter()
    for follow in flat_glob_foll:
        count_glob_foll[follow] += 1
    dict_foll = dict(count_glob_foll)
    pandas_follow = pd.DataFrame(dict_foll.items(), columns=['follows', 'n_of_follows'])
    print(pandas_follow.head())
    pandas_follow.to_csv('follows.csv', sep='\t')
    print(f'Saved CSV for {comptetitor_file}')

#Starting Chrome Browser
driver = webdriver.Chrome(params.path_to_exec)
login(driver)

global_following = []

#Insert path to competitors followers list
followers = pd.read_csv(params.csv_name, sep='\t')
followers = followers['followers'].values.tolist()

i = 0
private_accounts = 0
for follower in followers:
    if is_blocked == True:
        break
    else:
        print('Followers to scrape: ' + str(len(followers) - i))
        i += 1
        try:
            time.sleep(3)
            following = fetch_following(driver, str(follower))
            global_following.append(following)
            print(f'Fetched followers for {follower}')
        except:
            print(f'Account {follower} is private, couldnt fetch following')
            private_accounts += 1
            pass

exit_handler()
print(f'The numbe rof private accounts was {private_accounts}')
