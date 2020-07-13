from common import *


class TrackMatcher:

    def __init__(self, track_to_find, matched_track, status, status_details):
        self.track_to_find = track_to_find
        self.matched_track = matched_track
        self.status = status
        self.status_details = status_details


def same_hash_matcher(track_to_find, buffer):
    comp_hash = hash(track_to_find)
    matches = []
    if comp_hash in buffer:
        matches.extend(
            [TrackMatcher(track_to_find, track, 'UNCHANGED', '') for track in buffer[comp_hash]])  # maybe handle play_list rename
    return matches


def similar_artists_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_title_and_similar_artists(track_to_find):
            matches.append(TrackMatcher(track_to_find, track, 'MODIFIED', 'Artists could have been changed' if track.album == track_to_find.album else 'Artists and album could have been changed'))
    return matches


def same_id_matcher(track_to_find, buffer):
    matches = []
    for track in flatten_list(buffer.values()):
        if track.is_equal_by_id(track_to_find):
            matches.append(TrackMatcher(track_to_find, track, 'MODIFIED', 'Metadata could have been changed'))
    return matches
