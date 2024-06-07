# does what printsResults.py does but returns instead of prints
import json
import collections

# retrieve all the data from json files
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



# functions that return based on data collected all time

def top_track(data):
    """
        returns the top track and artist listened to all time
    """
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
    return topTrackName, topTrackArtist

# print to test
print("Florence's top track of all time is: " + top_track(data)[0] + " by " + top_track(data)[1])


def top_artist(data):
    """
        returns the top artist listened to all time
    """
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
    return topArtist

# print to test
print("Florence's top artist of all time is: " + top_artist(data))


def top_album(data):
    """
        returns the top album listened to all time
    """
    countAlbums = {}
    for dictionary in data:
        albumName = dictionary.get("master_metadata_album_album_name")
        if albumName:
            if albumName not in countAlbums:
                countAlbums[albumName] = 1
            else:
                countAlbums[albumName] += 1
    sortedAlbums = dict(sorted(countAlbums.items(), key=lambda item: item[1], reverse=True))
    topAlbum = next(iter(sortedAlbums))
    return topAlbum

# print to test
print("Florence's top album of all time is: " + top_album(data))
print("\n")



# functions that return based on data collected based on input year

def top_track_year(data, year):
    """
        returns the top track and artist listened to based on the input year
    """
    countTracksYear = collections.defaultdict(int)
    for dictionary in data:
        trackName = dictionary.get("master_metadata_track_name")
        trackArtist = dictionary.get("master_metadata_album_artist_name")
        timeStamp = dictionary.get("ts")
        if timeStamp.startswith(year) and trackName and trackArtist:
            pair = (trackName, trackArtist)
            countTracksYear[pair] += 1
    sortedTracks = dict(sorted(countTracksYear.items(), key=lambda item: item[1], reverse=True))
    topTrack = next(iter(sortedTracks))
    topTrackName = topTrack[0]
    topTrackArtist = topTrack[1]
    return topTrackName, topTrackArtist

# print to test
top_track_2021 = top_track_year(data, '2021')
print(f"Florence's top track in 2021 is: {top_track_2021[0]} by {top_track_2021[1]}")
top_track_2022 = top_track_year(data, '2022')
print(f"Florence's top track in 2022 is: {top_track_2022[0]} by {top_track_2022[1]}")
top_track_2023 = top_track_year(data, '2023')
print(f"Florence's top track in 2023 is: {top_track_2023[0]} by {top_track_2023[1]}")
top_track_2024 = top_track_year(data, '2024')
print(f"Florence's top track so far in 2024 is: {top_track_2024[0]} by {top_track_2024[1]}")
print("\n")


def top_artist_year(data, year):
    """
        returns the top artist listened to based on the input year
    """
    countArtistsYear = collections.defaultdict(int)
    for dictionary in data:
        trackArtist = dictionary.get("master_metadata_album_artist_name")
        timeStamp = dictionary.get("ts")
        if timeStamp.startswith(year) and trackArtist:
            countArtistsYear[trackArtist] += 1
    sortedArtists = dict(sorted(countArtistsYear.items(), key=lambda item: item[1], reverse=True))
    topArtist = next(iter(sortedArtists))
    return topArtist

# print to test
top_artist_2021 = top_artist_year(data, '2021')
print(f"Florence's top artist in 2021 is: {top_artist_2021}")
top_artist_2022 = top_artist_year(data, '2022')
print(f"Florence's top artist in 2022 is: {top_artist_2022}")
top_artist_2023 = top_artist_year(data, '2023')
print(f"Florence's top artist in 2023 is: {top_artist_2023}")
top_artist_2024 = top_artist_year(data, '2024')
print(f"Florence's top artist so far in 2024 is: {top_artist_2024}")
print("\n")


