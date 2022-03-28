import webbrowser
import pandas as pd
import numpy as np
import urllib
from my_fake_useragent import UserAgent
import requests
import re
from duckduckgo_search import ddg
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
#get_ipython().system('pip install -U duckduckgo_search')

#new=2

#tabUrl="http://google.com/search?q=";
#term= input("Enter search query:");

#webbrowser.open(tabUrl+term,new=new);

query="plants"
number_result=100
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
yahoo_url="https://search.yahoo.com/search?p=" + query + "&number_result" + str(number_result)
response = requests.get(yahoo_url, {"User-Agent": User_Agent})
soup = BeautifulSoup(response.text, "html.parser")

result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

links = []
titles = []
descriptions = []
for r in result_div:
    
    try:
        link = r.find('a', href = True)
        title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
        description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
        
        # Check to make sure everything is present before appending
        if link != '' and title != '' and description != '': 
            links.append(link['href'])
            titles.append(title)
            descriptions.append(description)
    
    except:
        continue

print(len(links))



keywords = 'flower plants'
results_div = ddg(keywords, region='wt-wt', safesearch='Moderate', time='y', max_results=200)
print(results_div)

