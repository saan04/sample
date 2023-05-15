import requests
import re
import json
#used BeautifulSoup as webscraping tool
from bs4 import BeautifulSoup
import pandas as pd

#using proxy for a bulk scraping of data to be done securely
proxies = {
    "http": "http://scraperapi:d4193e32c7679a06a0fd633921340a51@proxy-server.scraperapi.com:8001",
    "https": "http://scraperapi:d4193e32c7679a06a0fd633921340a51@proxy-server.scraperapi.com:8001"
}

#as video was previously decided used it as a base url
b_url = "https://www.ted.com/talks/stephanie_honchell_smith_the_rise_and_fall_of_the_mughal_empire?language="
url = "https://www.ted.com/talks/stephanie_honchell_smith_the_rise_and_fall_of_the_mughal_empire?language=hi"

r = requests.get(url,proxies=proxies,verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

#the aim is to get transcripts in multiple languages
#initialising a list for range of languages available
languages = []
link_tags = soup.find_all('link', rel='alternate')

for link_tag in link_tags:
    language = link_tag.get('hreflang')
    if language is not None and language!='x-default':
        languages.append(language)

#printing languages available
print(languages)

#initialising a dictionary to keep track of language and transcript
mydict = {}
for lan in languages:
    url = b_url+lan
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    next_data_transcript = soup.find('script', {'type': 'application/ld+json'})
    transcript_dict = next_data_transcript.string
    transcript_dict = json.loads(transcript_dict)
    mydict[lan] = transcript_dict.get('transcript')

#printing dictionary
for key,value in mydict.items():
    print(key,value)

#conversion of dicrionary into csv format
df = pd.DataFrame.from_dict(mydict,orient="index")
df.to_csv("data.csv")