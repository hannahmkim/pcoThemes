import json
import re


#shameless copy paste from json/decoder.py
# FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
# WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

# class ConcatJSONDecoder(json.JSONDecoder):
#     def decode(self, s, _w=WHITESPACE.match):
#         s_len = len(s)

#         objs = []
#         end = 0
#         while end != s_len:
#             obj, end = self.raw_decode(s, idx=_w(s, end).end())
#             end = _w(s, end).end()
#             objs.append(obj)
#         return objs

allSongs = {}
songs = json.load(open('songs0.txt')) 
for song in songs.get("data"):
	id = song.get("id")
	title = song.get("attributes").get("title")
	allSongs[title] = id

# songs = json.load(open('songs100.txt')) 
# for song in songs.get("data"):
# 	id = song.get("id")
# 	title = song.get("attributes").get("title")
# 	allSongs[title] = id
# songs = json.load(open('songs200.txt')) 
# for song in songs.get("data"):
# 	id = song.get("id")
# 	title = song.get("attributes").get("title")
# 	allSongs[title] = id
# songs = json.load(open('songs300.txt')) 
# for song in songs.get("data"):
# 	id = song.get("id")
# 	title = song.get("attributes").get("title")
# 	allSongs[title] = id
# songs = json.load(open('songs400.txt')) 
# for song in songs.get("data"):
# 	id = song.get("id")
# 	title = song.get("attributes").get("title")
# 	allSongs[title] = id

with open('allSongs.txt', 'w') as f:
	for song in allSongs:
		f.write(song.encode('utf-8'))
		f.write('\t')
		f.write(allSongs[song].encode('utf-8'))
		f.write('\n')
