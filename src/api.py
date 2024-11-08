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
charli_url = 'spotify:artist:25uiPmTg16RbhZWAqwLBy5'
my_user_id = '07kx17nd6nebncli9z3jcvhgj'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read"))

tracks = []
playlist_tracks = sp.playlist_tracks(playlist_id=playlist_id)
items = playlist_tracks['items']

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