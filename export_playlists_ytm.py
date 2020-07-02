from ytm_api_wrapper import *
from csv_wrapper import *

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

songs = list_duplicated_songs_in_playlist(api, playlistIds[3])

list_of_song_rows = []
for song in songs:
    song_row = [song]
    list_of_song_rows.append(song_row)

create_csv_with_list_of_dict(sys.argv[1]+'/duplicated_songs.csv', list_of_song_rows)
sys.exit()
