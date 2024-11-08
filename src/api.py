import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import pandas as pd
import requests
import base64

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

playlist_id = '5UkNVuZ9dCwnLFWi2rglRM'
shuffled_playlist_id = '5BgIi5pU6dA67OLT8m0U49'
charli_url = 'spotify:artist:25uiPmTg16RbhZWAqwLBy5'
my_user_id = '07kx17nd6nebncli9z3jcvhgj'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read"))

tracks = []
playlist_tracks = sp.playlist_tracks(playlist_id=playlist_id)
items = playlist_tracks['items']

while playlist_tracks['next']:
    playlist_tracks = sp.next(playlist_tracks)
    items.extend(playlist_tracks['items'])

df = pd.DataFrame(columns=('name', 'artist', 'id'))
i = 0

for item in items:
    track = item['track']
    track_name = track['name']
    track_id = track['id']
    track_artist = track['artists'][0]['name']

    df.loc[i] = list([track_name, track_artist, track_id])

    i += 1

df.to_csv(os.getcwd() + '/src/data/tracks.csv', index=False)

import random

def find(array, artist):
    i = 0
    for item in array:
        if (item[1] == artist):
            return i
        i += 1
        
    return -1

df = pd.read_csv(os.getcwd() + '/src/data/tracks.csv')

artists = df['artist'].values

artists = list(set(artists))

df_values = list(df.values)
random.shuffle(df_values)

result = []

while (len (df_values) != 0):
    artists_copy = artists.copy()
    random.shuffle(artists_copy)
    for artist in artists_copy:
        index = find(df_values, artist)
        if index != -1:
            result.append([
                df_values[index][0],
                df_values[index][1],
                df_values[index][2]
            ]
                )
            df_values.pop(index)

items = []

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-public"))
for r in result:
    track_item = ['spotify:track:' + r[2]]
    sp.playlist_add_items(playlist_id=shuffled_playlist_id, items= track_item, position=None)
    print(r)
