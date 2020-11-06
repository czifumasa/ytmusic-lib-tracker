import platform

from ytmusicapi import YTMusic

from ytmusiclibtracker.common import *


def open_api():
    log('Logging into YouTube Music...', True)
    if not os.path.isfile('headers_auth.json'):
        headers_raw = []
        log('Please paste here the request headers from your browser and then press \'Enter\' twice to continue:')
        while True:
            line = input()
            if line:
                headers_raw.append(line+'\n')
            else:
                break
        YTMusic.setup(filepath='headers_auth.json', headers_raw=''.join(headers_raw))
    api = YTMusic('headers_auth.json')
    log('Login Successful.', True)
    return api


def get_all_songs_from_my_library(api):
    log('Fetching tracks from library, it may take a while...')
    library_songs = api.get_library_songs(100000, True)

    log('Fetched ' + str(len(library_songs)) + ' tracks from Library', True)
    return library_songs


# returns [{id: playlistId, name: playlistName},...]
def get_my_playlist_ids_and_names(api):
    my_playlists = api.get_library_playlists(1000)
    playlist_ids = []
    for playlist in my_playlists:
        playlist_ids.append({'id': playlist['playlistId'], 'name': playlist['title']})
    return playlist_ids


def get_songs_from_playlist(api, playlist_id):
    playlist = api.get_playlist(playlist_id, 5000)

    log('Fetching tracks from \'' + playlist['title'] + '\' playlist...')
    if playlist['trackCount'] != len(playlist['tracks']):
        log('Invalid Response: ' + str(len(playlist['tracks'])) + '/' + str(playlist['trackCount']) + ', retrying...')
        playlist = api.get_playlist(playlist_id, 5000)

    log('Fetched ' + str(len(playlist['tracks'])) + ' tracks from \'' + playlist['title'] + '\' playlist', True)
    return playlist['tracks']


def get_all_uploaded_songs(api):
    log('Fetching uploaded tracks, it may take a while...')
    uploaded_songs = api.get_library_upload_songs(100000)
    log('Fetched ' + str(len(uploaded_songs)) + ' uploaded tracks', True)

    return uploaded_songs


def export_songs(songs, playlist):
    export_result = []
    for song in songs:
        song_row = [song_artists_string_representation(song),
                    song['title'],
                    song_album_string_representation(song['album']),
                    song['videoId'],
                    set_video_id_string_representation(song),
                    playlist['name'],
                    playlist['id'],
                    song_availability_status(song)]
        export_result.append(song_row)
    return export_result


def song_string_representation(song):
    artists = song_artists_string_representation(song)
    title = song['title']

    if artists:
        return artists + ' - ' + title
    return ' - ' + title


def song_artists_string_representation(song):
    if 'artists' in song and song['artists']:
        artists = song['artists']
    elif 'artist' in song and song['artist']:
        artists = song['artist']
    else:
        return None

    artists_names = [artist['name'] for artist in artists]
    return ','.join(artists_names)


def song_album_string_representation(album):
    if album:
        if "name" in album:
            return album["name"]
    return None


def set_video_id_string_representation(song):
    return song['setVideoId'] if 'setVideoId' in song else None


def song_availability_status(song):
    if 'isAvailable' in song:
        if not song['isAvailable']:
            return 0
    return '1'


def create_temporary_id_for_songs_without_one(playlist, counter):
    return 'missingId_from_' + playlist['id'] + '_' + str(counter)
