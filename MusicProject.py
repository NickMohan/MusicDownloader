from __future__ import unicode_literals
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from YoutubeSearch import youtube_search
import argparse
import youtube_dl
import config


def download(idList, x):

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'outtmpl': filePath+'%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v='+idList[x][0]])


trackList = []
idList = []
#User inputs for album and artists
album = input("Album: ")
#token authorization
client_credentials_manager = SpotifyClientCredentials(
        client_id=config.Spotify.CLIENT_ID,
        client_secret=config.Spotify.CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Album search to get the tracks on the albums
results = sp.search(q = "album:" + album, type = "album")
album_id = results['albums']['items'][0]['uri']
tracks = sp.album_tracks(album_id)
for x in tracks['items']:
    trackList.append(x['name'])

#Search the album dictionary for the artist uri
artistURI = results['albums']['items'][0]['artists'][0]['uri']
artist = results['albums']['items'][0]['artists'][0]['name']

#Get youtube ids for each song

for x in range(0,len(trackList)):
    search = (artist+" "+album+" "+trackList[x])
    #Searches for the videos and returns video id
    if __name__ == "__main__":
      parser = argparse.ArgumentParser()
      parser.add_argument("--q", help="Search term", default=search)
      parser.add_argument("--max-results", help="Max results", default=1)
      args = parser.parse_args()
    try:
        idList.append(youtube_search(args))
    except requests.HTTPError as e:
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

#Take Youtube ids and download the mp3s for each song
filePath = config.SAVE_LOCATION % (artist, album)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'outtmpl': filePath+'%(title)s.%(ext)s',
}

print("Downloading Youtube music...")
print("%s / %s complete" %
      (str(0).ljust(3), str(len(idList)).ljust(3)), end='\r')

for x in range(0,len(idList)):
    try:
        download(idList,x)
#        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#            ydl.download(['https://www.youtube.com/watch?v='+idList[x][0]])
    except:
        idList.append([idList[x][0]])
    print("%s / %s complete" %
          (str(x).ljust(3), str(len(idList)).ljust(3)), end='\r')

print("\nDone downloading.")

#Used to edit the metadata of the mp3s for name artist and album
#Do something here
