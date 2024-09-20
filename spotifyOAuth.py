import time
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from functools import wraps

class SpotifyAuthManager:
    def __init__(self, scope, use_flask_session=True):
        self.scope = scope
        self.use_flask_session = use_flask_session
        self.creds = self.load_credentials()

        # If using Flask, set up the session and app
        if self.use_flask_session:
            from flask import Flask, session
            self.app = Flask(__name__)
            self.app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
            self.app.secret_key = 'giccer-dazXi9-monkoc'  # Replace with a proper secret key
            self.session = session
            self.TOKEN_INFO = 'token_info'
            self.setup_routes()
        else:
            self.token_info_file = "spotify_token.json"

    def load_credentials(self):
        """Load credentials using 1Password or environment variables"""
        client_id = os.popen('op read "op://API Keys/Spotify/client_id"').read().strip()
        client_secret = os.popen('op read "op://API Keys/Spotify/client_secreat"').read().strip()
        redirect_uri = os.popen('op read "op://API Keys/Spotify/uri"').read().strip()

        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }

    def create_spotify_oauth(self):
        """Create Spotify OAuth instance"""
        return SpotifyOAuth(
            client_id=self.creds['client_id'],
            client_secret=self.creds['client_secret'],
            redirect_uri=self.creds['redirect_uri'],
            scope=self.scope
        )

    def get_token(self):
        """Get or refresh the token"""
        if self.use_flask_session:
            token_info = self.session.get(self.TOKEN_INFO, None)
        else:
            token_info = self.load_token_from_file()

        if not token_info:
            return None

        now = int(time.time())
        is_expired = token_info['expires_at'] - now < 60

        if is_expired:
            spotify_oauth = self.create_spotify_oauth()
            token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
            if self.use_flask_session:
                self.session[self.TOKEN_INFO] = token_info
            else:
                self.save_token_to_file(token_info)

        return token_info

    def load_token_from_file(self):
        """Load the token from a file"""
        if os.path.exists(self.token_info_file):
            with open(self.token_info_file, 'r') as f:
                return json.load(f)
        return None

    def save_token_to_file(self, token_info):
        """Save the token to a file"""
        with open(self.token_info_file, 'w') as f:
            json.dump(token_info, f)

    def login(self):
        """Redirect to the Spotify login page"""
        auth_url = self.create_spotify_oauth().get_authorize_url()
        return auth_url

    def redirect_page(self, code):
        """Handle redirect and save token"""
        token_info = self.create_spotify_oauth().get_access_token(code)
        if self.use_flask_session:
            self.session[self.TOKEN_INFO] = token_info
        else:
            self.save_token_to_file(token_info)
        return token_info

    # Custom decorator to handle authentication
    def authenticated(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token_info = self.get_token()
            if token_info:
                sp = spotipy.Spotify(auth=token_info['access_token'])
                return func(sp, *args, **kwargs)
            else:
                return "Authentication required. Please login first."
        return wrapper
