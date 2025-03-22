import json
import sys

import pyperclip

from ytmusiclibtracker.TrackRecord import TrackRecord
from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.track_matcher import *
from ytmusiclibtracker.ytm_api_wrapper import *

output_dir = None
previous_export_file = None
current_export_file = None
previous_export_type = None
current_export_type = None


def initialize_global_params_from_config_file():
    config = get_configuration_from_file('config.ini')

    global output_dir
    output_dir = config['CHANGELOG']["output_dir_changelog"]

    find_and_set_previous_and_current_file(config)


def find_and_set_previous_and_current_file(config):
    global previous_export_file, current_export_file, previous_export_type, current_export_type
    auto_detect = get_int_value_from_config(config, 'CHANGELOG', "auto_detect")
    if auto_detect > 0:
        auto_detect_dir = config['CHANGELOG']["auto_detect_dir"]

        # Look for both CSV and JSON files
        csv_files = get_list_of_csv_files_with_timestamp_from_dir(auto_detect_dir, 'exported_songs')
        json_files = get_list_of_files_with_timestamp_from_dir(auto_detect_dir, 'exported_songs', '.json')

        # Combine and sort all export files by date
        all_export_files = []
        for filename in csv_files:
            all_export_files.append({'filename': filename, 'type': 'CSV'})
        for filename in json_files:
            all_export_files.append({'filename': filename, 'type': 'JSON'})

        # Sort by date (newest first)
        if all_export_files:
            all_export_files.sort(key=lambda x: x['filename'], reverse=True)

        if len(all_export_files) == 1:
            current_export_file = os.path.join(auto_detect_dir, all_export_files[0]['filename'])
            current_export_type = all_export_files[0]['type']
        elif len(all_export_files) >= 2:
            current_export_file = os.path.join(auto_detect_dir, all_export_files[0]['filename'])
            current_export_type = all_export_files[0]['type']
            previous_export_file = os.path.join(auto_detect_dir, all_export_files[1]['filename'])
            previous_export_type = all_export_files[1]['type']
        else:
            throw_error(
                f"Error: Auto detect input files failed.\n"
                f"Could not find previous and current file in '{auto_detect_dir}' directory.\n"
                f"Verify your config.ini if 'auto_detect_dir' is set correctly.\n"
                f"If files were renamed, set 'auto_detect' to 0 and specify 'previous_file' and 'current_file' manually."
            )
    else:
        previous_export_file = config['CHANGELOG']["previous_file"] if os.path.isfile(
            config['CHANGELOG']["previous_file"]) else None
        current_export_file = config['CHANGELOG']["current_file"] if os.path.isfile(
            config['CHANGELOG']["current_file"]) else None

        # Determine file types based on extension
        if previous_export_file:
            previous_export_type = 'JSON' if previous_export_file.lower().endswith('.json') else 'CSV'
        if current_export_file:
            current_export_type = 'JSON' if current_export_file.lower().endswith('.json') else 'CSV'


def get_list_of_files_with_timestamp_from_dir(directory, filename_prefix, extension):
    """Get a list of files with specified extension and timestamp from the directory."""
    if not os.path.isdir(directory):
        return []
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
                 and f.startswith(filename_prefix) and f.endswith(extension)]
        return files
    except:
        return []


def import_track_records(filename, file_type):
    """Import track records from either CSV or JSON file"""
    if file_type == 'CSV':
        return import_track_records_from_csv_file(filename)
    else:  # JSON
        return import_track_records_from_json_file(filename)


def import_track_records_from_csv_file(filename):
    csv_rows = get_list_of_rows_from_file(filename)

    if csv_rows:
        convert_fnc = get_convert_function_by_headers(csv_rows[0])
        return [TrackRecord(convert_fnc(csv_row)) for csv_row in csv_rows[1:]]
    return []


