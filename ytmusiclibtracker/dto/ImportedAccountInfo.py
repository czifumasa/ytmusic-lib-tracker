from typing import Optional


class ImportedAccountInfo:
    def __init__(
            self,
            account_name: Optional[str],
            account_photo_url: Optional[str],
            last_synchronize: Optional[str]
    ):
        if account_name is None or account_name.strip() == "":
            raise ValueError("account_name must not be null or blank")

        if account_photo_url is None or account_photo_url.strip() == "":
            raise ValueError("account_photo_url must not be null or blank")

        if last_synchronize is None or last_synchronize.strip() == "":
            raise ValueError("last_synchronize must not be null or blank")

        self.accountName = account_name
        self.accountPhotoUrl = account_photo_url
        self.lastSynchronize = last_synchronize

    def to_dict(self):
        return {
            "accountName": self.accountName,
            "accountPhotoUrl": self.accountPhotoUrl,
            "lastSynchronize": self.lastSynchronize,
        }
