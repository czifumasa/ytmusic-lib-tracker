from ytmusiclibtracker.common import *


class TrackRecord:
    LIBRARY = 'Library'
    UPLOADED = 'Uploaded'
    THUMBS_UP = 'Thumbs Up'
    YOUR_LIKES = 'Your Likes'

    def __init__(self, song_row):
        self.artists = song_row[0].strip()
        self.title = song_row[1].strip()
        self.album = song_row[2].strip()
        self.video_id = song_row[3].strip()
        self.set_video_id = song_row[4].strip()
        self.playlist_name = song_row[5].strip()
        self.playlist_id = song_row[6].strip()
        self.full_name = get_comparable_text(self.artists + ' - ' + self.title)

    def __eq__(self, other):
        if not isinstance(other, TrackRecord):
            # don't attempt to compare against unrelated types
            return NotImplemented
        if not self.is_equal_by_playlist(other):
            return False
        if self.is_equal_by_full_name(other):
            return True
        return False

    def __hash__(self):
        return hash((self.full_name, get_comparable_text(self.playlist_name)))

    def is_equal_by_id(self, other):
        if self.is_equal_by_playlist(other) and self.video_id and other.video_id:
            return self.video_id == other.video_id
        return False

    def is_equal_by_title_and_has_added_removed_artists(self, other):
        if self.is_equal_by_playlist(other) and self.is_equal_by_title(other):
            artist_list_self = set(self.artists.split(","))
            artist_list_other = set(other.artists.split(","))
            if len(artist_list_self.intersection(artist_list_other)) > 0:
                return True
        return False

    def is_similar_by_artists_and_titles(self, other):
        if self.is_equal_by_playlist(other):
            processed_artists_self = get_comparable_text(self.artists, True)
            processed_artists_other = get_comparable_text(other.artists, True)
            processed_title_self = get_comparable_text(self.title, True)
            processed_title_other = get_comparable_text(other.title, True)
            if are_two_texts_similar(processed_artists_self, processed_artists_other, 0.80) \
                    and are_two_texts_similar(processed_title_self, processed_title_other,
                                              get_similarity_index_based_on_length(processed_title_self, processed_title_other)):
                return True
            if (processed_artists_other in processed_artists_self or processed_artists_self in processed_artists_other) and \
                    (processed_title_self in processed_title_other or processed_title_other in processed_title_self):
                return True
        return False

    def is_equal_by_full_name(self, other):
        if self.full_name == other.full_name:
            return True
        return False

    def is_equal_by_title(self, other):
        if get_comparable_text(self.title) == get_comparable_text(other.title):
            return True
        return False

    def is_equal_by_playlist(self, other):
        if self.playlist_id and other.playlist_id:
            return self.playlist_id == other.playlist_id
        elif self.playlist_name and other.playlist_name:
            if self.playlist_name == other.playlist_name:
                return True
            elif self.playlist_name in [self.YOUR_LIKES, self.THUMBS_UP] and other.playlist_name in [self.YOUR_LIKES, self.THUMBS_UP]:
                return True
        return False

    def is_equal_by_album(self, other):
        if get_comparable_text(self.album) == get_comparable_text(other.album):
            return True
        return False

    def is_equal_by_liked_playlist(self, other):
        if self.is_equal_by_full_name(other) and \
                self.playlist_name in [self.YOUR_LIKES, self.THUMBS_UP] and \
                other.playlist_name in [self.YOUR_LIKES, self.THUMBS_UP]:
            return True
        return False

    def is_equal_by_uploaded_library_status(self, other):
        if self.is_equal_by_full_name(other) and \
                self.playlist_name in [self.LIBRARY, self.UPLOADED] and \
                other.playlist_name in [self.LIBRARY, self.UPLOADED]:
            return True
        return False

    def serialize_to_csv_row(self):
        return [self.artists, self.title, self.album, self.video_id, self.set_video_id,
                self.playlist_name, self.playlist_id]


