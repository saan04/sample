import io
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
import moviepy.editor as mp
from tkinter.filedialog import *
import requests
import re
import json
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd


gauth = GoogleAuth()
drive = GoogleDrive(gauth)
parent_folder_id = '1Id92qts3NEJD-o_9h-hcTst6GgSko6ce'
def upload_file(file_path):
     file = drive.CreateFile({'title':file_path, 'parents':[{'id': parent_folder_id}]})
     file.SetContentFile(file_path)
     file.Upload()
     return file['id']

def upload_csv(file_path):
    file = drive.CreateFile(({'title':file_path, 'parents':[{'id':parent_folder_id}]}))
    file.SetContentFile(file_path)
    file.Upload()
    return file['id']

base_url = "https://www.ted.com"
proxies = {
    "http": "http://scraperapi:d4193e32c7679a06a0fd633921340a51@proxy-server.scraperapi.com:8001",
    "https": "http://scraperapi:d4193e32c7679a06a0fd633921340a51@proxy-server.scraperapi.com:8001"
}

url = "https://www.ted.com/talks?sort=newest&language=hi"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

a_element = soup.find_all('a',attrs={'class': 'ga-link', 'data-ga-context': 'talks', 'lang' : 'hi'})

url_list=[]
for a in a_element:
    href = a.get('href')
    url_list.append(href)

for list in url_list:
    print(list)

i=0
for list in url_list:
    url = base_url+list
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    languages = []
    link_tags = soup.find_all('link', rel='alternate')

    next_data_script = soup.find(id="__NEXT_DATA__")
    next_data_json = next_data_script.string
    player_data = json.loads(next_data_json)['props']['pageProps']['videoData']['playerData']
    url_content = json.loads(player_data)['resources']['h264'][0]['file']
    mp4_response = requests.get(url_content)
    file_name = f"vid{i}.mp4"
    with open(file_name, 'wb') as f:
        f.write(mp4_response.content)

    video = mp.VideoFileClip(file_name)
    aud = video.audio
    audio_file_path = f"audio{i}.mp3"
    aud.write_audiofile(audio_file_path)

    file_id = upload_file(audio_file_path)
    print(file_id)
    i=i+1

j=0
for list in url_list:
    url = base_url + list
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    languages = []
    link_tags = soup.find_all('link', rel='alternate')

    for link_tag in link_tags:
        language = link_tag.get('hreflang')
        if language is not None and language != 'x-default':
            languages.append(language)
    print(languages)
    mydict = {}

    for lan in languages:
        new_url = url.replace("=hi","="+lan)
        print(new_url)
        r = requests.get(new_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        next_data_transcript = soup.find('script', {'type': 'application/ld+json'})
        if next_data_transcript is not None:
            transcript_dict = next_data_transcript.string
            transcript_dict = json.loads(transcript_dict)
            mydict[lan] = transcript_dict.get('transcript')

    for key, value in mydict.items():
        print(key, value)

    df = pd.DataFrame.from_dict(mydict, orient="index")
    df_name = f"data{j}.csv"
    df.to_csv(df_name)
    upload_csv(df_name)
    j=j+1



