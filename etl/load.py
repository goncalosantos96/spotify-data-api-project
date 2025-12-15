import pandas as pd
import os
from sqlalchemy import create_engine

def load_data_to_database(
    df_fact_playlist_track: pd.DataFrame,
    df_dim_artists: pd.DataFrame,
    df_dim_albums: pd.DataFrame,
    df_dim_tracks: pd.DataFrame,
    df_dim_playlist: pd.DataFrame
):
    # Read database credentials from environment variables
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')

    # Create SQLAlchemy engine for PostgreSQL
    engine = create_engine(f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    # Load fact table
    df_fact_playlist_track.to_sql('fact_playlist_track', con=engine, if_exists='append', index=False)

    # Load dimension tables
    df_dim_artists.to_sql('dim_artists', con=engine, if_exists='append', index=False)
    df_dim_albums.to_sql('dim_albums', con=engine, if_exists='append', index=False)
    df_dim_playlist.to_sql('dim_playlist', con=engine, if_exists='append', index=False)
    df_dim_tracks.to_sql('dim_tracks', con=engine, if_exists='append', index=False)



