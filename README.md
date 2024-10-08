
# spotifyAI

AI-powered tool to analyze and group Spotify songs into playlists based on mood and features.

## Overview

The **spotifyAI** project leverages Spotify's Web API and machine learning algorithms like KMeans to categorize and group songs into different "vibes" or moods. The project aims to automate the creation of playlists by analyzing audio features such as danceability, energy, valence, and tempo, among others.

### Features

- Fetch playlists and song data using Spotify Web API.
- Analyze audio features such as danceability, energy, and mood.
- Group songs using AI-driven clustering algorithms like KMeans.
- Automatically generate playlists based on mood categories.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/spotifyAI.git
   cd spotifyAI
   ```

2. **Create and activate a Conda environment**:
   ```bash
   conda create --name spotifyAI python=3.9
   conda activate spotifyAI
   ```

3. **Install required dependencies**:
   ```bash
   pip install spotipy scikit-learn
   ```

4. **Set up the environment variable for credentials**:
   Set the `CREDENTIALS_PATH` environment variable to point to the folder containing your credentials file.

   On Linux/macOS, add this to your `.bashrc` or `.zshrc`:
   ```bash
   export CREDENTIALS_PATH=/path/to/your/credentials
   ```

   On Windows (PowerShell):
   ```powershell
   $env:CREDENTIALS_PATH = "C:\path\to\your\credentials"
   ```

5. **Set up Spotify API credentials**:
   - Create a `credentials.json` file in the folder pointed to by the `CREDENTIALS_PATH` variable:
     ```json
     {
       "client_id": "YOUR_CLIENT_ID",
       "client_secret": "YOUR_CLIENT_SECRET",
       "redirect_uri": "http://localhost:8888/callback"
     }
     ```

## Usage

1. **Authenticate with Spotify**:
   Upon running the script, you will be prompted to log in and authenticate via Spotify. This grants access to your playlists and song data.

2. **Run the main script**:
   The main script fetches playlists, retrieves song data, and runs a machine learning algorithm to group the songs based on their audio features:
   ```bash
   python main.py
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your improvements.

---

Developed by [Your Name].

