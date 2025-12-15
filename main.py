from dotenv import load_dotenv
from etl.extract import extract_data_from_api
from etl.transform import transform_dataframes
from etl.load import load_data_to_database
from authorization import get_auth_request


# Sample list of metal and rock bands used as seed input
metal_rock_bands = [
    "The Rolling Stones", "Led Zeppelin", "AC/DC", "Radiohead", "Arctic Monkeys", "Pink Floyd",
    "The Strokes", "The Black Keys", "Yes", "Explosions in the Sky", "Lynyrd Skynyrd", "T. Rex",
    "Crosby, Stills & Nash", "The Ramones", "Coldplay", "Iron Maiden", "Metallica", "Slayer",
    "Megadeth", "Black Sabbath", "Candlemass", "Electric Wizard", "Pantera", "Korn", "Slipknot",
    "Mayhem", "Dimmu Borgir", "Behemoth", "Cannibal Corpse", "In Flames", "Helloween", "Nightwish",
    "Dream Theater", "Eluveitie", "Amon Amarth", "Paradise Lost", "As I Lay Dying", "Suicide Silence", 
    "Ministry", "Candlemass", "Electric Wizard", "Pantera", "Korn", "Slipknot", "Mayhem", "Dimmu Borgir",
    "Behemoth", "Cannibal Corpse", "In Flames", "Helloween", "Nightwish", "Dream Theater", "Eluveitie",
    "Amon Amarth", "Paradise Lost", "As I Lay Dying", "Suicide Silence", "Ministry"
]

# Set of unique values of artists/bands
artists_sample= set(metal_rock_bands)


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get Spotify authorization headers
    headers = get_auth_request()

    # Run extraction phase
    df_tracks, df_artists = extract_data_from_api(artists_sample, headers)

    # Run transformation phase
    df_fact, df_dim_artists, df_dim_albums, df_dim_tracks, df_dim_playlist = \
        transform_dataframes(df_tracks, df_artists)

    # Load data into PostgreSQL
    load_data_to_database(
        df_fact,
        df_dim_artists,
        df_dim_albums,
        df_dim_tracks,
        df_dim_playlist
    )
   

if __name__ == "__main__":
    main()