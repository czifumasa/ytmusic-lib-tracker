from common import *
from MatchResult import MatchResult


def same_hash_matcher(track_to_find, buffer):
    comp_hash = hash(track_to_find)
    matches = []
    if comp_hash in buffer:
        matches.extend(
            [MatchResult(track_to_find, track, 'UNCHANGED', '') for track in
             buffer[comp_hash]])  # maybe handle play_list rename
    return matches


def thumbs_up_your_likes_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_title(track_to_find) and track.is_equal_by_artists(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'UNCHANGED', 'Thumbs Up playlist is now Your Likes playlist'))
    return matches


def similar_artists_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_title_and_has_added_removed_artists(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'MODIFIED', 'Artists could have been changed' if track.album == track_to_find.album else 'Artists and album could have been changed'))
    return matches


def same_id_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_id(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'MODIFIED', 'Metadata could have been changed'))
    return matches


def similar_titles_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_similar_by_artists_and_titles(track_to_find):
            matches.append(MatchResult(track_to_find, track, 'MODIFIED', 'Similar song has been found. Verify it manually, it could be different version.'))
    return matches


def create_match_results_for_unmatched_tracks_from_current_file(unmatched_tracks):
    return [MatchResult(None, track, 'ADDED', 'No match from previous file found. Probably track has been added to playlist recently') for track in unmatched_tracks]


