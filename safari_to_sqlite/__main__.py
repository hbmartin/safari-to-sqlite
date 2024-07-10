#!/usr/bin/env python

import logging
import time
from collections import Counter
from functools import reduce
from socket import gethostname
from sys import argv, stderr

from loguru import logger

from safari_to_sqlite.blacklist import filter_blacklist
from safari_to_sqlite.safari import get_safari_tabs
from safari_to_sqlite.turso import get_auth_creds_from_json, save_auth, turso_setup

from .datastore import Datastore


def auth(auth_path: str) -> None:
    """Save authentication credentials to a JSON file."""
    turso_url = input(
        "Enter your Turso database URL e.g. libsql://<yours>.turso.io\n"
        "(Leave this blank to start new DB setup)\n> ",
    )
    if turso_url == "":
        (turso_url, turso_auth_token) = turso_setup()
        save_auth(auth_path, turso_url, turso_auth_token)
    elif not turso_url.startswith("libsql://"):
        logger.error("Invalid libsql URL, please try again.")
        return
    else:
        turso_auth_token = input(
            "Enter your Turso database token\n"
            "(Create this by running `turso db tokens create <your DB>`)\n> ",
        )
        save_auth(auth_path, turso_url, turso_auth_token)


def save(
    db_path: str,
    auth_json: str,
) -> None:
    """Save Safari tabs to SQLite database."""
    host = gethostname()
    first_seen = int(time.time())
    logger.info(f"Loading tabs from Safari for {host}...")

    tabs, urls = get_safari_tabs(host, first_seen)
    logger.info(f"Finished loading tabs, connecting to database: {db_path}")

    initial_count = len(tabs)
    tabs = [tab for tab in tabs if filter_blacklist(tab.url)]
    duplicate_count = reduce(lambda acc, val: acc + val - 1, Counter(urls).values())
    blacklist_count = initial_count - len(tabs)
    logger.info(
        f"Found {len(tabs)} tabs ({duplicate_count} duplicates, "
        f"{blacklist_count} blacklisted)",
    )

    db = Datastore(db_path, **get_auth_creds_from_json(auth_json))
    db.insert_tabs(tabs)


def _configure_logging() -> None:
    # Ours
    logger.remove()
    logger.add(
        stderr,
        colorize=True,
        format="{time:HH:mm:ss.SS} | <level>{message}</level>",
    )
    # Turso
    replication_logger = logging.getLogger("libsql_replication")
    remote_client_logger = logging.getLogger("libsql.replication.remote_client")
    replication_logger.setLevel(logging.WARNING)
    remote_client_logger.setLevel(logging.WARNING)


def request_missing_bodies(db_path: str, auth_json: str) -> None:
    """Request body when missing and save extracted contents."""
    db = Datastore(db_path, **get_auth_creds_from_json(auth_json))
    for url, title in db.find_empty_body():
        logger.warning(f"Downloading and extracting body for {title} @ {url}")


def main() -> None:
    """Start main entry point."""
    _configure_logging()
    db_default = "safari_tabs.db"
    auth_default = "auth.json"
    if len(argv) == 1 or argv[1].endswith(".db"):
        db = argv[1] if len(argv) > 1 else db_default
        auth_path = argv[2] if len(argv) > 2 else auth_default  # noqa: PLR2004
        save(db, auth_path)
    elif argv[1] == "auth":
        auth_path = argv[1] if len(argv) > 1 else auth_default
        auth(auth_path)
    elif argv[1] == "req":
        db = argv[2] if len(argv) > 2 else db_default  # noqa: PLR2004
        auth_path = argv[3] if len(argv) > 3 else auth_default  # noqa: PLR2004
        request_missing_bodies(db, auth_path)
    else:
        pass


if __name__ == "__main__":
    main()
