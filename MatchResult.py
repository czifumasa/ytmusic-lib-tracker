class MatchResult:

    def __init__(self, track_to_find, matched_track, status, status_details):
        self.track_to_find = track_to_find
        self.matched_track = matched_track
        self.status = status
        self.status_details = status_details

    def serialize_to_csv_row(self):
        csv_row = [self.status, self.status_details]
        if self.track_to_find:
            csv_row.extend(self.track_to_find.serialize_to_csv_row())
        if self.matched_track:
            csv_row.extend(self.matched_track.serialize_to_csv_row())

        return csv_row
