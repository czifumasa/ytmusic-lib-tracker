from typing import Optional


class ImportedPlaylistItem:
    def __init__(
            self,
            is_available: bool,
            order_number: Optional[int],
            youtube_track_id: Optional[str],
            youtube_set_item_id: Optional[str],
    ):
        if is_available is None:
            raise ValueError("is_available must not be None")

        if youtube_track_id is not None and youtube_track_id.strip() == "":
            raise ValueError("youtube_track_id must not be blank")

        if youtube_set_item_id is not None and youtube_set_item_id.strip() == "":
            raise ValueError("youtube_set_item_id must not be blank")

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
