import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json

# songs.csv - spreadsheet with songs & themes
allSongs = pd.read_csv('themes.csv')

head = {"Authorization":"Basic MmVhYTc2NTVkYzExZDFjNzFhODI5NmQ2ODkyMmE0MTAwOTkxZDQ2NmNjYzM1ZmJhOWZjOGMxZWQyZDI5MWUxZjphMmZhZWEyNDc1MmZhMTRjYzEzM2UzNjRlMmFjM2IzMzEyYmI5OWEzYWY0ZTEyNTEzODg2NzJjZTQ4ZTNlZmYy"}

tagID = {
	"Children": "6904402",
	"Contemporary": "6904403",
	"Gospel": "6904404",
	"Traditional": "6904405",
	"Adoration": "6904406",
	"Celebratory": "6904407",
	"Declarative": "6904408",
	"Desperation & Dependence": "6904409",
	"Reflection & Prayer": "6904410",
	"Communion": "6904443",
	"Offering": "6904444",
	"Call to Worship": "6904445",
	"Christmas": "6904446",
	"Church & Unity": "6904447",
	"Commitment & Dedication": "6904448",
	"Freedom": "6904449",
	"God's Faithfulness": "6904450",
	"God's Greatness, Power, Glory": "6904451",
	"God's Kingdom & Reign": "6904452",
	"God's Love & as Father": "6904453",
	"God's Presence & Intimacy": "6904454",
	"Holiness & Purity": "6904455",
	"Holy Spirit": "6904456",
	"Hope": "6904457",
	"Jesus' Life, Death, & Resurrection": "6904458",
	"Missions, Evangelism, The Nations": "6904459",
	"Our Testimony & Redemption": "6904460",
	"Repentance": "6904461",
	"Surrender": "6904462",
	"Thankfulness & Adoration": "6904463",
	"Trust": "6904464"
}

for song in allSongs.itertuples():
	# ID number of song
	ID = int(song[1])

	# empty list for the themes
	tags = []

	# fills tags with the themes for that song
	for x in range(3,8):
		if isinstance(song[x], str):
			tags.append(
				{
					"type": "Tag",
					"id": tagID[song[x]]
				}
			)

	request = """ 
		{{
		    "data": {{
		        "type": "TagAssignment",
		        "attributes": {{

		        }},
		        "relationships": {{
		            "tags": {{
		                "data": {0}
		            }}
		        }}
		    }}
		}} 
	""".format(json.dumps(tags))

	# # make request...
	r = requests.post('https://api.planningcenteronline.com/services/v2/songs/{0}/assign_tags'.format(ID), data=request, headers=head)

	# # check for success!
	print r.status_code, r.reason
