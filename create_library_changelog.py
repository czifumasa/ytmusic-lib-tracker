import getopt
from timeit import default_timer as timer

import TrackMatcher
from TrackRecord import TrackRecord
from csv_wrapper import *
from ytm_api_wrapper import *

output_dir = None
previous_export_file = None
current_export_file = None

short_options = 'o:p:c:'
long_options = ['output=', 'previous=', 'current=']

# parse script arguments
try:
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    throw_error(str(err))
    sys.exit(2)

# process given arguments
for arg, val in arguments:
    if arg in ('-p', '--previous'):
        previous_export_file = val
        log('Previous export result file is \'' + val + '\'')
    if arg in ('-c', '--current'):
        current_export_file = val
        log('Current export result file is \'' + val + '\'')
    elif arg in ("-o", "--output"):
        output_dir = val
        log('Output directory is \'' + val + '\'')

if not output_dir:
    throw_error('ERROR output directory is required')
if not previous_export_file:
    throw_error('ERROR previous export result file is required')
if not current_export_file:
    throw_error('ERROR current export result file is required')


def import_songs_from_csv_file(filename):
    # TODO remove library filter
    song_rows = [TrackRecord(song_row) for song_row in get_list_of_rows_from_file(filename) if
                 TrackRecord(song_row).playlist_name != 'Library']
    return song_rows


def create_changelog(previous_list, current_list):
    unchanged_songs = []  # 5216
    added_songs = []
    removed_songs = []
    removed_from_playlist = []
    not_existing_songs = []
    renamed_songs = []
    song_is_private = []
    duplicates = []
    match_results = []

    unprocessed_tracks = list(previous_list)
    current_list_buffer = group_list_by_function(current_list, lambda track: hash(track))

    for matcher in get_match_functions():
        old_list_buffer = list(unprocessed_tracks)
        unprocessed_tracks = []
        for track_to_find in old_list_buffer:
            matches = matcher(track_to_find, current_list_buffer)
            if matches:
                for match in matches:
                    match_results.append(match)
                    match_hash = hash(match.matched_track)
                    if match_hash in current_list_buffer:
                        del current_list_buffer[match_hash]
                    if len(matches) > 1:
                        duplicates.append(matches[0])
            else:
                unprocessed_tracks.append(track_to_find)

    added_songs.extend(current_list_buffer.values())

    result = []
    return result


def get_match_functions():
    return [TrackMatcher.same_hash_matcher,
            TrackMatcher.similar_artists_matcher,
            TrackMatcher.same_id_matcher]


previous_song_rows = import_songs_from_csv_file(previous_export_file)
current_song_rows = import_songs_from_csv_file(current_export_file)

start = timer()
create_changelog(previous_song_rows, current_song_rows)
end = timer()
log('Operation took: ' + str(end - start) + ' sec.')

sys.exit()
