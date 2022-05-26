#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install search_engines


# In[27]:


pip install my_fake_useragent


# In[ ]:


get_ipython().system('pip install -U duckduckgo_search')


# In[28]:


import pandas as pd
import numpy as np
import urllib
from my_fake_useragent import UserAgent
import requests
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

ua = UserAgent()
query="plants"
number_result=100
google_url = "https://google.com/search?q=" + query + "&num=" + str(number_result)
response = requests.get(google_url, {"User-Agent": ua.random})
soup = BeautifulSoup(response.text, "html.parser")

result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

links = []
titles = []
descriptions = []
for r in result_div:
    # Checks if each element is present, else, raise exception
    try:
        link = r.find('a', href = True)
        title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
        description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
        
        # Check to make sure everything is present before appending
        if link != '' and title != '' and description != '': 
            links.append(link['href'])
            titles.append(title)
            descriptions.append(description)
    # Next loop if one element is not present
    except:
        continue

print(len(links))


# In[ ]:



from duckduckgo_search import ddg

keywords = 'medicinal plants'
results = ddg(keywords, region='wt-wt', safesearch='Moderate', time='y', max_results=200)
print(results)

