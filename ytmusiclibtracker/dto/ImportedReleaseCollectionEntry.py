from typing import List, Optional

from ytmusiclibtracker.dto.ImportedTrackCollectionEntry import ImportedTrackCollectionEntry


class ImportedReleaseCollectionEntry:
    def __init__(
            self,
            track_ratings: List[ImportedTrackCollectionEntry],
            release_code: Optional[str] = None,
            release_youtube_browse_id: Optional[str] = None,
            is_user_uploaded: bool = False,
            rating: Optional[float] = None,
            rated_on: Optional[str] = None,
    ):
        if track_ratings is None:
            raise ValueError("track_ratings must not be None")

        if is_user_uploaded is None:
            raise ValueError("is_user_uploaded must not be None")

        self.releaseCode = release_code
        self.releaseYoutubeBrowseId = release_youtube_browse_id
        self.isUserUploaded = is_user_uploaded
        self.rating = rating
        self.ratedOn = rated_on
        self.trackRatings = track_ratings

    def to_dict(self) -> dict:
        return {
            "releaseCode": self.releaseCode,
            "releaseYoutubeBrowseId": self.releaseYoutubeBrowseId,
            "isUserUploaded": self.isUserUploaded,
            "rating": self.rating,
            "ratedOn": self.ratedOn,
            "trackRatings": [entry.to_dict() for entry in self.trackRatings],
        }
