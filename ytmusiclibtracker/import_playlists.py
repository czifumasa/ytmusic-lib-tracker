import json
import sys
from typing import List, Optional

from ytmusiclibtracker.TrackRecord import TrackRecord
from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.dto.ImportedAccountInfo import ImportedAccountInfo
from ytmusiclibtracker.dto.ImportedArtist import ImportedArtist
from ytmusiclibtracker.dto.ImportedPlaylist import ImportedPlaylist
from ytmusiclibtracker.dto.ImportedPlaylistItem import ImportedPlaylistItem
from ytmusiclibtracker.dto.ImportedRelease import ImportedRelease
from ytmusiclibtracker.dto.ImportedTrack import ImportedTrack
from ytmusiclibtracker.json_wrapper import create_json_with_raw_data
from ytmusiclibtracker.ytm_api_wrapper import search_song, open_unauthorized_api

old_csv_file_import = None
current_json_file = None
helper_json_file = None
import_time = None
unauthorized_api = None
init_helper_json_file = False
account_name = None
account_photo_url = None


def initialize_global_params_from_config_file():
    config = get_configuration_from_file('config.ini')

    global old_csv_file_import, import_time, current_json_file, init_helper_json_file, helper_json_file, account_name, \
        account_photo_url
    old_csv_file_import = config['REVERSE']["old_csv_file_import"]
    current_json_file = config['REVERSE']["current_json_file"]
    helper_json_file = config['REVERSE']["helper_json_file"]
    account_name = config['REVERSE']["account_name"]
    account_photo_url = config['REVERSE']["account_photo_url"]
    import_time_str = config.get("REVERSE", "import_time", fallback=datetime.today())
    import_time = datetime.strptime(import_time_str, "%Y-%m-%d %H:%M:%S")
    if get_int_value_from_config(config, 'REVERSE', "init_helper_json_file") > 0:
        init_helper_json_file = True


def import_track_records_from_csv_file(filename):
    csv_rows = get_list_of_rows_from_file(filename)

    if not csv_rows:
        return []

    convert_fnc = get_convert_function_by_headers(csv_rows[0])
    return [
        record
        for row in csv_rows[1:]
        if (record := TrackRecord(convert_fnc(row))).set_video_id
    ]


