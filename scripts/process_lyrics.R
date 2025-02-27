library(stringr)
library(dplyr)
library(tibble)

lyrics_df <- read.csv("lyrics_data.csv")
#lyrics_df <- read.csv("lyrics_data_with_duration.csv")
#lyrics_df <- read.csv("lyrics_data_with_spotify_features.csv")

# Check if the new Spotify data is included
head(lyrics_df)

# Define the albums to process (leave empty to process all available albums)
album_titles <- c()  # Example: c("Aesop Rock - The Impossible Kid", "Jam Baxter - So We Ate Them Whole")

# Get all available album files in `lyrics_data/`
all_album_files <- list.files("lyrics_data", pattern = "\\.txt$", full.names = TRUE)

# If album_titles is empty, process all available albums
if (length(album_titles) == 0) {
  album_files_to_process <- all_album_files
} else {
  # Convert album titles to expected filenames
  album_files_to_process <- paste0("lyrics_data/", tolower(gsub(" ", "_", gsub("-", "", album_titles))), ".txt")
  
  # Keep only those that exist
  album_files_to_process <- album_files_to_process[file.exists(album_files_to_process)]
}

# Initialize an empty dataframe
lyrics_df <- tibble(Artist = character(), Album = character(), Song = character(), UniqueWords = numeric())

# Process each album file
for (album_file in album_files_to_process) {
  
  # Read full album text
  lyrics_text <- readLines(album_file, warn = FALSE)
  
  # Split into individual songs using ">" as the delimiter
  songs <- str_split(paste(lyrics_text, collapse = "\n"), "\n>")[[1]]
  
  if (length(songs) < 2) next  # Skip if no songs are found

  # Extract album title (first line, after ">")
  album_info <- str_trim(str_replace(songs[1], ">", ""))
  
  # Split into Artist and Album (assuming format "Artist - Album")
  if (grepl(" - ", album_info)) {
    artist_album <- str_split(album_info, " - ", n = 2)[[1]]
    artist_name <- str_trim(artist_album[1])
    album_title <- str_trim(artist_album[2])
  } else {
    artist_name <- "Unknown"
    album_title <- album_info
  }

  # Process each song
  for (i in 2:length(songs)) {
    song_lyrics <- str_split(songs[i], "\n", n = 2)[[1]]
    
    if (length(song_lyrics) < 2) next  # Skip if no lyrics exist

    song_title <- str_trim(song_lyrics[1])  # First line is the song title
    lyrics <- song_lyrics[2]  # Remaining text is the lyrics
    
    # Tokenize, clean text, and count unique words
    words <- tolower(unlist(str_split(lyrics, "\\s+")))
    words <- str_replace_all(words, "[[:punct:]]", "")  # Remove punctuation
    unique_word_count <- length(unique(words))
    
    # Append to dataframe
    lyrics_df <- bind_rows(lyrics_df, tibble(Artist = artist_name, Album = album_title, Song = song_title, UniqueWords = unique_word_count))
  }
} 

# Show the final dataframe
print(lyrics_df) 

