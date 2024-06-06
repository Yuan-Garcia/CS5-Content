# does everything in print statements

import json
import collections

file_names = [
    "Streaming_History_Audio_2016-2019_0.json",
    "Streaming_History_Audio_2019-2020_1.json",
    "Streaming_History_Audio_2020-2021_2.json",
    "Streaming_History_Audio_2021_3.json",
    "Streaming_History_Audio_2021-2022_4.json",
    "Streaming_History_Audio_2022_5.json",
    "Streaming_History_Audio_2022-2023_6.json",
    "Streaming_History_Audio_2023-2024_7.json",
    "Streaming_History_Audio_2024_8.json",
]

data = []
for file_name in file_names:
    with open(file_name, "r") as f:
        data += json.load(f)


# print(f"Dictionary: {data}")

# for dictionary in data:
#     print(dictionary.get("master_metadata_track_name"))

# prints top track with its artist listened to all time
countTracksArtists = {}
for dictionary in data:
    trackName = dictionary.get("master_metadata_track_name")
    trackArtist = dictionary.get("master_metadata_album_artist_name")
    if trackName and trackArtist:
        pair = (trackName, trackArtist)
        if pair not in countTracksArtists:
            countTracksArtists[pair] = 1
        else:
            countTracksArtists[pair] += 1

sortedTracks = dict(sorted(countTracksArtists.items(), key=lambda item: item[1], reverse=True))
topTrack = next(iter(sortedTracks))
topTrackName = topTrack[0]
topTrackArtist = topTrack[1]
print("Florence's top track of all time is: " + topTrackName + " by " + topTrackArtist)


# prints top artist listened to all time
countArtists = {}
for dictionary in data:
    trackArtist = dictionary.get("master_metadata_album_artist_name")
    if trackArtist:
        if trackArtist not in countArtists:
            countArtists[trackArtist] = 1
        else:
            countArtists[trackArtist] += 1
sortedTacks = dict(sorted(countArtists.items(), key=lambda item: item[1], reverse=True))
topArtist = next(iter(sortedTacks))
print("Florence's top artist of all time is: " + topArtist)



# prints top track with its artist listened to in the last year
# uses collections module to handle counting of tracks
countTracks2024 = collections.defaultdict(int)
for dictionary in data:
    trackName = dictionary.get("master_metadata_track_name")
    trackArtist = dictionary.get("master_metadata_album_artist_name")
    timeStamp = dictionary.get("ts")
    if timeStamp.startswith("2023") and trackName and trackArtist:
        pair = (trackName, trackArtist)
        countTracks2024[pair] += 1
sortedTracks = dict(sorted(countTracks2024.items(), key=lambda item: item[1], reverse=True))
topTrack = next(iter(sortedTracks))
topTrackName = topTrack[0]
topTrackArtist = topTrack[1]
print("Florence's top track in 2024 is: " + topTrackName + " by " + topTrackArtist)


#prints most listened to album of all time
countalbums = {}
for dictionary in data:
    albumName = dictionary.get("master_metadata_album_album_name")
    if albumName not in countalbums:
        countalbums[albumName] = 1
    else:
        countalbums[albumName] += 1
sortedAlbums = dict(sorted(countalbums.items(), key=lambda item: item[1], reverse=True))
topAlbum = next(iter(sortedAlbums))
print("Florence's top album of all time is: " + str(topAlbum))


