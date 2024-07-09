#!/usr/bin/env python
import json
import logging
import time
from collections import Counter
from pathlib import Path
from socket import gethostname
from sys import argv, stderr

from loguru import logger

from safari_to_sqlite.constants import TURSO_AUTH_TOKEN, TURSO_SAFARI, TURSO_URL
from safari_to_sqlite.safari import get_safari_tabs
from safari_to_sqlite.turso import save_auth, turso_setup

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

    auth_path = Path(auth_json)
    turso_auth = None
    if auth_path.is_file():
        auth_data = json.loads(auth_path.read_text())
        turso_auth = auth_data[TURSO_SAFARI]
    else:
        logger.warning(f"Auth file {auth_json} not found, skipping remote sync.")

    tabs, urls = get_safari_tabs(host, first_seen)
    logger.info(f"Finished loading tabs, connecting to database: {db_path}")
    duplicate_count = 0
    for _, count in Counter(urls):
        if count > 1:
            duplicate_count += count - 1
    logger.info(
        f"Inserting {len(tabs) - duplicate_count} tabs (ignoring existing URLs)",
    )

    db = (
        Datastore(db_path, None, None)
        if turso_auth is None
        else Datastore(db_path, turso_auth[TURSO_URL], turso_auth[TURSO_AUTH_TOKEN])
    )
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


def main() -> None:
    """Start main entry point."""
    _configure_logging()
    auth_default = "auth.json"
    if len(argv) == 1 or argv[1].endswith(".db"):
        db = argv[1] if len(argv) > 1 else "safari_tabs.db"
        auth_path = argv[2] if len(argv) > 2 else auth_default  # noqa: PLR2004
        save(db, auth_path)
    elif argv[1] == "auth":
        auth_path = argv[1] if len(argv) > 1 else auth_default
        auth(auth_path)
    else:
        pass


if __name__ == "__main__":
    main()
