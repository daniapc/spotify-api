import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import requests
import base64

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

def get_token(client_id, client_secret):
    """
    Obtém um token de acesso à API do Spotify usando credenciais de cliente e verifica seu tipo de token.

    Args:
        client_id (str): Chave ID do cliente da API do Spotify.
        client_secret (str): Chave Segredo do cliente da API do Spotify.

    Returns:
        str: Código de acesso obtido da API do Spotify.
        str: Tipo de token do código de acesso (ou None se falhar ao recuperar).
        str: Tempo de disponibilidade do token em segundos.
    """
    base64_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers': {
            'Authorization': 'Basic ' + base64_auth, 
            'Content-Type' : 'application/x-www-form-urlencoded'
        },
        'data': {
            'grant_type': 'client_credentials'
        }
    }

    response = requests.post(auth_options['url'], headers=auth_options['headers'], data=auth_options['data'])

    if response.status_code == 200:
        r = response.json()
        token = r['access_token']
        token_type = r['token_type']
        token_duration = r['expires_in']
        print(f'Token de Acesso requisitado com successo!')
        print(f'Tipo do Token: {token_type}')
        print(f'Disponibilidade do Token: {token_duration} segundos')
    else:
        print('Não foi possível obter o token de acesso')
    
    return f'{token_type} {token}'

def api_call(url, access_token):
    """
    Chama a API do Spotify usando um endpoint de URL e um token de acesso para recuperar dados no formato JSON.

    Args:
        url (str): Endpoint de URL para acessar dados de faixas disponíveis.
            URL padrão fornecida - https://api.spotify.com/v1/search?q=genre:{genre}&type=track&market={market}&limit={limit}&offset={offset}
        
        access_token (str): Token de acesso à API do Spotify fornecido com o uso da função get_token.

    Returns:
        dict: Objeto JSON com a resposta da API.
    """
    response = requests.get(url, headers={'Authorization': access_token})
    api_response = response.json()
    
    return api_response

token = get_token(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

# sp.start_playback()
print(token)

response = api_call('https://api.spotify.com/v1/07kx17nd6nebncli9z3jcvhgj/player/devices', token)

print(response)

# tracks = []
# playlist_tracks = sp.playlist_tracks(playlist_id=playlist_id)
# items = playlist_tracks['items']

# df = pd.DataFrame(columns=('name', 'artist', 'id'))
# i = 0

# for item in items:
#     track = item['track']
#     track_name = track['name']
#     track_id = track['id']
#     track_artist = track['artists'][0]['name']

#     df.loc[i] = list([track_name, track_artist, track_id])

#     i += 1

# df.to_csv(os.getcwd() + '/src/data/tracks.csv', index=False)