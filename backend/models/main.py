import pandas as pd
import numpy as np
import json
from backend.models.step1_genre_selection import process_genre_selection, filter_data_by_genre
from backend.models.step2_style_selection import process_style_selection, intersection_of_results
from backend.models.step3_music_recomendation import (
    categorize_places_by_time,
    get_music_scores,
    set_top_music,
    add_song_details,
    reorder_place_keys,
)


def main_pipeline(input_data, music_hashtags_data, csv_paths, music_embeddings, user_preferences_embeddings):
    """
    Updated to accept a single input_data dictionary.
    """
    genre_selection = input_data.get("musicGenres", [])
    genre_openess = input_data.get("genreOpenness", 0)
    style_selection = input_data.get("musicTags", [])
    style_openess = input_data.get("tagOpenness", 0)
    trip_data = input_data.get("recommendations", [])

    # Step 1: Genre Selection
    final_genre_selection = process_genre_selection(genre_selection, genre_openess)
    genre_filtered_data = filter_data_by_genre(final_genre_selection, music_hashtags_data)

    # Step 2: Style Selection
    style_filtered_data = process_style_selection(style_selection, style_openess, music_hashtags_data, music_embeddings,
                                                  user_preferences_embeddings)
    intersection_data = intersection_of_results(style_filtered_data, genre_filtered_data)

    # Step 3: Music Recommendation Considering Trip Schedule
    categorized_trip_data = categorize_places_by_time(trip_data)
    trip_data_with_music_scores = get_music_scores(categorized_trip_data, csv_paths)
    trip_data_with_top_music = set_top_music(trip_data_with_music_scores, intersection_data)
    trip_data_with_song_details = add_song_details(trip_data_with_top_music, music_hashtags_data)
    trip_data_with_ordered_keys = reorder_place_keys(trip_data_with_song_details)

    return trip_data_with_ordered_keys