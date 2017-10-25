import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json

# themes.csv is spreadsheet with songs mapped to relevant themes
# Format of one line in themes is 
# song[1]	song[2]		song[3]		song[4]		song[5]		song[6-8]
# ID 		TITLE 		Genre 		Mood 		Purpose		Theme(s)
allSongs = pd.read_csv('themes.csv')

# Authorization for our API endpoint (deleted for privacy)
head = {"Authorization":"InsertAuthorizationKeyHERE!"}

# Mapping of themes to themeID as specified in our API endpoint
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

# This segment takes the information in themes.csv and sends it to our API endpoint to auto-input tags for each song in database.
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

	# request body
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

# The end result is that our Planning Center databse is updated with the tags and songs are easily filterable by tag
