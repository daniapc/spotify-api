import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

playlist_id = '5UkNVuZ9dCwnLFWi2rglRM'
shuffled_playlist_id = '5BgIi5pU6dA67OLT8m0U49'
charli_url = 'spotify:artist:25uiPmTg16RbhZWAqwLBy5'
my_user_id = '07kx17nd6nebncli9z3jcvhgj'

import pandas as pd
import os
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
for i in range(int(len(artists)/3)):
    artists.append('Charli xcx')
# print(len(artists))

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

items = []
for r in result:
    items.append('spotify:track:' + r[2])
    if len(items) == 100:
        sp.playlist_remove_all_occurrences_of_items(playlist_id=shuffled_playlist_id, items= items)
        items = []
sp.playlist_remove_all_occurrences_of_items(playlist_id=shuffled_playlist_id, items= items)

items = []
for r in result:
    items.append('spotify:track:' + r[2])
    if len(items) == 100:
        sp.playlist_add_items(playlist_id=shuffled_playlist_id, items= items)
        items = []
sp.playlist_add_items(playlist_id=shuffled_playlist_id, items= items)

