#################################################################################
##################            DESCRIPTION                    ####################
#################################################################################

# FETCHES MAX 1.5K FOLLOWINGS FOR EACH FOLLOWER IN THE COMPETITOR'S CSV
# AGGREGATES ALL FOLLOWINGS AND CREATES CSV WITH FREQUENCIES

#################################################################################
##################            REQUIREMENTS                   ####################
#################################################################################

# DOWNLOAD EXEC DRIVER FOR YOUR BROWSER - SPECIFY PATH TO EXEC
# INSERT INSTAGRAM CREDENTIALS
# DEFINE PATH TO COMPETITOR'S FILE

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
import atexit

comptetitor_file = ''
competitors_csv = f'./followers_competitors/{comptetitor_file}.csv'
path_to_exec = #'/Users/alessandro.vitelli/Downloads/chromedriver'

#Define Competitors
ig_usr = ''
ig_pwd = ''
competitors = []
is_blocked = False

#Login into Instagram
def login(driver):
    usr = ig_usr
    pwd = ig_pwd
    driver.get('https://www.instagram.com/blueapron/followers')
    time.sleep(2)
    driver.find_element_by_name("username").send_keys(usr)
    driver.find_element_by_name("password").send_keys(pwd)
    time.sleep(1)
    driver.find_elements(By.XPATH, '//button')[0].click()
    time.sleep(2)

#Extract followers info once they have loaded
def extract_foll_info(driver, account, var):
    css_sel = "body > div:nth-child(12)"
    foll_box = driver.find_element_by_css_selector(css_sel)
    xpath = '/html/body/div[3]/div/div[2]/div/div[2]/ul/div'
    links = foll_box.find_element_by_xpath(xpath).text
    links_final = [link.split('\n')[0] for link in links.split('\nFollow\n')]
    if var == True:
        df_followers = pd.DataFrame({'followers': links_final})
        csv_name = 'followers_' + str(account) + '.csv'
        df_followers.to_csv(csv_name, sep='\t')
        print('Fetched all info and created csv file')
    elif var == False:
        return links_final
        print('Fetched all info for ' + str(account))

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
    foll_list = extract_foll_info(driver, account, False)
    return foll_list

def exit_handler():
    global global_following
    flat_glob_foll = [item for sublist in global_following for item in sublist]
    from collections import Counter
    count_glob_foll = Counter()
    for follow in flat_glob_foll:
        count_glob_foll[follow] += 1
    dict_foll = dict(count_glob_foll)
    pandas_follow = pd.DataFrame(dict_foll.items(), columns=['follows', 'n_of_follows'])
    print(pandas_follow.head())
    pandas_follow.to_csv('follows.csv', sep='\t')
    print(f'Saved CSV for {comptetitor_file}')

#Starting Chrome Browser
driver = webdriver.Chrome(path_to_exec)
login(driver)

global_following = []

#Insert path to competitors followers list
followers = pd.read_csv(competitors_csv, sep='\t')
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
