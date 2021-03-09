from bs4 import BeautifulSoup
import requests
import json
import time
import random
import atexit
from collections import Counter
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import params

#Login into Instagram
def login(driver):
    #Access random page to prompt logic
    driver.get('https://www.instagram.com/blueapron/followers')
    time.sleep(2)
    driver.find_element_by_name("username").send_keys(params.usr)
    driver.find_element_by_name("password").send_keys(params.pwd)
    time.sleep(1)
    driver.find_elements(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')[0].click()
    print("Logged In")
    time.sleep(45)

#Loads 15k followers for an account
def fetch_followers(driver):
    driver.get('https://www.instagram.com/' + str(params.account))
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
    extract_foll_info(driver)
    print('Process Complete for ' + str(params.account))   

#Extract followers info once they have loaded
def extract_foll_info(driver):
    css_sel = f"body > div:nth-child(12)"
    foll_box = driver.find_element_by_css_selector(css_sel)
    xpath = '/html/body/div[4]/div/div[2]/div/div[2]/ul/div'
    links = foll_box.find_element_by_xpath(xpath).text
    links_final = [link.split('\n')[0] for link in links.split('\nFollow\n')]
    df_followers = pd.DataFrame({'followers': links_final})
    df_followers.to_csv(params.csv_name, sep='\t')
    print('Fetched all info and created csv file')    

def return_foll_info(driver):
    css_sel = "body > div:nth-child(12)"
    foll_box = driver.find_element_by_css_selector(css_sel)
    xpath = '/html/body/div[3]/div/div[2]/div/div[2]/ul/div'
    links = foll_box.find_element_by_xpath(xpath).text
    links_final = [link.split('\n')[0] for link in links.split('\nFollow\n')]
    return links_final
    print('Fetched all info for ' + str(params.account))    

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
