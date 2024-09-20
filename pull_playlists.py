from spotifyOAuth import SpotifyAuthManager

# Initialize the auth manager with the required scope
spotify_auth_manager = SpotifyAuthManager('user-library-read playlist-modify-public playlist-modify-private', use_flask_session=False)

def debug_token():
    """Debugging function to check if we are retrieving a token."""
    token_info = spotify_auth_manager.get_token()
    if token_info:
        print("Token retrieved successfully:", token_info)
    else:
        print("Failed to retrieve token.")
    return token_info

def pull_playlists(sp):
    print("Pulling playlists...")  # Debug statement
    try:
        playlists = sp.current_user_playlists()
        
        # Check if any playlists are returned
        if not playlists['items']:
            print("No playlists found.")
            return
        
        for playlist in playlists['items']:
            print(f"Playlist: {playlist['name']}, Total Tracks: {playlist['tracks']['total']}")
    
    except Exception as e:
        print(f"Error while fetching playlists: {e}")  # Catch and display any errors

if __name__ == '__main__':
    print("Starting playlist pull script...")  # Debug statement
    
    # Debugging: Check if token retrieval works
    token_info = debug_token()
    
    if token_info:
        # Now try pulling playlists only if token retrieval is successful
        sp = spotify_auth_manager.create_spotify_oauth()
        pull_playlists(sp)
    
    print("Script finished.")  # Debug statement
