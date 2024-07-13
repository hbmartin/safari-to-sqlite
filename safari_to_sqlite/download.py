from mureq import Response, get
from trafilatura import extract

from safari_to_sqlite.constants import ScrapeStatus
from safari_to_sqlite.errors import FailedDownloadError


def _download(url: str) -> str:
    response: Response = get(url, max_redirects=2)
    if not response.ok:
        raise FailedDownloadError(response.status_code)
    try:
        return response.content.decode()
    except UnicodeDecodeError as e:
        raise FailedDownloadError(ScrapeStatus.UnicodeFailed.value) from e


def extract_body(url: str) -> str:
    """Download and extract body from a URL."""
    body = _download(url)
    return extract(
        body,
        output_format="markdown",
        favor_recall=True,
        include_links=True,
    )
