# updatePCOTitles.py
# updates the titles of the songs in the PCO db. used bc we changed songs that started with "The ..." to be coded by the first significant word rather than "T"
# 	ex) T00x - The Stand 	--> 	S00x - The Stand
# in: update.csv (all the titles to update) 
# out: nothing

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json

toUpdate = pd.read_csv('update.csv')

head = {"Authorization": "InsertAuthorizationKeyHERE!"}

for song in toUpdate.itertuples():
	ID = int(song[1])
	title = str(song[2])

	request = """ 
		{{
		    "data": {{
		        "type": "Song",
		        "id": {0},
		        "attributes": {{
		        	"title": "{1}"
		        }},
		        "relationships": {{
		        }}
		    }}
		}} 
	""".format(ID, title)

	r = requests.patch('https://api.planningcenteronline.com/services/v2/songs/{0}'.format(ID), data=request, headers=head)
	print r.status_code