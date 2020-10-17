class MatchResult:

    def __init__(self, track_to_find, matched_track, status, status_details):
        self.track_to_find = track_to_find
        self.matched_track = matched_track
        self.status = status
        self.status_details = status_details

    def serialize_to_csv_row(self):
        csv_row = [
            self.status,
            self.status_details,
            self.track_to_find.artists if self.track_to_find else '',
            self.matched_track.artists if self.matched_track else '',
            self.track_to_find.title if self.track_to_find else '',
            self.matched_track.title if self.matched_track else '',
            self.track_to_find.album if self.track_to_find else '',
            self.matched_track.album if self.matched_track else '',
            self.track_to_find.playlist_name if self.track_to_find else '',
            self.matched_track.playlist_name if self.matched_track else '',
            self.track_to_find.video_id if self.track_to_find else '',
            self.matched_track.video_id if self.matched_track else '',
            self.track_to_find.set_video_id if self.track_to_find else '',
            self.matched_track.set_video_id if self.matched_track else '',
            self.track_to_find.playlist_id if self.track_to_find else '',
            self.matched_track.playlist_id if self.matched_track else '',
        ]

        return csv_row