def load_json_file(json_filename):
    if not os.path.exists(json_filename):
        throw_error(f'File not found: {current_json_file}')

    try:
        with open(json_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            log(f'Successfully loaded data from: {json_filename}', True)
            return data
    except Exception as e:
        throw_error(f'Error loading JSON file: {str(e)}')


def get_tracks_by_video_id(library, uploaded, playlists):
    track_map = {}
    for playlist in playlists:
        # Extract tracks from the main 'tracks' list
        if 'tracks' in playlist and isinstance(playlist['tracks'], list):
            for track in playlist['tracks']:
                track_info = map_to_track_info(track)
                if track_info is not None:
                    track_map[track['videoId']] = track_info
    return track_map


def map_to_imported_track(track, track_record: Optional[TrackRecord] = None) -> ImportedTrack:
    video_id = track['videoId']
    title = track['title']
    artists = [
        map_to_imported_artist(artist)
        for artist in (track['artists'] or [])
        # Sometimes unavailable tracks are resolved with artist name as "Album Artist"
        if not (artist.get('name') == "Album Artist" and artist.get('id') is None)
    ]
    credited_name = track_record.artists if track_record and not artists else None
    return ImportedTrack(video_id, title, artists, credited_name).to_dict()


def map_to_imported_artist(artist) -> ImportedArtist:
    artist_name = artist['name'] or ''
    youtube_channel_id = artist['id']
    return ImportedArtist(artist_name, youtube_channel_id=youtube_channel_id)


def map_to_imported_release(release, is_user_uploaded: bool,
                            track_record: Optional[TrackRecord] = None) -> ImportedRelease or None:
    if release is None or release['name'] is None:
        return None

    # Sometimes unavailable tracks are resolved with album name as "Dave Rock Band Trio"
    if release['name'] == 'Dave Rock Band Trio' and track_record is not None:
        release_title = track_record.album
    else:
        release_title = release['name']

    youtube_browse_id = release['id'] or None
    return ImportedRelease(release_title, tracks=[], primary_artists=[], complete_track_list=False,
                           is_user_uploaded=is_user_uploaded, release_type='UNKNOWN',
                           youtube_browse_id=youtube_browse_id).to_dict()


def map_to_track_info(track, track_record: Optional[TrackRecord] = None):
    if 'videoId' in track:
        imported_track = map_to_imported_track(track, track_record)
        video_type = track['videoType']
        is_available = True if 'isAvailable' not in track else track['isAvailable']
        is_user_uploaded = video_type is None and is_available is True
        imported_release = map_to_imported_release(track.get('album'), is_user_uploaded, track_record)

        return {
            'track': imported_track,
            'release': imported_release,
            'isVideo': imported_release is None and is_available is True,
            'isCurrentlyAvailable': is_available,
            'hasInvalidVideoId': False,
            'failedToFetchFromApi': False,
        }
    return None


def map_uploaded_track_record_to_track_info(track_record: TrackRecord):
    imported_artists = map_track_record_artists_to_imported_artists(track_record.artists)
    imported_track = ImportedTrack(track_record.video_id, track_record.title, imported_artists).to_dict()
    imported_release = map_track_record_release_to_imported_release(track_record.album, True)
    return {
        'track': imported_track,
        'release': imported_release,
        'isVideo': False,
        'isCurrentlyAvailable': False,
        'hasInvalidVideoId': False,
        'failedToFetchFromApi': True,
    }


def map_track_with_invalid_video_id(track_record: TrackRecord):
    imported_artists = map_track_record_artists_to_imported_artists(track_record.artists)
    imported_track = ImportedTrack(track_record.video_id, track_record.title, imported_artists).to_dict()
    imported_release = map_track_record_release_to_imported_release(track_record.album, False)
    return {
        'track': imported_track,
        'release': imported_release,
        'isVideo': False,
        'isCurrentlyAvailable': False,
        'hasInvalidVideoId': True,
        'failedToFetchFromApi': True,
    }


def map_track_failed_in_search_api(track_record: TrackRecord):
    imported_artists = map_track_record_artists_to_imported_artists(track_record.artists)
    imported_track = ImportedTrack(track_record.video_id, track_record.title, imported_artists).to_dict()
    imported_release = map_track_record_release_to_imported_release(track_record.album, False)
    return {
        'track': imported_track,
        'release': imported_release,
        'isVideo': False,
        'isCurrentlyAvailable': False,
        'hasInvalidVideoId': False,
        'failedToFetchFromApi': True,
    }


def map_track_record_artists_to_imported_artists(artists: str) -> List[ImportedArtist]:
    artist_list = [{"name": artist.strip(), "id": None} for artist in artists.split(',') if artist.strip()]
    return [map_to_imported_artist(artist) for artist in artist_list]


def map_track_record_release_to_imported_release(release_name: str, is_user_uploaded: bool) -> ImportedRelease or None:
    return map_to_imported_release({"name": release_name, "id": None}, is_user_uploaded)


def merge_track_record_with_info(track_record: TrackRecord, track_info) -> ImportedTrack:
    track = ImportedTrack.from_dict(track_info['track'])
    artists: List[ImportedArtist] = merge_track_record_artists_with_info(track_record, track.primaryArtists)
    return ImportedTrack(track_record.video_id, track_record.title, artists)


def merge_track_record_with_imported_release(track_record: TrackRecord, track_info) -> ImportedRelease or None:
    if track_info["release"] is None or not track_record.album:
        return None

    release = ImportedRelease.from_dict(track_info["release"])
    return ImportedRelease(track_record.album, tracks=release.tracks, primary_artists=release.primaryArtists,
                           complete_track_list=False,
                           is_user_uploaded=release.isUserUploaded, release_type='UNKNOWN',
                           youtube_browse_id=release.youtubeBrowseId)


def merge_track_record_artists_with_info(track_record: TrackRecord, artists: List[ImportedArtist]) \
        -> List[ImportedArtist]:
    track_record_artists: List[ImportedArtist] = map_track_record_artists_to_imported_artists(track_record.artists)
    artists_with_filled_ids: List[ImportedArtist] = []
    for artist in track_record_artists:
        matched_artist = next((a for a in artists if a.fullName == artist.fullName), None)
        if matched_artist:
            enriched_artist = ImportedArtist(
                full_name=artist.fullName,
                youtube_channel_id=matched_artist.youtubeChannelId,
                code=matched_artist.code,
                localized_full_name=matched_artist.localizedFullName,
                url=matched_artist.url
            )
            artists_with_filled_ids.append(enriched_artist)
        else:
            artists_with_filled_ids.append(artist)
    return artists_with_filled_ids


def prepare_json_helper_based_on_current_library():
    current_library = load_json_file(current_json_file)
    if {'library', 'uploaded', 'playlists'}.issubset(current_library):
        library = current_library["library"] or []
        uploaded = current_library["uploaded"] or []
        playlists = current_library["playlists"] or []
        log(f'Current library has {len(library)} regular, {len(uploaded)} uploaded songs and {len(playlists)} playlists',
            True)
        tracks_by_video_id = get_tracks_by_video_id(library, uploaded, playlists)
        create_json_with_raw_data(os.path.join('input', 'import'), 'helper_json_file', tracks_by_video_id, False)


def create_timestamped_import_result(releases, playlists):
    import_results = {
        'library': [],
        'uploaded': [],
        'playlists': list(playlists),
        'releases': list(releases),
        'accountInfo': ImportedAccountInfo(account_name, account_photo_url,
                                           (import_time or datetime.now()).isoformat()).to_dict()
    }

    import_result_filename = 'import_results_' + date_time_to_file_name_string(import_time or datetime.today())
    create_json_with_raw_data(os.path.join('input', 'import'), import_result_filename, import_results, False)


def import_from_file():
    log('IMPORT FROM CSV TO MOCK YOUTUBE MUSIC RESPONSE')
    log('-----------------------------------------------------------------------', True)
    validate_config_file()
    initialize_global_params_from_config_file()
    global unauthorized_api
    unauthorized_api = open_unauthorized_api()
    log(f'Importing from {old_csv_file_import} file with {import_time} timestamp', True)
    track_records: List[TrackRecord] = []
    track_records.extend(import_track_records_from_csv_file(old_csv_file_import))
    log(f'Old file has {len(track_records)} tracks', True)
    log(f'Using {current_json_file} file as a helper to resolve data faster', True)
    if init_helper_json_file:
        prepare_json_helper_based_on_current_library()
    track_info_by_video_id = load_json_file(helper_json_file)

    playlists_to_import_by_id = {}
    releases_to_import_by_id = {}
    resolved_tracks = {}

    count_from_api = 0
    count_unresolved = 0

    uploaded_video_ids = {trackRecord.video_id for trackRecord in track_records if
                          trackRecord.playlist_id == TrackRecord.UPLOADED}

    invalid_video_ids = {trackRecord.video_id for trackRecord in track_records if
                         len(trackRecord.video_id) != 11}
    for track_record in track_records:
        if track_record.playlist_id != TrackRecord.LIBRARY and track_record.playlist_id != TrackRecord.UPLOADED:
            playlist_item = ImportedPlaylistItem(bool(int(track_record.is_available)), None, track_record.video_id,
                                                 track_record.set_video_id)
            if track_record.playlist_id not in playlists_to_import_by_id:
                playlists_to_import_by_id[track_record.playlist_id] = ImportedPlaylist(
                    track_record.playlist_id,
                    track_record.playlist_name,
                    [playlist_item],
                    None,
                    None,
                    'LL'
                ).to_dict()
            else:
                playlists_to_import_by_id[track_record.playlist_id]['items'].append(playlist_item.to_dict())

            if track_record.video_id not in resolved_tracks:
                track_info = track_info_by_video_id.get(track_record.video_id)
                if track_info is None:
                    if track_record.video_id in uploaded_video_ids:
                        track_info = map_uploaded_track_record_to_track_info(track_record)
                    elif track_record.video_id in invalid_video_ids:
                        track_info = map_track_with_invalid_video_id(track_record)
                    else:
                        search_song_result = search_song(unauthorized_api, track_record.video_id)
                        if search_song_result is not None:
                            track_info = map_to_track_info(search_song_result, track_record)
                            count_from_api += 1
                        else:
                            track_info = map_track_failed_in_search_api(track_record)
                            count_unresolved += 1
                    track_info_by_video_id[track_record.video_id] = track_info

                resolved_tracks[track_record.video_id] = track_info

                merged_track = merge_track_record_with_info(track_record, track_info)
                merged_release = merge_track_record_with_imported_release(track_record, track_info)

                if merged_release and merged_release.youtubeBrowseId:
                    release_id = merged_release.youtubeBrowseId
                    if release_id not in releases_to_import_by_id:
                        merged_release.tracks = [merged_track]
                        releases_to_import_by_id[release_id] = merged_release.to_dict()
                    else:
                        releases_to_import_by_id[release_id]["tracks"].append(merged_track.to_dict())

    log(f'Resolved tracks: {len(resolved_tracks.keys())}', True)
    log(f'Resolved tracks from api: {count_from_api}', True)
    log(f'Unresolved unavailable track_info: {count_unresolved}', True)
    log(f'Playlists: {len(playlists_to_import_by_id.keys())}', True)
    log(f'Releases: {len(releases_to_import_by_id.keys())}', True)
    create_json_with_raw_data(os.path.join('input', 'import'), 'helper_json_file', track_info_by_video_id, False)
    create_timestamped_import_result(releases_to_import_by_id.values(), playlists_to_import_by_id.values())


if __name__ == "__main__":
    import_from_file()
    sys.exit()
