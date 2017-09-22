import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json

toUpdate = pd.read_csv('update.csv')

head = {"Authorization":"Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy"}

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