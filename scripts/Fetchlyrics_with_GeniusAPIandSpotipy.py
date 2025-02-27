import requests
import lyricsgenius
import time
import os
import re
from bs4 import BeautifulSoup
import pandas as pd

# Genius API Access Token (Replace with your own)
GENIUS_ACCESS_TOKEN = "GENIUS_ACCESS_TOKEN"
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

# API Rate Limits
REQUESTS_PER_MINUTE = 60
MIN_REQUEST_INTERVAL = 60 / REQUESTS_PER_MINUTE  # Max. 60 requests per minute
last_request_time = 0  

# List of artists to fetch albums for
artists = [
    "Jam Baxter", "Dead Players", "Ed Scissor & Jam Baxter", "Aesop Rock",
    "Eminem", "50 Cent", "Themselves", "Dirty Dike", "Defenders of Style", "Dabbla",
    "Kendrick Lamar", "MF DOOM", "Nas", "Mos Def", "Ocean Wisdom", "Jack Danz",
    "Edward Scissortongue", "Tyler, The Creator", "Darc Mind", "Shahmen",
    "Slick Rick", "Lee Scott", "Deep Puddle Dynamics", "Coops", "Latyrx",
    "Beastie Boys", "CunninLynguists", "The Mouse Outfit", "Mac Lethal",
    "Rob Sonic", "Masta Ace", "Brother Ali", "Atmosphere", "Q-Tip",
    "Flatbush Zombies", "Del the Funky Homosapien", "Camp Lo", "Mr. Lif",
    "Poor Righteous Teachers", "Deniro Farrar", "Denzel Curry", "Kae Tempest"
]

# Store missing songs
missing_songs = []

