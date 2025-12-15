--  ALL  THIS QUERIES PRESENTED ARE PERFORMED AT POSTGRESQL (IDE DBeaver)


-- The artist most frequently featured in all playlists
select da.artist, count(distinct playlist_id) as num_playlist_present
from fact_playlist_track f
join dim_artists da
on f.artist_id = da.artist_id
group by da.artist
order by num_playlist_present desc
limit 1


-- The artist with most songs on all playlists
select da.artist, count(track_id) as num_all_tracks
from fact_playlist_track f
join dim_artists da
on f.artist_id = da.artist_id
group by da.artist
order by num_all_tracks desc
limit 1


-- Top 10 most featured tracks on all playlists
select da.artist,
	   dt.track_name,
	   count(track_name) as num_track_on_playlist
from fact_playlist_track f
join dim_artists da
on f.artist_id = da.artist_id
join dim_tracks dt
on f.track_id = dt.track_id
group by da.artist, dt.track_name
order by num_track_on_playlist desc
limit 10


-- Longest playlist 

select dp.playlist_id, dp.playlist_name, sum(f.track_duration_min) as total_minutes
from fact_playlist_track f
join dim_playlist dp 
on f.playlist_id = dp.playlist_id
group by dp.playlist_id, dp.playlist_name
order by total_minutes desc
limit 1


-- The most represented album in all playlists

select da.artist, dal.album_name, count(1) total_tracks_album
from fact_playlist_track f
join dim_albums dal
on f.album_id = dal.album_id
join dim_artists da 
on f.artist_id = da.artist_id
group by da.artist, dal.album_name
order by total_tracks_album desc
limit 1