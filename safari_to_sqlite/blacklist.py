_blacklist = {
    "ally.com/",
    "americanexpress.com/",
    "bankofamerica.com/",
    "capitalone.com/",
    "chase.com/",
    "citi.com/",
    "discover.com/",
    "etrade.com/",
    "fidelity.com/",
    "gmail.com/",
    "hotmail.com/",
    "mail.google.com/",
    "outlook.com/",
    "paypal.com/",
    ".slack.com/",
    "schwab.com/",
    "tdameritrade.com/",
    "usaa.com/",
    "usbank.com/",
    "vanguard.com/",
    "wellsfargo.com/",
}


def filter_blacklist(url: str) -> bool:
    """Filter out blacklisted URLs."""
    return all(blacklisted not in url for blacklisted in _blacklist)
