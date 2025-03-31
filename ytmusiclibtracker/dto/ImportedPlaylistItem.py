from typing import Optional


class ImportedPlaylistItem:
    def __init__(
            self,
            is_available: bool,
            order_number: Optional[int],
            youtube_track_id: Optional[str],
            youtube_set_item_id: Optional[str],
    ):
        self.isAvailable = is_available
        self.orderNumber = order_number
        self.youtubeTrackId = youtube_track_id
        self.youtubeSetItemId = youtube_set_item_id

    def to_dict(self):
        return {
            "isAvailable": self.isAvailable,
            "orderNumber": self.orderNumber,
            "youtubeTrackId": self.youtubeTrackId,
            "youtubeSetItemId": self.youtubeSetItemId
        }
