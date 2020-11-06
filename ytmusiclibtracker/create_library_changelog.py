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
        if len(list_of_filenames) == 1:
            current_export_file = auto_detect_dir + '\\' + list_of_filenames[0]
        elif len(list_of_filenames) >= 2:
            list_of_filenames.sort(reverse=True)
            current_export_file = auto_detect_dir + '\\' + list_of_filenames[0]
            previous_export_file = auto_detect_dir + '\\' + list_of_filenames[1]
        else:
            throw_error(
                'Error: Auto detect input files failed.'
                '\nCould not find previous and current file in \'' + auto_detect_dir + '\' directory.'
                '\nVerify your config.ini file if \'auto_detect_dir\' is set correctly.'
                '\nThis could also happen if you renamed files. In that case, please change \'auto_detect\' to 0,'
                '\nthen set \'previous_file\' and \'current_file\' manually.')
    else:
        previous_export_file = config['CHANGELOG']["previous_file"] if os.path.isfile(
            config['CHANGELOG']["previous_file"]) else None
        current_export_file = config['CHANGELOG']["current_file"] if os.path.isfile(
            config['CHANGELOG']["current_file"]) else None


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
               'Artists', 'Matched_Artists',
               'Title', 'Matched_Title',
               'Album', 'Matched_Album',
               'Playlist', 'Matched_Playlist',
               'VideoId', 'Matched_VideoId',
               'SetVideoId', 'Matched_SetVideoId',
               'PlaylistId', 'Matched_PlaylistId']
    return create_csv_with_list_of_dict(output_dir, 'change_log', headers, csv_rows, True)



def get_sort_function_for_track_matches():
    return lambda row: (row[2] if row[2] else row[3], row[4] if row[4] else row[5], row[8] if row[8] else row[9])


def create_match_results(previous_list, current_list):
    song_is_private = []
    match_results = []

    unprocessed_tracks = set(previous_list)
    current_list_buffer = group_list_by_function(current_list, lambda track: hash(track))

    for matcher in get_match_functions():
        old_list_buffer = set(unprocessed_tracks)
        unprocessed_tracks = []
        for track_to_find in old_list_buffer:
            matches = matcher(track_to_find, current_list_buffer)
            if matches:
                for match in matches:
                    match_results.append(match)
                    match_hash = hash(match.matched_track)
                    if match_hash in current_list_buffer:
                        del current_list_buffer[match_hash]
            else:
                unprocessed_tracks.append(track_to_find)

    match_results.extend(create_match_results_for_unmatched_tracks_from_previous_file(unprocessed_tracks))
    match_results.extend(
        create_match_results_for_unmatched_tracks_from_current_file(flatten_list(current_list_buffer.values())))

    return match_results


def create_duplicates_results(current_list):
    duplicates_buffer = group_list_by_function(current_list, lambda track_row: track_row.playlist_id)
    all_duplicates = []
    for playlist_tracks in duplicates_buffer.values():
        hash_buffer = group_list_by_function(
            playlist_tracks, lambda track_row: hash(get_comparable_text(track_row.full_name)))
        duplicates = [track_list[0] for (track_hash, track_list) in hash_buffer.items() if len(track_list) > 1]
        all_duplicates.extend(duplicates)
    return create_match_results_for_duplicates(all_duplicates)


def get_match_functions():
    return [same_hash_matcher,
            unavailable_playlist_songs_matcher,
            thumbs_up_your_likes_matcher,
            uploaded_to_library_matcher,
            similar_artists_matcher,
            same_id_matcher,
            similar_metadata_matcher]


def create_library_changelog():
    log('CHANGELOG')
    log('-----------------------------------------------------------------------', True)
    initialize_global_params_from_config_file()
    if previous_export_file and current_export_file:

        log('Previous export file: ')
        log(os.path.abspath(previous_export_file), True)
        previous_song_rows = import_track_records_from_csv_file(previous_export_file)
        log('Current export file: ')
        log(os.path.abspath(current_export_file), True)
        log('Creating changelog...', True)
        current_song_rows = import_track_records_from_csv_file(current_export_file)

        track_matches = create_match_results(previous_song_rows, current_song_rows)
        duplicates = create_duplicates_results(current_song_rows)

        changelog_results = track_matches + duplicates
        # setup the output directory, create it if needed
        create_dir_if_not_exist(output_dir)
        filename = export_track_matches_to_csv_file(changelog_results)
        log('Changelog has been created. File with results has been saved in:')
        log(filename, True)
    elif (not previous_export_file) and current_export_file:
        log('Changelog skipped. Only one export file exists.', True)
    else:
        log('Changelog cannot be created. Previous and Current Export files not found.', True)


if __name__ == "__main__":
    create_library_changelog()
    sys.exit()
