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


def get_songs_from_playlist_by_id(songs_list):
    songs_by_id = {}

    for track in songs_list:
        songs_by_id[track['videoId']] = track

    return songs_by_id


def list_duplicated_songs_in_playlist(api, playlist_id):

    playlist = api.get_playlist(playlist_id, 5000)
    songs = playlist['tracks']

    log('Duplicated items in playlist: ' + playlist['title'])

    video_ids = []
    for song in songs:
        video_ids.append(song['videoId'])

    duplicated_ids = list_duplicates(video_ids)

    songs_by_ids = get_songs_from_playlist_by_id(songs)

    duplicated_song_strings = []
    for dupe in duplicated_ids:
        duplicated_song_strings.append(song_string_representation(songs_by_ids[dupe]))

    return duplicated_song_strings


def song_string_representation(song):

    artists = song['artists']
    title = song['title']

    return artists[0]['name'] + ' - ' + title

































