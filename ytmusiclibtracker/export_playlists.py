import sys

from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.json_wrapper import create_json_with_row_data
from ytmusiclibtracker.ytm_api_wrapper import *

skip_export = False
output_dir = None
output_type = "CSV"  # Default to CSV
api = None


def validate_config_file():
    if not os.path.isfile('config.ini'):
        throw_error('Configuration file not found. Please make sure that \'config.ini\' is in the main directory.')


def initialize_global_params_from_config_file():
    config = get_configuration_from_file('config.ini')

    global output_dir, skip_export, output_type
    output_dir = config['EXPORT']["output_dir_export"]
    if get_int_value_from_config(config, 'EXPORT', "skip_export") > 0:
        skip_export = True

    # Get output type from config (default to CSV if not specified)
    if "output_type" in config['EXPORT']:
        output_type = config['EXPORT']["output_type"].upper()
        if output_type not in ["CSV", "JSON"]:
            log(f"Invalid output_type '{output_type}' in config. Using CSV as default.", True)
            output_type = "CSV"


def export_all_songs():
    global api
    api = open_api()

    # For CSV export - processed data
    export_result = []

    # For JSON export - raw data
    raw_data = {
        'library': [],
        'uploaded': [],
        'playlists': []
    }

    # Collect data for both export types
    library_songs = get_all_songs_from_my_library(api)
    uploaded_songs = get_all_uploaded_songs(api)
    playlist_ids = get_my_playlist_ids(api)

    # Process for CSV export
    export_result.extend(export_songs(library_songs, {'id': 'Library', 'title': 'Library'}))
    export_result.extend(export_songs(uploaded_songs, {'id': 'Uploaded', 'title': 'Uploaded'}))

    # Store raw data for JSON export
    raw_data['library'] = library_songs
    raw_data['uploaded'] = uploaded_songs

    # Process playlists
    for playlist_id in playlist_ids:
        playlist = get_playlist_by_id(api, playlist_id)
        tracks = playlist.get('tracks', [])
        # For CSV
        export_result.extend(export_songs(tracks, playlist))
        # For JSON
        raw_data['playlists'].append({
            'id': playlist['id'],
            'title': playlist['title'],
            'tracks': tracks,
            'description': playlist['description'],
            'privacy': playlist['privacy'],
            'owned': playlist['owned']
        })

    return export_result, raw_data


def export_to_file():
    log('EXPORT FROM YOUTUBE MUSIC')
    log('-----------------------------------------------------------------------', True)
    validate_config_file()
    initialize_global_params_from_config_file()

    if not skip_export:
        export_result, raw_data = export_all_songs()
        # setup the output directory, create it if needed
        create_dir_if_not_exist(output_dir)

        if output_type == "CSV":
            headers = get_ytmlt_export_headers()
            filename = create_csv_with_list_of_dict(output_dir, 'exported_songs', headers, export_result, True)
            log('Export has been completed. CSV file with results has been saved in:')
            log(filename, True)
            return export_result
        else:  # JSON export
            filename = create_json_with_row_data(output_dir, 'exported_songs', raw_data, True)
            log('Export has been completed. JSON file with results has been saved in:')
            log(filename, True)
            return raw_data

    log('Export has been skipped. If you want to export again, open config.ini file and edit option: skip_export=0',
        True)
    return []


if __name__ == "__main__":
    export_to_file()
    sys.exit()
