import json
import re

allSongs = {}

# There are 5 separate txt files that contain object for each song in our database.
# Format of song object is...
# song = {
#   "data": {
#     "type": "Song",
#     "id": "primary_key",
#     "attributes": {
#       "admin": "string",
#       "author": "string",
#       "ccli_number": 1,
#       "copyright": "string",
#       "created_at": "2000-01-01T12:00:00Z",
#       "hidden": true,
#       "themes": "string",
#       "title": "string",
#       "updated_at": "2000-01-01T12:00:00Z"
#     },
#     "relationships": {
#     }
#   }
# }
for x in range(0, 500, 100):
	songs = json.load(open('songs{0}.txt').format(x))
	for song in songs.get("data"):
		id = song.get("id")
		title = song.get("attributes").get("title")
		allSongs[title] = id

# This creates a new txt file compiling the necessary information (in our case just ID and title)
with open('allSongs.txt', 'w') as f:
	for song in allSongs:
		f.write(song.encode('utf-8'))
		f.write('\t')
		f.write(allSongs[song].encode('utf-8'))
		f.write('\n')

# The end result of this file was used to have a template for people to manually input themes and attributes to each song so we could classify them.
# Now see updatePCO.py