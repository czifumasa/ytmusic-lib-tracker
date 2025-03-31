from typing import List, Optional

from ytmusiclibtracker.dto.ImportedPlaylistItem import ImportedPlaylistItem


class ImportedPlaylist:
    def __init__(
            self,
            youtube_playlist_id: str,
            title: str,
            items: List[ImportedPlaylistItem],
            description: Optional[str],
            year: Optional[str],
            author: Optional[str]

    ):
        self.youtubePlaylistId = youtube_playlist_id
        self.title = title
        self.items = items
        self.description = description
        self.year = year
        self.author = author

    def to_dict(self):
        return {
            "youtubePlaylistId": self.youtubePlaylistId,
            "title": self.title,
            "description": self.description,
            "year": self.year,
            "author": self.author,
            "items": [item.to_dict() for item in self.items]
        }
