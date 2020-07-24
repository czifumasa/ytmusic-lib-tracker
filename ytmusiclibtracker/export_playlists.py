from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.ytm_api_wrapper import *

output_dir = None
api = None


def initialize_global_params_from_config_file():
    config = get_configuration_from_file('config.ini')

    global output_dir
    output_dir = config['OUTPUT']["output_dir"]


def export_all_songs():
    export_result = []
    export_result.extend(export_songs_from_library())
    export_result.extend(export_songs_from_playlists())

    headers = ['Artists', 'Title', 'FullName', 'Album', 'VideoId', 'SetVideoId', 'Playlist', 'PlaylistId']
    create_csv_with_list_of_dict(output_dir, 'exported_songs', headers, export_result, True)


def export_songs_from_library():
    library_songs = get_all_songs_from_my_library(api)
    return export_songs(library_songs, {'id': 'Library', 'name': 'Library'})


def export_songs_from_playlists():
    playlists = get_my_playlist_ids_and_names(api)
    export_result = []
    for playlist in playlists:
        songs = get_songs_from_playlist(api, playlist['id'])
        export_result.extend(export_songs(songs, playlist))
    return export_result


def export_to_csv():
    initialize_global_params_from_config_file()

    # setup the output directory, create it if needed
    create_dir_if_not_exist(output_dir)
    global api
    api = open_api()
    export_all_songs()
    sys.exit()


if __name__ == "__main__":
    export_to_csv()
