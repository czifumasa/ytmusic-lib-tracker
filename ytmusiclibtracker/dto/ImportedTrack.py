from typing import List, Optional

from ytmusiclibtracker.dto.ImportedArtist import ImportedArtist


class ImportedTrack:
    def __init__(
            self,
            youtube_track_id: Optional[str],
            title: str,
            primary_artists: List[ImportedArtist],
            is_available: Optional[bool] = True,
            credited_name: Optional[str] = None,
            track_number: Optional[str] = None,
            order_number: Optional[int] = None
    ):
        if title is None or title.strip() == "":
            raise ValueError("title must not be null or blank")

        if youtube_track_id is not None and youtube_track_id.strip() == "":
            raise ValueError("youtube_track_id must not be blank")

        self.youtubeTrackId = youtube_track_id
        self.title = title
        self.creditedName = credited_name
        self.trackNumber = track_number
        self.primaryArtists = primary_artists or []
        self.orderNumber = order_number
        self.isAvailable = is_available

    @classmethod
    def from_dict(cls, data: dict) -> "ImportedTrack":
        return cls(
            youtube_track_id=data['youtubeTrackId'],
            title=data['title'],
            is_available=data['isAvailable'],
            credited_name=data.get('creditedName'),
            track_number=data.get('trackNumber'),
            order_number=data.get('orderNumber'),
            primary_artists=[ImportedArtist.from_dict(artist) for artist in data["primaryArtists"]],
        )

    def to_dict(self):
        return {
            "youtubeTrackId": self.youtubeTrackId,
            "title": self.title,
            "creditedName": self.creditedName,
            "trackNumber": self.trackNumber,
            "primaryArtists": [artist.to_dict() for artist in (self.primaryArtists or [])],
            "orderNumber": self.orderNumber,
            "isAvailable": self.isAvailable,
        }
