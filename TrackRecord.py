class TrackRecord:
    LIBRARY = 'Library'

    def __init__(self, song_row):
        self.artists = song_row[0]
        self.title = song_row[1]
        self.full_name = song_row[2]
        self.album = song_row[3]
        self.video_id = song_row[4]
        self.set_video_id = song_row[5]
        self.playlist_name = song_row[6]
        self.playlist_id = song_row[7]
        self.status = None
        self.status_details = None

    def get_artists_list(self):
        return self.artists.split(',')

    def __eq__(self, other):
        if not isinstance(other, TrackRecord):
            # don't attempt to compare against unrelated types
            return NotImplemented
        if not self._is_equal_by_playlist(other):
            return False
        if self.full_name == other.full_name:
            return True
        return False

    def __hash__(self):
        return hash((self.full_name, self.playlist_name))

    def _is_equal_by_playlist(self, other):
        if self.playlist_id and other.playlist_id:
            return self.playlist_id == other.playlist_id
        elif self.playlist_name and other.playlist_name:
            return self.playlist_name == other.playlist_name
        return False

    def is_equal_by_id(self, other):
        if self._is_equal_by_playlist(other) and self.video_id and other.video_id:
            return self.video_id == other.video_id
        return False

    def is_equal_by_title_and_similar_artists(self, other):
        if self._is_equal_by_playlist(other) and self._is_equal_by_title(other):
            artist_list_self = set(self.artists.split(","))
            artist_list_other = set(other.artists.split(","))
            if len(artist_list_self.intersection(artist_list_other)) > 0:
                return True
        return False

    def _is_equal_by_title(self, other):
        if self.title == other.title:
            return True
        return False

    def _is_equal_by_album(self, other):
        if self.album == other.album:
            return True
        return False
