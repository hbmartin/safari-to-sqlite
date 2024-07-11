class SafariValueError(Exception):
    """Base class for exceptions raised during conversion."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class FailedDownloadError(SafariValueError):
    """Page download error."""

    def __init__(self, code: int) -> None:
        super().__init__(
            f"Download failed with status code {code}",
        )
        self.code = code
