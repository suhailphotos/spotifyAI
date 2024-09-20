import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ee2f488d96a04a62a88936b97eb2c54f",
                                               client_secret="54a1811cdbcc4ee78824d17d18e10dfb",
                                               redirect_uri="http://100.94.188.10:5000/redirect",
                                               scope="user-library-read playlist-modify-public playlist-modify-private"))

playlists = sp.current_user_playlists()
for playlist in playlists['items']:
    print(playlist['name'])
