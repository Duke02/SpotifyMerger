import sys

import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
from time import sleep

def createPlaylistName(playlistNames):
    newPlaylistName = "Merge - "
    for name in playlistNames:
        n = str(name)
        nList = n.split(" ")
        for word in nList:
            newPlaylistName += word[0].upper()
        newPlaylistName += " "
    return newPlaylistName

def addTracksAndPlaylistNames(playlistIDs):
    playlistNames = []
    tracks = []
    playlistIDs[0] = playlistIDs[0][:-1]
    for id in playlistIDs:
        indivId = id.split(":")
        pID = indivId[4]
        userID = indivId[2]
        playlist = spotify.user_playlist(userID, playlist_id=pID)
        playlistNames.append(playlist["name"])
        initTracks = playlist["tracks"]["items"]
        for t in initTracks:
            tracks.append(t[unicode("track")]["id"])
    return {"names": playlistNames, "tracks": tracks}

def createPlaylist(spotify, playlistIDsFile, username):
    playlistNamesAndTracks = addTracksAndPlaylistNames(playlistIDsFile.readlines())
    tracks = playlistNamesAndTracks["tracks"]
    newPlaylist = spotify.user_playlist_create(username, createPlaylistName(playlistNamesAndTracks["names"]))
    while len(tracks) > 0:
        spotify.user_playlist_add_tracks(username, newPlaylist["id"], tracks[:100])
        tracks = tracks[100:]

scope = "user-library-read playlist-modify-public user-library-modify"
username = "1228112042"

clientCredits = oauth2.SpotifyClientCredentials()
token = util.prompt_for_user_token(username, scope)

if token:
    print("Authenticated!")
    spotify = spotipy.Spotify(client_credentials_manager=clientCredits, auth=token, requests_timeout=10)
else:
    print("Unable to authenticate. Exiting")
    sys.exit(0)

playlistIDsToMerge = open("playlistsToMerge.txt")
createPlaylist(spotify, playlistIDsToMerge, username)
print("We should be done now.")

