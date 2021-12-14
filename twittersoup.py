#Get the webpage
# Load libraries for web scraping
from bs4 import BeautifulSoup
import requests
from lxml import etree
# Get a soup from a URL
burl = 'https://twitter.com/DababyDababy'
r = requests.get(burl)
soup = BeautifulSoup(r.content, 'html.parser')
tags = soup.find_all("/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[2]/a/span[1]/span")
followers = soup.get("/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[2]/a/span[1]/span")
print(tags)
print('done')