import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from functools import wraps
from flask import Flask, request, url_for, session, redirect

class SpotifyAuthManager:
    def __init__(self, app, scope='user-library-read playlist-modify-public playlist-modify-private'):
        self.app = app
        self.scope = scope
        self.token_info_key = 'token_info'
        self.authenticated_user = None
        self.auth_url = None
        self.spotify_creds = None

    def get_credentials(self):
        """
        Method to fetch credentials using oauthmanager. 
        This is just an abstraction for fetching credentials.
        """
        from oauthmanager import OnePasswordAuthManager
        auth_manager = OnePasswordAuthManager()
        self.spotify_creds = auth_manager.get_credentials("Spotify", "client_id", "client_secret", "uri")

    def create_spotify_oauth(self):
        return SpotifyOAuth(
            client_id=self.spotify_creds['client_id'],
            client_secret=self.spotify_creds['client_secret'],
            redirect_uri=self.spotify_creds['uri'],
            scope=self.scope
        )

    def get_token(self):
        """Retrieve the token from the session."""
        token_info = session.get(self.token_info_key, None)
        if not token_info:
            return None

        now = int(time.time())
        is_expired = token_info['expires_at'] - now < 60
        if is_expired:
            spotify_oauth = self.create_spotify_oauth()
            token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
            session[self.token_info_key] = token_info

        return token_info

    def login(self):
        """Route for logging in."""
        self.get_credentials()  # Get the credentials from oauthmanager
        spotify_oauth = self.create_spotify_oauth()
        self.auth_url = spotify_oauth.get_authorize_url()
        return redirect(self.auth_url)

    def redirect_page(self):
        """Handle the redirect after Spotify OAuth."""
        session.clear()
        code = request.args.get('code')
        spotify_oauth = self.create_spotify_oauth()
        token_info = spotify_oauth.get_access_token(code)
        session[self.token_info_key] = token_info
        self.authenticated_user = True
        return redirect(url_for('get_playlists'))

    def authenticated(self, func):
        """
        Decorator to ensure the user is authenticated before calling Spotify functions.
        If not authenticated, it will redirect to the Spotify login URL.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            token_info = self.get_token()
            if not token_info:
                print("User not logged in. Redirecting to login.")
                return self.login()

            sp = spotipy.Spotify(auth=token_info['access_token'])
            return func(sp, *args, **kwargs)

        return wrapper

    def run(self):
        """Start the Flask app."""
        self.app.run(host='0.0.0.0', port=5000, debug=True)
