import ytmusicapi

from ytmusiclibtracker.common import *


def open_api():
    log('Logging into YouTube Music...', True)
    api = setup_api()
    log('Login Successful.', True)
    return api


def setup_api():
    if not os.path.isfile('headers_auth.json'):
        headers_raw = []
        log('Please paste here the request headers from your browser and then press \'Enter\' twice to continue:')
        buffer = ''
        while True:
            line = input()
            # If line ends with ':' then it's copied Chromium Headers. They need some parsing before headers_raw can
            # be sent to ytmusicapi. Debug here if setup fails with missing headers error.
            if len(line) > 0 and line[-1] == ':':
                buffer = line + ' '
            else:
                headers_raw.append(buffer + line + '\n')
            if not line:
                break
        ytmusicapi.setup(filepath='headers_auth.json', headers_raw=''.join(headers_raw))
    try:
        return ytmusicapi.YTMusic('headers_auth.json')
    except Exception as error:
        log('There was a problem with login to Youtube Music.', True)
        if "Could not detect credential type" in (str(error)):
            log('Please setup your login request headers again.', False)
            os.remove('headers_auth.json')
            return setup_api()
        else:
            raise error


def get_all_songs_from_my_library(api):
    log('Fetching tracks from library, it may take a while...')
    library_songs = api.get_library_songs(100000, True)

    log('Fetched ' + str(len(library_songs)) + ' tracks from Library', True)
    return library_songs


def get_my_playlist_ids(api):
    my_playlists = api.get_library_playlists(1000)
    playlist_ids = []
    for playlist in my_playlists:
        playlist_ids.append(playlist['playlistId'])
    return playlist_ids


def get_playlist_by_id(api, playlist_id):
    playlist = api.get_playlist(playlist_id, 5000)

    log('Fetching tracks from \'' + playlist['title'] + '\' playlist...')
    tracks = playlist.get('tracks', [])
    if playlist['trackCount'] != len(tracks):
        log('Invalid Response: ' + str(len(tracks)) + '/' + str(playlist['trackCount']) + ', retrying...')
        playlist = api.get_playlist(playlist_id, 5000)

    log('Fetched ' + str(len(tracks)) + ' tracks from \'' + playlist['title'] + '\' playlist', True)
    return playlist


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
                    playlist['title'],
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
