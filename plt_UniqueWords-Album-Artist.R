library(ggplot2)
library(ggbeeswarm)
library(RColorBrewer)

# Ensure there are enough palettes for artists# Define available sequential palettes
available_palettes <- c("Blues", "Greens", "Oranges", "Purples", "Reds", "YlGnBu", "BuPu")  
artist_names <- unique(lyrics_df$Artist)
palette_map <- setNames(rep(available_palettes, length.out = length(artist_names)), artist_names)  # Repeat palettes if needed

# Generate a fill color for each album using different shades per artist
fill_colors <- c()
for (artist in artist_names) {
  albums <- unique(lyrics_df$Album[lyrics_df$Artist == artist])
  
  # Ensure valid palette selection
  palette_name <- palette_map[artist]
  if (is.na(palette_name)) palette_name <- "Blues"  # Default fallback
  
  # Ensure at least 3 shades for brewer.pal()
  num_shades <- min(max(3, length(albums)), 9)  # Brewer supports up to 9 shades
  shades <- brewer.pal(num_shades, palette_name)  
  
  # Assign a different shade to each album
  album_colors <- setNames(shades[1:length(albums)], albums)
  
  # Add to global color mapping
  fill_colors <- c(fill_colors, album_colors)
}

# Apply the generated fill colors in ggplot
ggplot(lyrics_df, aes(x = Artist, y = UniqueWords, fill = Album)) +
  geom_beeswarm(size = 2, alpha = 0.8, shape = 21, stroke = 0.15, color= "black") +  # Only use fill for differentiation
  theme_minimal() +
  labs(
    title = "Unique Word Count per Song (Grouped by Artist & Album)",
    x = "Artist",
    y = "Unique Words",
    fill = "Album"
  ) +
  scale_fill_manual(values = fill_colors) +  # Apply album-specific shades
  theme(
    legend.position = "none",
    axis.text.x = element_text(angle = 45, hjust = 1)  # Rotate for readability
  )

