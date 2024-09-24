from oauthmanager import AuthManager, OnePasswordAuthManager

# Initialize the Auth Manager
auth_manager = OnePasswordAuthManager()

# Retrieve credentials for Spotify
spotify_creds = auth_manager.get_credentials("Spotify", "client_id", "client_secret", "uri")

# Use the credentials
print(f"Client ID: {spotify_creds['client_id']}")
print(f"Client Secret: {spotify_creds['client_secret']}")
print(f"Redirect URI: {spotify_creds['uri']}")
