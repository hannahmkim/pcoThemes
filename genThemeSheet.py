# import pandas as pd
import requests
import json
import re

head = {"Authorization":"Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy"}

allTags = {}
allSongs = {}

# Fetch songs
songsReq = requests.get('https://api.planningcenteronline.com/services/v2/songs/?per_page=5', headers=head)
songsObj = json.loads(songsReq.text)

# For each song in that set... ###########################################################################

for song in songsObj["data"]:
    title = song["attributes"]["title"]
    link = song["links"]["self"]

    # Get all the info for that song... ##################################################################
    songReq = requests.get('{0}/arrangements'.format(link), headers=head)
    songObj = json.loads(songReq.text)

    allSongs[title] = {}

    # Get first line...
    firstLine = songObj["data"][0]["attributes"]["chord_chart"]
    firstLine = firstLine.splitlines()[1]
    firstLine = re.sub('(\\[.*?\\])', '', firstLine)
    allSongs[title]["firstLine"] = firstLine

    # And BPM...
    allSongs[title]["BPM"] = songObj["data"][0]["attributes"]["bpm"]

    # And all keys...
    allSongs[title]["keys"] = []
    for arr in songObj["data"]:
        key = arr["attributes"]["chord_chart_key"]
        allSongs[title]["keys"].append(key)
    ###################################################################################################### 

    # Get all the tags for that song... ##################################################################
    tagsReq = requests.get('{0}/tags'.format(link), headers=head)
    tagsObj = json.loads(tagsReq.text)

    for songTag in tagsObj["data"]:
        tag = songTag["attributes"]["name"]

        if tag not in allTags:
            allTags[tag] = []

        # And map that song to that theme!
        allTags[tag].append(title)
    ###################################################################################################### 

##########################################################################################################

# # Generate excel sheet data...
# for tag in allTags:
#     print tag

#     # TODO: alphabetize here?
    
#     for song in allTags[tag]:
#         print allSongs[song]
