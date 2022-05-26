#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mon Mar 21 00:53:03 2022
@author: adeleh
'''
import urllib
import requests
import panda as pd
from my_fake_useragent import UserAgent
from requests_html import HTMl
from requests_html import HTMLSession
from bs4 import BeautifulSoup

Search_item = "plants"
number_result =100
User_Agent = {
        'User-Agent': 
  "args" , 
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "en-us", 
    "Host": "httpbin.org", 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15", 
    "X-Amzn-Trace-Id": "Root=1-62380878-37f2ea371f802f5972280aae"
  }, 
  "origin": "158.222.133.218", 
  "url": "https://httpbin.org/get"
}
    
bing_url = "https://www.bing.com/search?q=" + Search_item + "&number_result" + str(number_result)
response= requests.get(bing_url, {User_Agent : User_Agent})
soup = Beautifulsoup(response.text, "html.parser")
result_div = soup.find_all('div', attrs = {'class' : 'ZINbbc'})

links = []
titles = []
descriptions = []
for r in result_div:
     try:
        link = r.find('a' , href = True)
        title = r.find('dive', attrs = {'class':'vvjwb'}).get_text()
        description= r.find('dive', attrs = {'class':'a3v9rd'}).get_text()
         
        if link != '' and title != '' and description != '':
             links.append(link['href'])
             titles.append(link['href'])
             descriptions.eppend(description)
     except:
         continue
print(links)