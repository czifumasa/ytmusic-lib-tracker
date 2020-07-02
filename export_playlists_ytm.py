from ytm_api_wrapper import *
from csv_wrapper import *
import time

if len(sys.argv) < 2:
    log('ERROR output directory is required')
    time.sleep(3)
    exit()

# setup the output directory, create it if needed
output_dir = sys.argv[1]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

api = open_api()

playlistIds = get_my_playlist_ids(api)

songs = get_songs_from_playlist(api, playlistIds[8])

duplicated_song_ids = get_duplicated_song_ids(songs)

export_result = export_songs(songs, duplicated_song_ids)
create_csv_with_list_of_dict(sys.argv[1]+'/duplicated_songs.csv', export_result)

sys.exit()
