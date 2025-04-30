from typing import Optional


class ImportedArtist:
    def __init__(
            self,
            full_name: str,
            youtube_channel_id: Optional[str] = None,
            code: Optional[str] = None,
            localized_full_name: Optional[str] = None,
            url: Optional[str] = None,
    ):
        self.youtubeChannelId = youtube_channel_id
        self.code = code
        self.fullName = full_name
        self.localizedFullName = localized_full_name
        self.url = url

    @classmethod
    def from_dict(cls, data: dict) -> "ImportedArtist":
        return cls(
            full_name=data["fullName"],
            youtube_channel_id=data.get("youtubeChannelId"),
            code=data.get("code"),
            localized_full_name=data.get("localizedFullName"),
            url=data.get("url"),
        )

    def to_dict(self):
        return {
            "youtubeChannelId": self.youtubeChannelId,
            "code": self.code,
            "fullName": self.fullName,
            "localizedFullName": self.localizedFullName,
            "url": self.url
        }
