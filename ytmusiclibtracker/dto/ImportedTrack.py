from typing import List, Optional

from ytmusiclibtracker.dto.ImportedArtist import ImportedArtist


class ImportedTrack:
    def __init__(
            self,
            youtube_track_id: str,
            title: str,
            primary_artists: List[ImportedArtist],
            credited_name: Optional[str] = None,
            track_number: Optional[int] = None,
            order_number: Optional[int] = None
    ):
        self.youtubeTrackId = youtube_track_id
        self.title = title
        self.creditedName = credited_name
        self.trackNumber = track_number
        self.primaryArtists = primary_artists
        self.orderNumber = order_number

    def to_dict(self):
        return {
            "youtubeTrackId": self.youtubeTrackId,
            "title": self.title,
            "creditedName": self.creditedName,
            "trackNumber": self.trackNumber,
            "primaryArtists": [artist.to_dict() for artist in self.primaryArtists],  # Convert artist objects
            "orderNumber": self.orderNumber,
        }
