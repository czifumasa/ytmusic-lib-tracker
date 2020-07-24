from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.ytm_api_wrapper import *

output_dir = None
api = None


def initialize_global_params_from_config_file():
    config = get_configuration_from_file('config.ini')

    global output_dir
    output_dir = config['OUTPUT']["output_dir"]


def export_duplicated_songs():
    playlists = get_my_playlist_ids_and_names(api)

    export_result = []
    for playlist in playlists:
        songs = get_songs_from_playlist_grouped_by_id(api, playlist['id'])
        duplicated_songs = create_list_of_duplicated_sons(songs)
        export_result.extend(export_songs(duplicated_songs, playlist))

    headers = ['Artists', 'Title', 'FullName', 'Album', 'VideoId', 'SetVideoId', 'Playlist', 'PlaylistId']
    create_csv_with_list_of_dict(output_dir, 'duplicated_songs', headers, export_result, True)


def list_duplicates():
    initialize_global_params_from_config_file()

    # setup the output directory, create it if needed
    create_dir_if_not_exist(output_dir)
    global api
    api = open_api()
    export_duplicated_songs()
    sys.exit()


if __name__ == "__main__":
    list_duplicates()
