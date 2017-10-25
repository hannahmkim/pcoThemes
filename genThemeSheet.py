import requests
import json
import re
import csv
import pandas as pd
import xlsxwriter

# For each song in that set... ###########################################################################
def getSongData(songsObj, allSongs, allTags, head):
    for song in songsObj["data"]:
        title = song["attributes"]["title"]
        link = song["links"]["self"]

        # Get all the info for that song...
        songReq = requests.get('{0}/arrangements'.format(link), headers=head)
        songObj = json.loads(songReq.text)

        allSongs[title] = {}

        # Get first line...
        try: 
            firstLine = songObj["data"][0]["attributes"]["chord_chart"]
            firstLine = firstLine.splitlines()[1]
            firstLine = re.sub('(\\[.*?\\])', '', firstLine)
        except:
            firstLine = "sorry, you have to manually get first line... idk why"
        allSongs[title]["firstLine"] = firstLine

        # And BPM...
        try:
            allSongs[title]["BPM"] = songObj["data"][0]["attributes"]["bpm"]
        except: 
            allSongs[title]["BPM"] = "sorry, you have to manually get bpm... idk why"

        # And all keys...
        allSongs[title]["keys"] = []
        for arr in songObj["data"]:
            try:
                key = arr["attributes"]["chord_chart_key"]
            except:
                key = "sorry, you have to manually get key... idk why"
            allSongs[title]["keys"].append(key)

        # Get all the tags for that song... 
        tagsReq = requests.get('{0}/tags'.format(link), headers=head)
        tagsObj = json.loads(tagsReq.text)

        for songTag in tagsObj["data"]:
            tag = songTag["attributes"]["name"]

            if tag not in allTags:
                allTags[tag] = []

            # And map that song to that theme!
            allTags[tag].append(title)

    for tag in allTags:
        allTags[tag].sort()
###################################################################################################### 

##########################################################################################################
# Version 1 generates a csv file using pandas
def genCSV(allTags, allSongs):
    df = pd.DataFrame()

    for tag in allTags:
        # apply formatting for section header
        df = df.append([tag], ignore_index=True)

        for song in allTags[tag]:
            # apply formatting for song 
            df = df.append([[ song, allSongs[song]["firstLine"], allSongs[song]["BPM"], allSongs[song]["keys"] ]], ignore_index=True)

    df.to_csv(open('themeSheet.csv', 'wb'), sep='\t', encoding='utf-8')
##########################################################################################################

##########################################################################################################
# Version 2 generates xls file using xlsxwriter
def genXLS(allTags, allSongs, head):

    workbook = xlsxwriter.Workbook('themeSheet.xlsx')
    worksheets = {}

    # stylessssss
    sectionStyle = workbook.add_format({'bold': True, 'font_name': 'Avenir', 'bg_color': 'black', 'font_color': 'white', 'font_size': 10})
    songCenterStyle = workbook.add_format({'bold': True, 'font_name': 'Avenir', 'bottom': 4, 'align': 'center', 'font_size': 10})
    songStyle = workbook.add_format({'bold': True, 'font_name': 'Avenir', 'bottom': 4, 'font_size': 10})

    # getting tag groups
    # allTagGroups = { idOfTagGroup --> alphabetical list of ids of children tags }
    tagGroups = requests.get('https://api.planningcenteronline.com/services/v2/tag_groups', headers=head)
    tagGroupObj = json.loads(tagGroups.text)
    allTagGroups = {}
    for tagGroup in tagGroupObj["data"]:
        if tagGroup["attributes"]["tags_for"] == 'song':
            worksheets[tagGroup["attributes"]["name"]] = workbook.add_worksheet()

            allTagGroups[tagGroup["attributes"]["name"]] = []
            r = requests.get('https://api.planningcenteronline.com/services/v2/tag_groups/{0}/tags'.format(tagGroup["id"]), headers=head)
            groupData = json.loads(r.text)
            for tag in groupData["data"]:
                allTagGroups[tagGroup["attributes"]["name"]].append(tag["attributes"]["name"])

            sorted(allTagGroups[tagGroup["attributes"]["name"]])

    for tagGroup in allTagGroups:
        worksheet = worksheets[tagGroup]
        worksheet.hide_gridlines(2)
        worksheet.set_column('A:A', 3)
        worksheet.set_column('B:B', 40)
        worksheet.set_column('C:C', 55)
        worksheet.set_column('D:D', 7)
        worksheet.set_column('E:E', 7)

        row = 0
        try:
            for tag in allTagGroups[tagGroup]:
                worksheet.merge_range(row, 0, row, 4, tag, sectionStyle)
                row += 1

                for song in allTags[tag]:
                    worksheet.write(row, 1, song, songStyle)
                    worksheet.write(row, 2, allSongs[song]["firstLine"], songStyle)
                    worksheet.write(row, 3, allSongs[song]["BPM"], songCenterStyle)
                    # regex gets rid of unicode and random quotes and stuff
                    keys = re.sub('([\\[\\]\'u])', '', str(allSongs[song]["keys"]))
                    worksheet.write(row, 4, keys, songCenterStyle)
                    row += 1    
        except:
            continue

        
##########################################################################################################

def main():
    head = {"Authorization":"Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy"}

    allTags = {}
    allSongs = {}

    # Fetch songs
    for x in range(0, 500, 100):
        songsReq = requests.get('https://api.planningcenteronline.com/services/v2/songs/?per_page=100&offset={0}'.format(x), headers=head)
        songsObj = json.loads(songsReq.text)
        getSongData(songsObj, allSongs, allTags, head)

    # genCSV(allTags, allSongs)
    genXLS(allTags, allSongs, head)

main()
