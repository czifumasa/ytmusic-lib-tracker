from ytmusiclibtracker.common import *
from ytmusiclibtracker.MatchResult import *


def same_hash_matcher(track_to_find, buffer):
    matches = []
    comp_hash = hash(track_to_find)
    if comp_hash in buffer and track_to_find.is_available == '1':
        matches.extend(
            [MatchResult(track_to_find, track, 'UNCHANGED', '') for track in
             buffer[comp_hash]])  # maybe handle play_list rename
    return matches


def unavailable_playlist_songs_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_ignoring_availability(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'REMOVED', 'Song is greyed out and unavailable'))
    return matches


def thumbs_up_your_likes_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_liked_playlist(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'MODIFIED', '\'Thumbs Up\' playlist is now \'Your Likes\' playlist'))
    return matches


def uploaded_to_library_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_uploaded_library_status(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'UNCHANGED', ''))
    return matches


def similar_artists_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_title_and_has_added_removed_artists(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'MODIFIED', 'Artists could have been changed' if track.is_equal_by_album(track_to_find) else 'Artists and album could have been changed'))
    return matches


def same_id_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_id(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'MODIFIED', 'Track with same id has been found. Metadata could have been changed'))
    return matches


def similar_metadata_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_similar_by_artists_and_titles(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'MODIFIED', 'Similar song has been found. Verify it manually if it\'s the same track as before'))
    return matches


def create_match_results_for_unmatched_tracks_from_previous_file(unmatched_tracks):
    return [MatchResult(track, None, 'REMOVED', 'No match from current file found. Probably track has been removed recently') for track in unmatched_tracks]


def create_match_results_for_unmatched_tracks_from_current_file(unmatched_tracks):
    get_match_result = lambda track: \
        MatchResult(track, None, 'ADDED', 'No match from previous file found. Probably track has been added recently') if track.is_available == '1' else \
        MatchResult(track, None, 'REMOVED', 'Song is greyed out and unavailable')

    return [get_match_result(track) for track in unmatched_tracks]


