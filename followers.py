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
from utils import login, fetch_followers
import params as params

#Starting Chrome Browser
driver = webdriver.Chrome(params.path_to_exec) 
login(driver)

#Extracting followers for target account (15k sample)
print('Fetching followers for ' + str(params.account))

fetch_followers(driver)

print('Fetched followers for ' + str(params.account))
