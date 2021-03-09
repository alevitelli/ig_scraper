# ig_scraper
## Overview
Instagram scraper fetches sample of followers from target pages and in turn, for each of those followers, scrapes a sample of other pages those followers follow. The aim of the scraper is to get a sense of what are the common influencers of the people who follow a specific page. _What other pages do people who follow Telsa follow?".

> _What other pages do people who follow Telsa follow?_

The output of the final file will be of the sorts:

`tesla_scraped.csv`

| Acccount  | Number of Followers | Percentage |
| ------------- | ------------- | ------------- |
| Telsa  | 12,000  | 100%  | 
| Elon Musk  | 10,790  | 89%  | 
| Grimes  | 7,657  | 63%  | 

## Usage
Access to params.py file in order to specifiy relevant information such as:
- path to chrome drive (you can download the chrome driver [here](https://chromedriver.chromium.org/downloads)
- Instagram username and password
- Instagram account name to scrape

## Caveat
The scraper was coded in 2018. Since then, IG might have changed XPATHs of many elements on it's website. Some debugging might be required.


