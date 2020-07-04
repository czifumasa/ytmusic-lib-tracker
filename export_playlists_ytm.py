from csv_wrapper import *
from ytm_api_wrapper import *

if len(sys.argv) < 2:
    throw_error('ERROR output directory is required')

# setup the output directory, create it if needed
output_dir = sys.argv[1]
create_dir_if_not_exist(output_dir)

api = open_api()


def export_duplicated_songs():
    playlists = get_my_playlist_ids_and_names(api)

    export_result = []
    for playlist in playlists:
        songs = get_songs_from_playlist_grouped_by_id(api, playlist['id'])
        duplicated_songs = create_list_of_duplicated_sons(songs)
        export_result.extend(export_songs(duplicated_songs, playlist))

    headers = ['Artists', 'Title', 'FullName', 'VideoId', 'SetVideoId', 'Playlist', 'PlaylistId']
    create_csv_with_list_of_dict(output_dir + '/duplicated_songs.csv', headers, export_result)


export_duplicated_songs()
sys.exit()