def top_album_year(data, year):
    """
        returns the top album listened to based on the input year
    """
    countAlbumsYear = collections.defaultdict(int)
    for dictionary in data:
        albumName = dictionary.get("master_metadata_album_album_name")
        timeStamp = dictionary.get("ts")
        if timeStamp.startswith(year) and albumName:
            countAlbumsYear[albumName] += 1
    sortedAlbums = dict(sorted(countAlbumsYear.items(), key=lambda item: item[1], reverse=True))
    topAlbum = next(iter(sortedAlbums))
    return topAlbum

# print to test
top_album_2021 = top_album_year(data, '2021')
print(f"Florence's top album in 2021 is: {top_album_2021}")
top_album_2022 = top_album_year(data, '2022')
print(f"Florence's top album in 2022 is: {top_album_2022}")
top_album_2023 = top_album_year(data, '2023')
print(f"Florence's top album in 2023 is: {top_album_2023}")
top_album_2024 = top_album_year(data, '2024')
print(f"Florence's top album so far in 2024 is: {top_album_2024}")
print("\n")


# functions that return data based on time listened


def msToHours(ms):
    """
        converts milliseconds to hours, minutes, and seconds
    """
    hours = ms // 3600000
    msRemaining = ms % 3600000
    minutes = msRemaining // 60000
    msRemaining = msRemaining % 60000
    seconds = msRemaining // 1000
    return hours, minutes, seconds


def timeListenedAll():
    """
        returns the time listened to all songs
    """
    msListened = 0
    for dictionary in data:
        msListened += dictionary.get("ms_played")
    timeListened = msToHours(msListened)
    return timeListened

# print to test
timeListened = timeListenedAll()
hours = timeListened[0]
minutes = timeListened[1]
seconds = timeListened[2]
print(f"Florence has listend to Spotify for {hours} hours, {minutes} minutes, and {seconds} seconds since November 2016")


def timeListenedSong(trackName, trackArtist):
    """
        returns the time listened to a specific song
    """
    msListened = 0
    for dictionary in data:
        if dictionary.get("master_metadata_track_name") == trackName and dictionary.get("master_metadata_album_artist_name") == trackArtist:
            msListened += dictionary.get("ms_played")
    timeListened = msToHours(msListened)
    return timeListened

# print to test
trackName = "Head In The Clouds"
trackArtist = "88rising"
timeListened = timeListenedSong(trackName, trackArtist)
hours = timeListened[0]
minutes = timeListened[1]
seconds = timeListened[2]
print(f"Florence has listend to {trackName} by {trackArtist} for {hours} hours, {minutes} minutes, and {seconds} seconds") 


def timeListenedArtist(trackArtist):
    """
        returns the time listened to any artist
    """
    msListened = 0
    for dictionary in data:
        if dictionary.get("master_metadata_album_artist_name") == trackArtist:
            msListened += dictionary.get("ms_played")
    timeListened = msToHours(msListened)
    return timeListened

# print to test
trackArtist = "Steve Lacy"
timeListened = timeListenedArtist(trackArtist)
hours = timeListened[0]
minutes = timeListened[1]
seconds = timeListened[2]
print(f"Florence has listend to {trackArtist} for {hours} hours, {minutes} minutes, and {seconds} seconds") 


def topSongArtist(trackArtist):
    """
        returns the top song listened to from an artist
    """
    countTracksArtist = collections.defaultdict(int)
    for dictionary in data:
        if dictionary.get("master_metadata_album_artist_name") == trackArtist:
            trackName = dictionary.get("master_metadata_track_name")
            countTracksArtist[trackName] += 1
    sortedTracks = dict(sorted(countTracksArtist.items(), key=lambda item: item[1], reverse=True))
    topTrack = next(iter(sortedTracks))
    return topTrack

# print to test
trackArtist = "Kendrick Lamar"
topTrackFromArtist = topSongArtist(trackArtist)
timeListened = timeListenedSong(topTrackFromArtist, trackArtist)
hours = timeListened[0]
minutes = timeListened[1]
seconds = timeListened[2]
print(f"Florence's top track from {trackArtist} is: {topTrackFromArtist} and has been listened to for {hours} hours, {minutes} minutes, and {seconds} seconds") 




