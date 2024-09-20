import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAuthManager:
    def __init__(self, scope):
        self.scope = scope

    def fetch_credentials(self):
        """Fetch credentials from 1Password."""
        try:
            client_id = subprocess.getoutput('op read "op://API Keys/Spotify/client_id"')
            client_secret = subprocess.getoutput('op read "op://API Keys/Spotify/client_secreat"')
            redirect_uri = subprocess.getoutput('op read "op://API Keys/Spotify/uri"')
            print(f"Client ID: {client_id}, Client Secret: {client_secret}, Redirect URI: {redirect_uri}")  # Debug output
            return client_id, client_secret, redirect_uri
        except Exception as e:
            print(f"Error fetching credentials from 1Password: {e}")
            return None, None, None

    def create_spotify_oauth(self):
        """Create Spotify OAuth instance."""
        client_id, client_secret, redirect_uri = self.fetch_credentials()

        if not client_id or not client_secret or not redirect_uri:
            print("Missing credentials. Exiting.")
            return None

        print("Creating SpotifyOAuth instance...")  # Debug output
        return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=self.scope
        )

    def get_token(self):
        """Retrieve the token, authenticate if needed."""
        spotify_oauth = self.create_spotify_oauth()

        if not spotify_oauth:
            print("SpotifyOAuth creation failed.")
            return None

        print("Fetching cached token...")  # Debug output
        token_info = spotify_oauth.get_cached_token()

        if not token_info:
            print("No cached token found. Starting authentication...")  # Debug output
            auth_url = spotify_oauth.get_authorize_url()
            print(f"Please go to this URL to authenticate: {auth_url}")
            code = input("Enter the code from the URL after authentication: ")
            token_info = spotify_oauth.get_access_token(code)
            print(f"Token retrieved: {token_info}")  # Debug output

        return token_info

def pull_playlists(sp):
    print("Pulling playlists...")  # Debug statement
    try:
        playlists = sp.current_user_playlists()
        
        if not playlists['items']:
            print("No playlists found.")
            return
        
        for playlist in playlists['items']:
            print(f"Playlist: {playlist['name']}, Total Tracks: {playlist['tracks']['total']}")
    
    except Exception as e:
        print(f"Error while fetching playlists: {e}")

if __name__ == '__main__':
    print("Starting playlist pull script...")

    # Initialize the auth manager
    spotify_auth_manager = SpotifyAuthManager('user-library-read playlist-modify-public playlist-modify-private')

    # Try to retrieve the token
    token_info = spotify_auth_manager.get_token()

    if token_info:
        # Create Spotipy instance and fetch playlists
        sp = spotipy.Spotify(auth=token_info['access_token'])
        pull_playlists(sp)
    else:
        print("Authentication failed. Please authenticate via the provided URL.")

    print("Script finished.")
