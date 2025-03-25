from typing import List

from ytmusiclibtracker.dto.ImportedPlaylistItem import ImportedPlaylistItem


class ImportedPlaylist:
    def __init__(
            self,
            youtube_playlist_id: str,
            title: str,
            items: List[ImportedPlaylistItem]

    ):
        self.youtubePlaylistId = youtube_playlist_id
        self.title = title
        self.items = items

    def to_dict(self):
        return {
            "youtubePlaylistId": self.youtubePlaylistId,
            "title": self.title,
            "items": [item.to_dict() for item in self.items]
        }
