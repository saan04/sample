import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
import moviepy.editor as mp
from tkinter.filedialog import *
import requests
import re
import json
#used BeautifulSoup as webscraping tool
from bs4 import BeautifulSoup

#using proxy for a bulk scraping of data to be done securely
proxies = {
    "http": "http://scraperapi:d4193e32c7679a06a0fd633921340a51@proxy-server.scraperapi.com:8001",
    "https": "http://scraperapi:d4193e32c7679a06a0fd633921340a51@proxy-server.scraperapi.com:8001"
}

#accessed url of said video
url = "https://www.ted.com/talks/stephanie_honchell_smith_the_rise_and_fall_of_the_mughal_empire?language=hi"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url,proxies=proxies,verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

#the content required was present in a json object
next_data_script = soup.find(id="__NEXT_DATA__")
next_data_json = next_data_script.string

player_data = json.loads(next_data_json)['props']['pageProps']['videoData']['playerData']
url_content = json.loads(player_data)['resources']['h264'][0]['file']
mp4_response = requests.get(url_content)

#waiting to see if accessible
print(mp4_response)

#giving a random file name
file_name = 'talk.mp4'
with open(file_name,'wb') as f:
     f.write(mp4_response.content)

#as the requirement was of an audio
#conversion of video to an audio
#the website did not have a .mp3 format audio clip to access
video = mp.VideoFileClip(file_name)
aud = video.audio

#output audio obtained
aud.write_audiofile("demo.mp3")



