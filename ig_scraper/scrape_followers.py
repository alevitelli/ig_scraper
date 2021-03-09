#################################################################################
##################            DESCRIPTION                    ####################
#################################################################################

# FETCHES MAX 1.5K FOLLOWINGS FOR EACH FOLLOWER IN THE COMPETITOR'S CSV
# AGGREGATES ALL FOLLOWINGS AND CREATES CSV WITH FREQUENCIES

import params as params
from utils import login, return_foll_info, fetch_following, exit_handler

is_blocked = False

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
