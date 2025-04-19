from typing import Optional


class ImportedPlaylistItem:
    def __init__(
            self,
            is_available: bool,
            order_number: Optional[int],
            youtube_track_id: str,
            youtube_set_item_id: str,
    ):
        if is_available is None:
            raise ValueError("is_available must not be None")

        if youtube_track_id is None or youtube_track_id.strip() == "":
            raise ValueError("youtube_track_id must not be null or blank")

        if youtube_set_item_id is None or youtube_set_item_id.strip() == "":
            raise ValueError("youtube_set_item_id must not be null or blank")

        self.isAvailable = is_available
        self.orderNumber = order_number
        self.youtubeTrackId = youtube_track_id
        self.youtubeSetItemId = youtube_set_item_id

    def to_dict(self) -> dict:
        return {
            "isAvailable": self.isAvailable,
            "orderNumber": self.orderNumber,
            "youtubeTrackId": self.youtubeTrackId,
            "youtubeSetItemId": self.youtubeSetItemId
        }
