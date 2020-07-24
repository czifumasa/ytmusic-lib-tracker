from timeit import default_timer as timer

from ytmusiclibtracker.TrackRecord import TrackRecord
from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.track_matcher import *

output_dir = None
previous_export_file = None
current_export_file = None


def initialize_global_params_from_config_file():
    config = get_configuration_from_file('config.ini')

    global output_dir, previous_export_file, current_export_file
    output_dir = config['OUTPUT']["output_dir"]
    previous_export_file = config['INPUT']["previous_file"]
    current_export_file = config['INPUT']["current_file"]


def import_track_records_from_csv_file(filename):
    # TODO remove library filter
    track_records = [TrackRecord(csv_row) for csv_row in get_list_of_rows_from_file(filename) if
                     TrackRecord(csv_row).playlist_name != 'Library']
    return track_records


def export_track_matches_to_csv_file(matches):
    csv_rows = [track_match.serialize_to_csv_row() for track_match in matches]
    headers = ['Status', 'Details', 'Old_Artists', 'Old_Title', 'Old_FullName', 'Old_Album', 'Old_VideoId',
               'Old_SetVideoId', 'Old_Playlist', 'Old_PlaylistId', 'New_Artists', 'New_Title', 'New_FullName',
               'New_Album', 'New_VideoId', 'New_SetVideoId', 'New_Playlist', 'New_PlaylistId']
    create_csv_with_list_of_dict(output_dir, 'change_log', headers, csv_rows, True)


def create_match_results(previous_list, current_list):
    unchanged_songs = []
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

    match_results.extend(create_match_results_for_unmatched_tracks_from_previous_file(unprocessed_tracks))
    match_results.extend(
        create_match_results_for_unmatched_tracks_from_current_file(flatten_list(current_list_buffer.values())))

    return match_results


def get_match_functions():
    return [same_hash_matcher,
            thumbs_up_your_likes_matcher,
            similar_artists_matcher,
            same_id_matcher,
            similar_titles_matcher]


def create_library_changelog():
    initialize_global_params_from_config_file()
    # setup the output directory, create it if needed
    create_dir_if_not_exist(output_dir)

    previous_song_rows = import_track_records_from_csv_file(previous_export_file)
    current_song_rows = import_track_records_from_csv_file(current_export_file)

    start = timer()
    track_matches = create_match_results(previous_song_rows, current_song_rows)
    export_track_matches_to_csv_file(track_matches)
    end = timer()
    log('Creating changelog took: ' + str(end - start) + ' sec.')

    sys.exit()


if __name__ == "__main__":
    create_library_changelog()
