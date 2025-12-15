import pandas as pd

def transform_dataframes(df_playlists_tracks: pd.DataFrame, df_artists_bands: pd.DataFrame) -> pd.DataFrame:
    # Fill missing genres with a placeholder
    df_artists_bands['genre'] = df_artists_bands['genre'].fillna('undefined')

    # Remove duplicate artist entries and reset index
    df_artists = df_artists_bands.drop_duplicates(subset=['name']).reset_index(drop=True)

    # Create surrogate key for artists
    df_artists['artist_id'] = df_artists.index + 1

    # Select relevant track columns and drop duplicates / missing values
    df_tracks = df_playlists_tracks[['id_track', 'artist', 'album_name', 'track_name', 'track_popularity', 'track_duration_ms']] \
        .drop_duplicates(subset=['artist', 'album_name', 'track_name']) \
        .dropna() \
        .reset_index(drop=True)

    # Create surrogate key for tracks
    df_tracks['track_id'] = df_tracks.index + 1

    # Select album information, remove duplicates and missing values
    df_albums = df_playlists_tracks[['id_artist', 'artist', 'album_name', 'album_release_date']] \
        .copy() \
        .drop_duplicates(subset=['artist', 'album_name']) \
        .dropna()

    # Extract album release year
    df_albums['album_release_year'] = df_albums['album_release_date'].str[0:4].astype(int)

    # Filter albums released after 1950
    df_albums = df_albums[df_albums['album_release_year'] > 1950].reset_index(drop=True)

    # Create surrogate key for albums
    df_albums['album_id'] = df_albums.index + 1

    # Create dimension table for playlists
    df_dim_playlist = df_playlists_tracks[['id_playlist', 'playlist_name']] \
        .drop_duplicates(subset=['id_playlist', 'playlist_name']) \
        .reset_index(drop=True)
    df_dim_playlist['playlist_id'] = df_dim_playlist.index + 1

    # Merge playlist info into track data
    df_merged_with_playlist = pd.merge(df_playlists_tracks, df_dim_playlist, left_on=['id_playlist', 'playlist_name'], right_on=['id_playlist', 'playlist_name'], how='inner')
    df_merged_with_playlist.drop(columns=['id_playlist', 'playlist_name'], inplace=True)

    # Merge track IDs into playlist-track data
    df_merged_playlist_tracks = pd.merge(df_merged_with_playlist, df_tracks[['artist', 'album_name', 'track_name', 'track_id']], left_on=['artist', 'album_name', 'track_name'], right_on=['artist', 'album_name', 'track_name'], how='inner')
    df_merged_playlist_tracks.drop(columns=['track_name'], inplace=True)

    # Merge album IDs
    df_merged_playlist_tracks_albums = pd.merge(df_merged_playlist_tracks, df_albums[['artist', 'album_name', 'album_id']], left_on=['artist', 'album_name'], right_on=['artist', 'album_name'], how='inner')

    # Merge artist IDs to build fact table
    df_fact_playlist_track = pd.merge(df_merged_playlist_tracks_albums, df_artists[['name', 'artist_id']], left_on='artist', right_on='name', how='inner')

    # Calculate track duration in minutes
    df_fact_playlist_track['track_duration_min'] = (df_fact_playlist_track['track_duration_ms'] / 60000).round(2)

    # Drop unnecessary columns to leave only fact table measures / foreign keys
    df_fact_playlist_track.drop(columns=['id_track', 'id_artist', 'artist', 'album_name', 'album_release_date', 'name', 'track_duration_ms'], inplace=True)

    # Prepare dimension tables by dropping unnecessary columns and renaming where needed
    df_dim_artists = df_artists.drop(columns=['id']).rename(columns={'name': 'artist'})
    df_dim_albums = df_albums.drop(columns=['id_artist', 'artist', 'album_release_date'])
    df_dim_tracks = df_tracks.drop(columns=['id_track', 'artist', 'album_name', 'track_popularity', 'track_duration_ms'])
    df_dim_playlist.drop(columns=['id_playlist'], inplace=True)

    return df_fact_playlist_track, df_dim_artists, df_dim_albums, df_dim_tracks, df_dim_playlist