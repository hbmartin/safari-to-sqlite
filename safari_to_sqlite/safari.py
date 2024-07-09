import subprocess
from pathlib import Path

from .constants import SEP
from .datastore import TabRow


def _get_safari_tabs_raw() -> list[str]:
    """Return tab information as a list of strings requested from AppleScript."""
    parent = Path(__file__).resolve().parent
    command = ["osascript", "-s", "o", f"{parent}/export_from_safari.applescript"]
    result = subprocess.run(command, capture_output=True, check=False)  # noqa: S603
    return result.stderr.decode().strip().splitlines()


def get_safari_tabs(host: str, first_seen: int) -> tuple[list[TabRow], list[str]]:
    """Return all tabs."""
    output_iter = iter(_get_safari_tabs_raw())
    tabs = []
    output_available = True
    urls = []

    while output_available:
        try:
            url = next(output_iter)
            urls.append(url)
            title = next(output_iter)
            window_id = int(next(output_iter))
            tab_index = int(next(output_iter))
            body = ""
            while (line := next(output_iter)) != SEP:
                body += line + "\n"
            # SCRAPE_STATUS is None because the tab has not been scraped yet
            tabs.append(
                (url, title, body, window_id, tab_index, host, first_seen, None),
            )
        except StopIteration:
            output_available = False

    return tabs, urls
