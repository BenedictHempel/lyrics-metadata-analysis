# lyrics-metadata-analysis
## Lyrics Data Analysis: Unique Words, Duration & Spotify Features
Analyzing lyrical complexity, song duration, and Spotify metadata across multiple hip-hop artists using Genius &amp; Spotify APIs as well as web scraping.

📌 Project Type: Data Analysis, Natural Language Processing (NLP), Data Visualization  
📌 Tech Stack: Python, R, Pandas, Spotipy, Genius API, ggplot2  
📌 Skills Demonstrated: API Data Extraction, Data Cleaning, Feature Engineering, Data Visualization, Statistical Analysis  

## 📖 Overview  
This project explores the lyrical complexity of various hip-hop artists by analyzing:

    Unique word count per song & artist
    Song duration fetched from Spotify API
    Spotify features (danceability, energy, popularity)
    Explicit lyrics vs. energy levels
    Lyrical complexity vs. song popularity

By leveraging Genius API for lyrics and Spotify API for song metadata, we generate insights into how artists differ in word diversity, song structure, and musical composition.

## 🛠️ Project Structure

Each script is modularized for better reproducibility:

📂 lyrics-analysis/  
│── 📂 data/ (Stores raw & processed data)  
│── 📂 notebooks/ (Jupyter & R Markdown Notebooks)  
│── 📂 scripts/ (Python & R scripts). 
│      ├── fetch_lyrics.py (Extract lyrics using Genius API)  
│      ├── fetch_song_metadata.py (Get song duration & features from Spotify API)  #coming soon
│      ├── process_lyrics.R (Clean text & calculate unique word count)  
│      ├── generate_visualizations.R (Create plots using ggplot2). 
│── 📂 results/ (Visualizations & insights)  
│── 📂 docs/ (Documentation, methods, and reports)  
│── .gitignore (Excludes API keys & unnecessary files)  
│── README.md (Project description & instructions)  
│── requirements.txt (Dependencies for Python)  
│── environment.yml (Conda environment for reproducibility)  

## 📊 Data Pipeline

✅ Step 1: Fetch Lyrics & Store in TXT Files
🔹 fetch_lyrics.py scrapes lyrics from Genius API & saves them in lyrics_data/.

✅ Step 2: Extract Song Metadata # coming soon
🔹 fetch_song_metadata.py fetches duration, popularity, energy, and danceability from Spotify API.

✅ Step 3: Process Lyrics for Unique Word Count
🔹 process_lyrics.R cleans text & counts unique words per song & artist.

✅ Step 4: Generate Insights & Plots
🔹 generate_visualizations.R analyzes word diversity, song duration, and Spotify features.  

## 📊 Example Visualizations

✅ Unique Words vs. Song Duration (Does longer duration mean more complex lyrics?) 
✅ Lyrical Complexity vs. Song Popularity (Do highly streamed songs have richer vocabularies?)  
✅ Explicit Lyrics vs. Energy Level (Are explicit songs more energetic?)  
✅ Artist Comparison: (Who has the widest vocabulary in hip-hop?)  

    📌 All plots are available in the results/ folder.


