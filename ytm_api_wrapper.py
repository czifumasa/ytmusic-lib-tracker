from ytmusicapi import YTMusic
from common import *
import json


def open_api():
    log('Logging into YouTube Music...')
    api = YTMusic('headers_auth.json')
    log('Login Successful.')
    return api


def get_my_playlist_ids(api):
    my_playlists = api.get_library_playlists()
    playlist_ids = []
    for playlist in my_playlists:
        # TODO create constants
        playlist_ids.append(playlist['playlistId'])
    return playlist_ids


def get_songs_from_playlist(api, playlist_id):
    playlist = api.get_playlist(playlist_id, 5000)

    log('\nFetched ' + str(len(playlist['tracks'])) + ' tracks from \'' + playlist['title'] + '\' playlist')
    return playlist['tracks']


def group_songs_by_id(songs_list):
    songs_by_id = {}

    for track in songs_list:
        songs_by_id[track['videoId']] = track

    return songs_by_id


def get_duplicated_song_ids(songs):
    video_ids = []
    for song in songs:
        video_ids.append(song['videoId'])

    duplicated_track_ids = get_duplicated_items_from_list(video_ids)
    log('Found ' + str(len(duplicated_track_ids)) + ' duplicated tracks')
    return duplicated_track_ids


# if ids_to_export is empty then export everything
def export_songs(songs, ids_to_export=None):
    grouped_songs = group_songs_by_id(songs)
    if ids_to_export:
        grouped_songs = {song_id: song for (song_id, song) in grouped_songs.items() if song_id in ids_to_export}

    export_result = []
    for (song_id, song) in grouped_songs.items():
        song_row = [song_artists_string_representation(song['artists']), song['title'], (song_string_representation(song)), song_id]
        export_result.append(song_row)
    return export_result


def song_string_representation(song):
    artists = song_artists_string_representation(song['artists'])
    title = song['title']

    return artists + ' - ' + title


def song_artists_string_representation(artists):

    artists_names = [artist['name'] for artist in artists]
    return ','.join(artists_names)
































