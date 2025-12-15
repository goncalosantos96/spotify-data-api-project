from authorization import get_auth_request
from requests import requests
import pandas as pd
import time


def get_request_endpoint(url: str, headers: dict):
    # Perform GET request to Spotify endpoint
    response = requests.get(url, headers=headers)

    # Handle rate limiting (Too Many Requests)
    if response.status_code == 429:
        # Spotify tells how many seconds to wait
        retry_after = response.headers.get("Retry-After")
        print(f'Request limit reached. Waiting {retry_after} seconds.')
        time.sleep(int(retry_after))
        response = requests.get(url, headers=headers)

    # Handle expired or invalid token
    if response.status_code in (400, 401):
        headers = get_auth_request()
        response = requests.get(url, headers=headers)

    return response


def get_playlist_tracks(items_playlist: dict, rows_playlist: list[dict], headers: dict) -> None:
    # Iterate over playlists returned by Spotify search
    for playlist in items_playlist:
        if playlist is None:
            continue

        # URL to retrieve tracks of the playlist
        tracks_href = playlist.get('tracks', {}).get('href')
        if not tracks_href:
            continue

        try:
            # Request playlist tracks endpoint
            response_playlist = get_request_endpoint(tracks_href, headers)
            records_playlist = response_playlist.json()

            # Extract track items
            items_playlist_tracks = records_playlist.get('items', [])

        except requests.exceptions.RequestException:
            print("HTTP error while fetching playlist tracks")
            continue
        except ValueError:
            print("Invalid JSON returned by Spotify")
            continue

        # Iterate over tracks inside the playlist
        for playlist_tracks in items_playlist_tracks:
            if playlist_tracks['track'] is None:
                continue

            # Normalize playlist-track data into a dictionary
            playlist_track_info = {
                'id_playlist': playlist['id'],
                'playlist_name': playlist['name'],
                'id_track': playlist_tracks['track']['id'],
                'track_name': playlist_tracks['track']['name'],
                'track_popularity': playlist_tracks['track']['popularity'],
                'track_duration_ms': playlist_tracks['track']['duration_ms'],
                'id_artist': playlist_tracks['track']['artists'][0]['id'],
                'artist': playlist_tracks['track']['artists'][0]['name'],
                'album_name': playlist_tracks['track']['album']['name'],
                'album_release_date': playlist_tracks['track']['album']['release_date']
            }

            # Append extracted row to shared list
            rows_playlist.append(playlist_track_info)


def extract_sub_genres(artists_sample: list[str], headers: dict) -> list[str]:
    # Store all genres found for the input artists
    sub_genres = []

    LIMIT = 20  # Spotify search limit per request

    for artist in artists_sample:
        # Search artist by name
        url_band = f'https://api.spotify.com/v1/search?q={artist}&type=artist&limit={LIMIT}'

        try:
            response = get_request_endpoint(url_band, headers)
            records = response.json()

            # Navigate safely through JSON structure
            items = records.get('artists', {}).get('items', [])
        except Exception:
            continue

        # Take first artist result if exists
        artist = items[0] if items else None

        # Extend genres list
        if artist:
            sub_genres.extend(artist['genres'])

    # Remove duplicates before returning
    return list(set(sub_genres))


def extract_playlists_tracks(sub_genres: list[str], headers: dict) -> pd.DataFrame:
    # Accumulate all playlist-track rows
    rows_playlist = []

    for genre in sub_genres:
        # Search playlists by genre
        url_playlist = f'https://api.spotify.com/v1/search?q={genre}&type=playlist&limit=50'

        try:
            response = get_request_endpoint(url_playlist, headers)
            records = response.json()

            items_playlist = records.get('playlists', {}).get('items', [])
            next_url = records.get('playlists', {}).get('next')
        except Exception:
            continue

        # Extract tracks from first page
        get_playlist_tracks(items_playlist, rows_playlist, headers)

        # Handle pagination
        while next_url:
            response = get_request_endpoint(next_url, headers)
            records = response.json()
            items_playlist = records.get('playlists', {}).get('items', [])
            next_url = records.get('playlists', {}).get('next')

            get_playlist_tracks(items_playlist, rows_playlist, headers)

    # Convert list of dictionaries into DataFrame
    return pd.DataFrame(rows_playlist)


def extract_artists_bands(artists_ids: pd.Series, headers: dict) -> pd.DataFrame:
    rows_artists_bands = []
    LIMIT = 20  # Spotify allows max 20 artist IDs per request

    for i in range(0, len(artists_ids), LIMIT):
        # Build comma-separated artist IDs string
        string_ids = ','.join(artists_ids[i:i + LIMIT].tolist())
        url = f'https://api.spotify.com/v1/artists?ids={string_ids}'

        try:
            response = get_request_endpoint(url, headers)
            records = response.json()
            artists = records.get('artists', [])
        except Exception:
            continue

        for artist in artists:
            if artist is None:
                continue

            # Normalize artist information
            rows_artists_bands.append({
                'id': artist['id'],
                'name': artist['name'],
                'genre': artist['genres'][0] if artist['genres'] else None,
                'popularity': artist['popularity'],
                'followers': artist['followers']['total']
            })

    return pd.DataFrame(rows_artists_bands)


def extract_data_from_api(artists_sample: list[str], headers: dict):
    # Step 1: extract sub-genres from artists
    sub_genres = extract_sub_genres(artists_sample, headers)

    # Step 2: extract playlists and tracks
    df_playlists_tracks = extract_playlists_tracks(sub_genres, headers)

    # Step 3: extract unique artist IDs from tracks
    artists_ids = (
        df_playlists_tracks['id_artist']
        .drop_duplicates()
        .dropna()
        .reset_index(drop=True)
    )

    # Step 4: extract artist metadata
    df_artists_bands = extract_artists_bands(artists_ids, headers)

    return df_playlists_tracks, df_artists_bands