def import_track_records_from_json_file(filename):
    """Parse the JSON file and convert the data to TrackRecord objects"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        track_records = []

        # Process library songs
        if 'library' in data:
            for song in data['library']:
                track_record = convert_song_to_track_record(song, {'id': 'Library', 'name': 'Library'})
                if track_record:
                    track_records.append(track_record)

        # Process uploaded songs
        if 'uploaded' in data:
            for song in data['uploaded']:
                track_record = convert_song_to_track_record(song, {'id': 'Uploaded', 'name': 'Uploaded'})
                if track_record:
                    track_records.append(track_record)

        # Process playlists
        if 'playlists' in data:
            for playlist_id, playlist_data in data['playlists'].items():
                playlist = {'id': playlist_id, 'name': playlist_data.get('name', '')}
                for song in playlist_data.get('songs', []):
                    track_record = convert_song_to_track_record(song, playlist)
                    if track_record:
                        track_records.append(track_record)

        return track_records
    except Exception as e:
        log(f"Error reading JSON file: {str(e)}", True)
        return []


def convert_song_to_track_record(song, playlist):
    """Convert a song from JSON format to TrackRecord object"""
    try:
        # Create a dictionary with the required fields for TrackRecord
        track_data = {
            'artists': song_artists_string_representation(song) or '',
            'title': song.get('title', '') or '',
            'album': song_album_string_representation(song.get('album', {}) or {}) or '',
            'videoId': song.get('videoId', '') or '',
            'setVideoId': set_video_id_string_representation(song) or '',
            'playlist': playlist.get('name', '') or '',
            'playlistId': playlist.get('id', '') or '',
            'availability': song_availability_status(song) or ''
        }

        return TrackRecord(list(track_data.values()))
    except Exception as e:
        log(f"Error converting song to TrackRecord: {str(e)}", False)
        return None


def export_track_matches_to_csv_file(matches):
    csv_rows = [track_match.serialize_to_csv_row() for track_match in matches]
    csv_rows = sorted(csv_rows, key=get_sort_function_for_track_matches())
    headers = ['Status', 'Details',
               'Artists', 'Matched_Artists',
               'Title', 'Matched_Title',
               'Album', 'Matched_Album',
               'Playlist', 'Matched_Playlist',
               'VideoId', 'Matched_VideoId',
               'SetVideoId', 'Matched_SetVideoId',
               'PlaylistId', 'Matched_PlaylistId']
    return create_csv_with_list_of_dict(output_dir, 'change_log', headers, csv_rows, True)


def get_sort_function_for_track_matches():
    return lambda row: (row[2] if row[2] else row[3], row[4] if row[4] else row[5], row[8] if row[8] else row[9])


def create_match_results(previous_list, current_list):
    match_results = []

    unprocessed_tracks = set(previous_list)
    current_list_buffer = group_list_by_function(current_list, lambda track: hash(track))

    for matcher in get_match_functions():
        old_list_buffer = set(unprocessed_tracks)
        unprocessed_tracks = []
        for track_to_find in old_list_buffer:
            matches = matcher(track_to_find, current_list_buffer)
            if matches:
                for match in matches:
                    match_results.append(match)
                    match_hash = hash(match.matched_track)
                    if match_hash in current_list_buffer:
                        del current_list_buffer[match_hash]
            else:
                unprocessed_tracks.append(track_to_find)

    match_results.extend(create_match_results_for_unmatched_tracks_from_previous_file(unprocessed_tracks))
    match_results.extend(
        create_match_results_for_unmatched_tracks_from_current_file(flatten_list(current_list_buffer.values())))

    return match_results


def create_duplicates_results(current_list):
    duplicates_buffer = group_list_by_function(current_list, lambda track_row: track_row.playlist_id)
    all_duplicates = []
    for playlist_tracks in duplicates_buffer.values():
        hash_buffer = group_list_by_function(
            playlist_tracks, lambda track_row: hash(get_comparable_text(track_row.full_name)))
        duplicates = [track_list[0] for (track_hash, track_list) in hash_buffer.items() if len(track_list) > 1]
        all_duplicates.extend(duplicates)
    return create_match_results_for_duplicates(all_duplicates)


def get_match_functions():
    return [same_hash_matcher,
            unavailable_playlist_songs_matcher,
            thumbs_up_your_likes_matcher,
            uploaded_to_library_matcher,
            similar_artists_matcher,
            same_id_matcher,
            similar_metadata_matcher]


def create_library_changelog():
    log('CHANGELOG')
    log('-----------------------------------------------------------------------', True)
    initialize_global_params_from_config_file()
    if current_export_file:
        previous_song_rows = []
        current_song_rows = []

        if previous_export_file:
            log('Previous export file: ')
            log(os.path.abspath(previous_export_file))
            log(f'File type: {previous_export_type}')
            previous_song_rows.extend(import_track_records(previous_export_file, previous_export_type))

        log('\nCurrent export file: ')
        log(os.path.abspath(current_export_file))
        log(f'File type: {current_export_type}')
        current_song_rows.extend(import_track_records(current_export_file, current_export_type))

        log('\nFiles loaded successfully, Creating changelog...', True)

        track_matches = create_match_results(previous_song_rows, current_song_rows)
        duplicates = create_duplicates_results(current_song_rows)

        changelog_results = track_matches + duplicates
        # setup the output directory, create it if needed
        create_dir_if_not_exist(output_dir)
        filename = export_track_matches_to_csv_file(changelog_results)
        pyperclip.copy(os.path.basename(filename))
        log('Changelog has been created. File with results has been saved in:')
        log(filename, True)
        log('Filename saved to the clipboard.')
    else:
        log('Changelog cannot be created. Previous and Current Export files not found.', True)


if __name__ == "__main__":
    create_library_changelog()
    sys.exit()
