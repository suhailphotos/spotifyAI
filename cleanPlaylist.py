import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Get the credentials path from the environment variable
credentials_path = os.getenv('CREDENTIALS_PATH')

if credentials_path is None:
    raise EnvironmentError("The environment variable 'CREDENTIALS_PATH' is not set.")

# Load credentials from the spotifyOAuth.json file
with open(os.path.join(credentials_path, 'spotifyOAuth.json'), 'r') as file:
    creds = json.load(file)

# Path for token cache file (can be customized if needed)
token_cache_path = os.path.join(credentials_path, 'spotify_token_cache')

# Set up authentication with token caching
sp_oauth = SpotifyOAuth(
    client_id=creds['client_id'],
    client_secret=creds['client_secret'],
    redirect_uri=creds['redirect_uri'],
    scope="playlist-read-private",
    cache_path=token_cache_path
)

# Get the token either from cache or by prompting for authorization
token_info = sp_oauth.get_access_token(as_dict=False)

# Authenticate with the access token
sp = spotipy.Spotify(auth=token_info)

# Fetch and print all playlists from the authenticated user's account
def fetch_user_playlists(sp):
    playlists = sp.current_user_playlists()
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(f"{i + 1}. {playlist['name']} - {playlist['id']}")
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

if __name__ == '__main__':
    fetch_user_playlists(sp)
