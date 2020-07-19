import getopt

from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.ytm_api_wrapper import *

output_dir = None
export_duplicates = False

short_options = 'o:d'
long_options = ['output=', 'duplicates']

# parse script arguments
try:
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    throw_error(str(err))
    sys.exit(2)

# process given arguments
for arg, val in arguments:
    if arg in ('-d', '--duplicates'):
        export_duplicates = True
        log('Exporting list of duplicates')
    elif arg in ('-o', '--output'):
        output_dir = val
        log('Output directory is \'' + val + '\'')

if not output_dir:
    throw_error('ERROR output directory is required')

# setup the output directory, create it if needed
create_dir_if_not_exist(output_dir)

api = open_api()


def export_duplicated_songs():
    playlists = get_my_playlist_ids_and_names(api)

    export_result = []
    for playlist in playlists:
        songs = get_songs_from_playlist_grouped_by_id(api, playlist['id'])
        duplicated_songs = create_list_of_duplicated_sons(songs)
        export_result.extend(export_songs(duplicated_songs, playlist))

    headers = ['Artists', 'Title', 'FullName', 'Album', 'VideoId', 'SetVideoId', 'Playlist', 'PlaylistId']
    create_csv_with_list_of_dict(output_dir, 'duplicated_songs', headers, export_result, True)


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


if export_duplicates:
    export_duplicated_songs()
else:
    export_all_songs()

sys.exit()
