from typing import Optional


class ImportedAccountInfo:
    def __init__(
            self,
            account_name: Optional[str],
            account_photo_url: Optional[str],
            url: Optional[str]
    ):
        if account_name is None or account_name.strip() == "":
            raise ValueError("account_name must not be null or blank")

        if account_photo_url is not None and account_photo_url.strip() == "":
            raise ValueError("account_photo_url must not be blank")

        if url is None or url.strip() == "":
            raise ValueError("url must not be null or blank")

        self.accountName = account_name
        self.accountPhotoUrl = account_photo_url
        self.url = url

    def to_dict(self):
        return {
            "accountName": self.accountName,
            "accountPhotoUrl": self.accountPhotoUrl,
            "url": self.url,
        }
