from typing import Optional


class ImportedTrackCollectionEntry:
    def __init__(
            self,
            order_number: Optional[int],
            youtube_track_id: Optional[str],
            is_user_uploaded: bool = False,
            rating: Optional[float] = None,
    ):
        if is_user_uploaded is None:
            raise ValueError("is_user_uploaded must not be None")

        self.orderNumber = order_number
        self.youtubeTrackId = youtube_track_id
        self.isUserUploaded = is_user_uploaded
        self.rating = rating

    def to_dict(self) -> dict:
        return {
            "orderNumber": self.orderNumber,
            "youtubeTrackId": self.youtubeTrackId,
            "isUserUploaded": self.isUserUploaded,
            "rating": self.rating,
        }
