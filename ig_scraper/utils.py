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
    time.sleep(5)

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
