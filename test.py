from ctypes.wintypes import tagSIZE
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import httplib2
from oauth2client import client, GOOGLE_TOKEN_URI
from datetime import datetime
import csv
import requests
import json
import shutil
import os
import re

CLIENT_ID1 = os.environ.get("CLIENT_ID1")
CLIENT_SECRET1 = os.environ.get("CLIENT_SECRET1")
REFRESH_TOKEN1 = os.environ.get("REFRESH_TOKEN1")
print(f"{CLIENT_ID1}\n\n{CLIENT_SECRET1}\n\n{REFRESH_TOKEN1}")

with open("channels.json", "r") as f:
    allchans = json.load(f)

channelsdata = []
channels = []
for c in allchans:
    if allchans[c] == False: # if not already scrapped
        channels.append(c)

# "UC4DnCSjFjEJnlCG-kui53iA"

credentials = client.OAuth2Credentials( # set up creds
    access_token = None, 
    client_id = CLIENT_ID1, 
    client_secret = CLIENT_SECRET1, 
    refresh_token = REFRESH_TOKEN1, 
    token_expiry = None, 
    user_agent = None,
    token_uri = GOOGLE_TOKEN_URI,
    revoke_uri= None)
http = credentials.authorize(httplib2.Http())
youtube = googleapiclient.discovery.build(
    'youtube', 'v3', credentials=credentials)

for c in channels:
    
    videoIds = []
        
    uploadsPList = list(c) # get the uploads playlist from channel id
    uploadsPList[1] = 'U'
    uploadsPList = ''.join(uploadsPList)

    nextPageToken = ""
    
    while nextPageToken != None:
        request = {'items':[f"v1{c}", f"v2{c}", f"v3{c}"]}
        
        try:
            nextPageToken = request['nextPageToken'] # update nextpage token
        except:
            nextPageToken = None

        for v in request['items']:
            
            daysSinceUpload=60

            
            durationSeconds = 100

            if daysSinceUpload > 30 and daysSinceUpload < 1095 and int(durationSeconds) > 60: # if the video was uploaded between 1 month to 3 years ago, and is not a shorts video: add its id to a list
                videoIds.append(v['contentDetails']['videoId'])
            
    for v in videoIds:
        print(v)
        request = youtube.videos().list(
            part="snippet",
            id=v
        ).execute()['items'][0]['snippet']
        title = request['title'].replace("u'", "'")
        thumbnailURL = request['thumbnails']['default']['url']
        date = request['publishedAt']
        channelName = request['channelTitle']
        try:
            tags = request['tags']
        except:
            tags = []

        request = youtube.videos().list(
            part="statistics",
            id=v
        ).execute()['items'][0]['statistics']
        views = request['viewCount']

        channelsdata.append([c, channelName, title, views, thumbnailURL, date, tags, duration])

        res = requests.get(thumbnailURL, stream = True) # download thumbnail
        with open(f"thumbnails/{v}.jpg",'wb') as f:
            shutil.copyfileobj(res.raw, f)

    allchans[c] = True
    with open("channels.json", "w") as f:
        json.dump(allchans, f, indent=4)
    
        # writing to csv file
    with open("data.csv", 'a', encoding="utf-8", newline='') as f:
        # creating a csv writer object
        writer = csv.writer(f)
        
        # writing the data rows
        writer.writerows(channelsdata)
    


print('done')
    


    

    
# from channel id:
#   get all videos within constaints (3 month to 3 year)
#       contentDetails.relatedPlaylists.uploads
#   for each video get title, thumbnail, viewcount
#   store csv / json index

