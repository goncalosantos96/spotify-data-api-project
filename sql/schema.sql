--  ALL THIS QUERIES ARE TO CREATE TABLES AT A POSTGRESQL DATABASE

create table if not exists fact_playlist_track 
(
	playlist_id INTEGER,
	artist_id INTEGER,
	album_id INTEGER,
	track_id INTEGER,
	track_popularity INTEGER,
	track_duration_min real,
	primary key(playlist_id, track_id)

);


create table if not exists dim_artists
(

	artist_id INTEGER,
	artist TEXT,
	genre TEXT,
	popularity INTEGER,
	followers INTEGER,
	primary key(artist_id)

);


create table if not exists dim_albums
(

	album_id INTEGER,
	album_name TEXT,
	album_release_year INTEGER,
	primary key(album_id)

);


create table if not exists dim_tracks
(

	track_id INTEGER,
	track_name TEXT,
	primary key(track_id)

);


create table if not exists dim_playlist
(

	playlist_id INTEGER,
	playlist_name TEXT,
	primary key(playlist_id)

);