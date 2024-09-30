import time
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
from oauthmanager import OnePasswordAuthManager  # Importing from oauthmanager

# Initialize Flask app
app = Flask(__name__)

app.config['Manage_Spotify_Playlists'] = 'Spotify Cookie'
app.secret_key = 'giccer-dazXi9-monkoc'

TOKEN_INFO = 'token_info'

# Initialize OnePasswordAuthManager to fetch credentials
auth_manager = OnePasswordAuthManager()

# Use oauthmanager to fetch Spotify credentials
spotify_creds = auth_manager.get_credentials("Spotify", "client_id", "client_secret", "uri")

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('get_playlists', _external=True))

@app.route('/getPlaylists')
def get_playlists():
    try:
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists()
    playlist_info = []
    
    for playlist in playlists['items']:
        playlist_info.append({
            'name': playlist['name'],
            'tracks': playlist['tracks']['total']
        })
    
    print("User's playlists:", playlist_info)
    return f"Pulled {len(playlist_info)} playlists successfully! Check the console for details."

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        return redirect(url_for('login', _external=False))

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    # Now use credentials from oauthmanager instead of reading from a file
    return SpotifyOAuth(
        client_id=spotify_creds['client_id'],
        client_secret=spotify_creds['client_secret'],
        redirect_uri=spotify_creds['uri'],  # Use 'uri' from 1Password
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
