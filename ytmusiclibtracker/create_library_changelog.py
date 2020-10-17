from timeit import default_timer as timer

from ytmusiclibtracker.TrackRecord import TrackRecord
from ytmusiclibtracker.csv_wrapper import *
from ytmusiclibtracker.track_matcher import *

output_dir = None
previous_export_file = None
current_export_file = None


def initialize_global_params_from_config_file():
    config = get_configuration_from_file('config.ini')

    global output_dir
    output_dir = config['CHANGELOG']["output_dir_changelog"]

    find_and_set_previous_and_current_file(config)


def find_and_set_previous_and_current_file(config):
    global previous_export_file, current_export_file
    auto_detect = get_int_value_from_config(config, 'CHANGELOG', "auto_detect")
    if auto_detect > 0:
        auto_detect_dir = config['CHANGELOG']["auto_detect_dir"]
        list_of_filenames = get_list_of_csv_files_with_timestamp_from_dir(auto_detect_dir, 'exported_songs')
        if len(list_of_filenames) >= 2:
            list_of_filenames.sort(reverse=True)
            current_export_file = auto_detect_dir+'\\'+list_of_filenames[0]
            previous_export_file = auto_detect_dir+'\\'+list_of_filenames[1]
        else:
            throw_error(
                'Error: Auto detect input files failed.' 
                '\nCould not find previous and current file in \'' + auto_detect_dir +'\' directory.'
                '\nVerify your config.ini file if \'auto_detect_dir\' is set correctly.'
                '\nThis could also happen if you renamed files. In that case, please change \'auto_detect\' to 0,'
                '\nthen set \'previous_file\' and \'current_file\' manually.')
    else:
        previous_export_file = config['CHANGELOG']["previous_file"]
        current_export_file = config['CHANGELOG']["current_file"]


def import_track_records_from_csv_file(filename):

    csv_rows = get_list_of_rows_from_file(filename)

    if csv_rows:
        convert_fnc = get_convert_function_by_headers(csv_rows[0])
        return [TrackRecord(convert_fnc(csv_row)) for csv_row in csv_rows[1:]]
    return []


def export_track_matches_to_csv_file(matches):
    csv_rows = [track_match.serialize_to_csv_row() for track_match in matches]
    csv_rows = sorted(csv_rows, key=get_sort_function_for_track_matches())
    headers = ['Status', 'Details',
               'Old_Artists', 'New_Artists',
               'Old_Title', 'New_Title',
               'Old_Album', 'New_Album',
               'Old_Playlist', 'New_Playlist',
               'Old_VideoId', 'New_VideoId',
               'Old_SetVideoId', 'New_SetVideoId',
               'Old_PlaylistId', 'New_PlaylistId']
    create_csv_with_list_of_dict(output_dir, 'change_log', headers, csv_rows, True)


def get_sort_function_for_track_matches():
    return lambda row: (row[2] if row[2] else row[3], row[4] if row[4] else row[5], row[8] if row[8] else row[9])


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