# Function to check if a lyrics file is empty (i.e., only contains header)
def is_lyrics_file_empty(filepath):
    """Check if a lyrics file contains only the header or is truly empty."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return len(lines) <= 1  # If it has 1 or 0 lines, it's considered empty
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return True  # Treat unreadable files as empty

# Function to get all albums for an artist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

SPOTIPY_CLIENT_ID = "SPOTIPY_CLIENT_ID"
SPOTIPY_CLIENT_SECRET = "SPOTIPY_CLIENT_SECRET"

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

def get_artist_albums(artist_name, max_retries=3):
    """Fetch all albums of an artist using the Spotify API."""
    print(f"🔍 Searching albums for artist: {artist_name}")

    attempt = 0
    artist_id = None

    while attempt < max_retries:
        try:
            results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
            if results["artists"]["items"]:
                artist_id = results["artists"]["items"][0]["id"]
                break
            else:
                print(f"⚠️ No Spotify artist found for: {artist_name}")
                return []
        except spotipy.exceptions.SpotifyException as e:
            print(f"⚠️ Spotify API error: {e}. Retrying in 5s...")
            time.sleep(5)
        attempt += 1

    if not artist_id:
        print(f"❌ Could not find Spotify artist ID for {artist_name}")
        return []

    # Fetch albums using artist ID
    albums = []
    offset = 0
    while True:
        try:
            album_results = sp.artist_albums(artist_id, album_type="album", limit=50, offset=offset)
            new_albums = [album["name"] for album in album_results["items"]]

            if not new_albums:
                break

            albums.extend(new_albums)
            offset += len(new_albums)  # Paginate results

            time.sleep(1)  # Avoid API rate limits

        except spotipy.exceptions.SpotifyException as e:
            print(f"⚠️ Error fetching albums for {artist_name}: {e}")
            return []

    # Remove duplicates and print results
    albums = list(set(albums))  # Remove duplicates
    print(f"✅ Found {len(albums)} albums for {artist_name}.")
    
    return albums

# Function to get album tracklist
def get_album_tracks(artist_name, album_name):
    search_url = f"https://genius.com/albums/{artist_name.replace(' ', '-')}/{album_name.replace(' ', '-')}"
    print(f"Searching tracklist for: {artist_name} - {album_name}")
    
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Album page not found: {search_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    track_list = []

    for link in soup.find_all("a", {"class": "u-display_block"}):
        track_name = link.get_text(strip=True)
        if track_name:
            cleaned_track_name = re.sub(r'\s*Lyrics$', '', track_name)
            track_list.append(cleaned_track_name)

    print(f"Found {len(track_list)} tracks.")
    return track_list

# Function to fetch lyrics and save them properly
def fetch_lyrics(artist, album, songs):
    global last_request_time
    album_clean = f"{artist.replace(' ', '_')}_{album.replace(' ', '_')}".lower()
    album_dir = os.path.join("lyrics_data", album_clean)
    os.makedirs(album_dir, exist_ok=True)

    album_txt_path = os.path.join("lyrics_data", f"{album_clean}.txt")

    # Load existing album file to prevent overwriting
    existing_lyrics = ""
    if os.path.exists(album_txt_path):
        with open(album_txt_path, "r", encoding="utf-8") as f:
            existing_lyrics = f.read()

    with open(album_txt_path, "a", encoding="utf-8") as album_file:  # Append mode
        if is_lyrics_file_empty(album_txt_path):  # Only write header if empty
            album_file.write(f">{artist} - {album}\n\n")

        for song in songs:
            song_filename = os.path.join(album_dir, f"{song.replace(' ', '_')}.txt")

            # Skip fetching if the song file exists and is not empty
            if os.path.exists(song_filename) and not is_lyrics_file_empty(song_filename):
                print(f"✅ Already saved: {song}")
                continue

            print(f"Fetching: {song}...")

            try:
                # Respect API Rate Limits
                elapsed_time = time.time() - last_request_time
                if elapsed_time < MIN_REQUEST_INTERVAL:
                    time.sleep(MIN_REQUEST_INTERVAL - elapsed_time)

                # Fetch song lyrics
                song_data = genius.search_song(song, artist)
                last_request_time = time.time()

                if song_data:
                    lyrics = song_data.lyrics

                    # Save as separate file
                    with open(song_filename, "w", encoding="utf-8") as f:
                        f.write(lyrics)

                    # Append to album file
                    album_file.write(f">{song}\n")
                    album_file.write(lyrics + "\n\n")

                    print(f"✅ Saved: {song}")

                else:
                    print(f"⚠️ No lyrics found for: {song}")
                    missing_songs.append({"Artist": artist, "Album": album, "Song": song})

            except Exception as e:
                print(f"⚠️ Error fetching {song}: {e}")
                missing_songs.append({"Artist": artist, "Album": album, "Song": song})

# Main program: Get albums, tracklists, and fetch lyrics
for artist in artists:
    albums = get_artist_albums(artist)

    if not albums:
        print(f"Skipping {artist}, no albums found.")
        continue

    for album in albums:
        tracks = get_album_tracks(artist, album)

        if tracks:
            fetch_lyrics(artist, album, tracks)
        else:
            print(f"Skipping album {album}, no tracks found.")

# Print missing songs
if missing_songs:
    print("\n--- Missing Songs ---")
    for song_info in missing_songs:
        print(f"{song_info['Artist']} - {song_info['Album']} - {song_info['Song']}")

    # Ask user if they want to retry fetching missing lyrics from another platform
    retry = input("\nWould you like to try fetching missing lyrics from another source? (yes/no): ").strip().lower()
    
    if retry == "yes":
        print("Fetching from an alternative source is not implemented yet.")
    else:
        print("Skipping alternative sources.")
else:
    print("\nAll songs successfully fetched.")

print("All lyrics successfully saved.")
print(os.path.abspath("lyrics_data"))

#lets creatze the csv'

# Define the directory where lyrics are stored
lyrics_folder = "lyrics_data"

# Initialize an empty list to hold song data
song_data = []

# Loop through each album file
for file in os.listdir(lyrics_folder):
    if file.endswith(".txt"):
        album_path = os.path.join(lyrics_folder, file)
        
        with open(album_path, "r", encoding="utf-8") as f:
            content = f.read().split("\n>")  # Split by song marker
            artist_album = content[0].replace(">", "").strip()
            
            # Split into Artist and Album (assuming format "Artist - Album")
            if " - " in artist_album:
                artist, album = artist_album.split(" - ", 1)
            else:
                artist, album = "Unknown", artist_album
            
            # Process each song
            for song in content[1:]:
                song_lines = song.split("\n", 1)
                if len(song_lines) < 2:
                    continue
                
                song_title = song_lines[0].strip()
                lyrics = song_lines[1].strip()
                
                # Append to list
                song_data.append([artist, album, song_title, lyrics])

# Convert to DataFrame
lyrics_df = pd.DataFrame(song_data, columns=["Artist", "Album", "Song", "Lyrics"])

# Save to CSV
lyrics_df.to_csv("lyrics_data.csv", index=False, encoding="utf-8")

print("`lyrics_data.csv` created successfully.")

print(lyrics_df.head())

