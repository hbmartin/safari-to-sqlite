from enum import Enum

BODY = "body"
BROWSER = "browser"
FIRST_SEEN = "firstSeen"
HOST = "host"  # refers to user's local hostname NOT the URL host
SCRAPE_STATUS = "scrapeStatus"
TABS = "tabs"
TAB_INDEX = "tabIndex"
TITLE = "title"
URL = "url"
WINDOW_ID = "windowId"

TURSO_SAFARI = "turso_safari"
TURSO_URL = "turso_url"
TURSO_AUTH_TOKEN = "turso_auth_token"  # noqa: S105


class ScrapeStatus(int, Enum):
    """Enum for scrape status."""

    NotScraped = -1
    ExtractFailed = -2
    UnicodeFailed = -3


class Browser(str, Enum):
    """Enum for browser."""

    Safari = "safari"
    Icloud = "icloud"
    Chrome = "chrome"


SEP = "150r2M72e7D6Lb7Z9u1g4BSQBonv6U21W1fmX8B1TXR8XXqB2wTgQzqwoB06144d"
