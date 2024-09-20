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

# Set up authentication manually (disable automatic server-based flow)
sp_oauth = SpotifyOAuth(
    client_id=creds['client_id'],
    client_secret=creds['client_secret'],
    redirect_uri=creds['redirect_uri'],
    scope="playlist-read-private",
    open_browser=False  # Disable auto browser opening
)

# Get the authorization URL and print it to manually open it in a browser
auth_url = sp_oauth.get_authorize_url()
print(f"Please navigate here to authorize: {auth_url}")

# Prompt for the redirect URL after authorization
response = input("Paste the URL you were redirected to: ")

# Parse the authorization code from the URL
code = sp_oauth.parse_response_code(response)

# Exchange the code for an access token
token_info = sp_oauth.get_access_token(code)

# Authenticate with the access token
sp = spotipy.Spotify(auth=token_info['access_token'])

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
