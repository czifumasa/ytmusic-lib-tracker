from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.ytm_api_wrapper import *

skip_export = False
output_dir = None
api = None


def validate_config_file():
    if not os.path.isfile('config.ini'):
        throw_error('Configuration file not found. Please make sure that \'config.ini\' is in the main directory.')


def initialize_global_params_from_config_file():
    config = get_configuration_from_file('config.ini')

    global output_dir, skip_export
    output_dir = config['EXPORT']["output_dir_export"]
    if get_int_value_from_config(config, 'EXPORT', "skip_export") > 0:
        skip_export = True


def export_all_songs():
    validate_config_file()
    global api
    api = open_api()
    export_result = []

    export_result.extend(export_songs_from_library())
    export_result.extend(export_uploaded_songs())
    export_result.extend(export_songs_from_playlists())

    return export_result


def export_songs_from_library():
    library_songs = get_all_songs_from_my_library(api)
    return export_songs(library_songs, {'id': 'Library', 'name': 'Library'})


def export_uploaded_songs():
    uploaded_songs = get_all_uploaded_songs(api)
    return export_songs(uploaded_songs, {'id': 'Uploaded', 'name': 'Uploaded'})


def export_songs_from_playlists():
    playlists = get_my_playlist_ids_and_names(api)
    export_result = []
    for playlist in playlists:
        songs = get_songs_from_playlist(api, playlist['id'])
        export_result.extend(export_songs(songs, playlist))
    return export_result


def export_to_csv():
    initialize_global_params_from_config_file()
    if not skip_export:
        # setup the output directory, create it if needed
        create_dir_if_not_exist(output_dir)

        export_result = export_all_songs()
        headers = get_ytmlt_export_headers()
        create_csv_with_list_of_dict(output_dir, 'exported_songs', headers, export_result, True)
        return export_result
    return []


if __name__ == "__main__":
    export_to_csv()
    sys.exit()
