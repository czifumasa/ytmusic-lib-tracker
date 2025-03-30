from typing import Optional, List

from ytmusiclibtracker.dto.ImportedArtist import ImportedArtist
from ytmusiclibtracker.dto.ImportedTrack import ImportedTrack


class ImportedRelease:
    def __init__(
            self,
            title: str,
            tracks: List[ImportedTrack],
            primary_artists: List[ImportedArtist],
            complete_track_list: bool,
            is_user_uploaded: bool,
            release_type: Optional[str] = None,
            code: Optional[str] = None,
            release_year: Optional[str] = None,
            url: Optional[str] = None,
            credited_name: Optional[str] = None,
            youtube_browse_id: Optional[str] = None,
            youtube_playlist_id: Optional[str] = None,
    ):
        self.title = title
        self.tracks = tracks
        self.primaryArtists = primary_artists
        self.completeTrackList = complete_track_list
        self.isUserUploaded = is_user_uploaded
        self.releaseType = release_type
        self.code = code
        self.releaseYear = release_year
        self.url = url
        self.creditedName = credited_name
        self.youtubeBrowseId = youtube_browse_id
        self.youtubePlaylistId = youtube_playlist_id

    def to_dict(self):
        return {
            "title": self.title,
            "tracks": [track.to_dict() for track in self.tracks],
            "primaryArtists": [artist.to_dict() for artist in self.primaryArtists],
            "completeTrackList": self.completeTrackList,
            "isUserUploaded": self.isUserUploaded,
            "releaseType": self.releaseType,
            "code": self.code,
            "releaseYear": self.releaseYear,
            "url": self.url,
            "creditedName": self.creditedName,
            "youtubeBrowseId": self.youtubeBrowseId,
            "youtubePlaylistId": self.youtubePlaylistId,
        }
