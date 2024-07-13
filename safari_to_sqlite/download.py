from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPException
from os import cpu_count

from loguru import logger
from mureq import Response, TooManyRedirects, get
from trafilatura import extract

from safari_to_sqlite.constants import ScrapeStatus
from safari_to_sqlite.errors import FailedDownloadError

POOL_SIZE = int(cpu_count() if cpu_count() is not None else 6)


def _download(url: str) -> str:
    response: Response = get(url, max_redirects=2)
    if not response.ok:
        raise FailedDownloadError(response.status_code)
    try:
        return response.content.decode()
    except UnicodeDecodeError as e:
        raise FailedDownloadError(ScrapeStatus.UnicodeFailed.value) from e


def extract_bodies(
    urls: Iterable[tuple[str]],
) -> tuple[list[tuple[str, str]], list[tuple[str, int]]]:
    """Download and extract bodies from URLs."""

    def _extract_body(url_tuple: tuple[str]) -> tuple[str, str | int]:
        url = url_tuple[0]
        try:
            body = _download(url)
            extracted: str = extract(
                body,
                output_format="markdown",
                favor_recall=True,
                include_links=True,
            )
            return url, extracted
        except FailedDownloadError as e:
            return url, e.code
        except TooManyRedirects:
            return url, ScrapeStatus.RedirectsExceeded.value
        except TimeoutError:
            return url, ScrapeStatus.Timeout.value
        except HTTPException:
            return url, ScrapeStatus.UnknownHttp.value

    successes: list[tuple[str, str]] = []
    errors: list[tuple[str, int]] = []
    with ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
        # Mapping the read_first_line function over all file paths
        for result in executor.map(_extract_body, urls):
            if isinstance(result[1], int):
                errors.append(result)
            else:
                successes.append(result)
            if len(successes) % 10 == 0:
                logger.info(f"Extracted {len(successes)} bodies so far...")
            if len(errors) % 10 == 0:
                logger.info(f"Encountered {len(errors)} errors so far...")
    return successes, errors
