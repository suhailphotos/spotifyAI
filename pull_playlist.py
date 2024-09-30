# flask_app.py
from flask import Flask
from spotifyOAuth import SpotifyAuthManager

# Initialize Flask app
app = Flask(__name__)

app.config['Manage_Spotify_Playlists'] = 'Spotify Cookie'
app.secret_key = 'giccer-dazXi9-monkoc'

# Initialize SpotifyAuthManager
spotify_auth_manager = SpotifyAuthManager(app)

@app.route('/')
def login():
    """Trigger the login process."""
    return spotify_auth_manager.login()

@app.route('/redirect')
def redirect_page():
    """Handle the OAuth redirect."""
    return spotify_auth_manager.redirect_page()

@spotify_auth_manager.authenticated
def pull_playlists(sp):
    """Example of pulling playlists once authenticated."""
    playlists = sp.current_user_playlists()
    playlist_info = []
    for playlist in playlists['items']:
        playlist_info.append({
            'name': playlist['name'],
            'tracks': playlist['tracks']['total']
        })

    print("User's Playlists:", playlist_info)
    return f"Pulled {len(playlist_info)} playlists successfully!"


@app.route('/getPlaylists')
def get_playlists():
    """Wrapper for calling pull_playlists."""
    return pull_playlists()

if __name__ == '__main__':
    # Run the Flask app
    spotify_auth_manager.run()
