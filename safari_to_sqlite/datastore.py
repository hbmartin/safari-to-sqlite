from collections.abc import Iterable
from typing import TypeAlias

import libsql_experimental as libsql
from loguru import logger

from safari_to_sqlite.constants import (
    BODY,
    FIRST_SEEN,
    HOST,
    SCRAPE_STATUS,
    TAB_INDEX,
    TABS,
    TITLE,
    URL,
    WINDOW_ID,
)

TabRow: TypeAlias = tuple[str, str, str, int, int, str, int, int | None]


class Datastore:
    """Object responsible for all database interactions."""

    def __init__(
        self,
        db_path: str,
        turso_url: str | None,
        turso_auth_token: str | None,
    ) -> None:
        """Instantiate and ensure tables exist with expected columns."""
        self.is_remote = turso_url is not None and turso_auth_token is not None
        if self.is_remote:
            logger.info(f"Connecting to remote db: {turso_url}")
        self.con = (
            libsql.connect(db_path)
            if not self.is_remote
            else libsql.connect(
                db_path,
                sync_url=turso_url,
                auth_token=turso_auth_token,
            )
        )
        self._prepare_db()

    def _prepare_db(self) -> None:
        create_tabs = f"""
        CREATE TABLE IF NOT EXISTS {TABS} (
            {URL} TEXT PRIMARY KEY,
            {TITLE} TEXT NOT NULL,
            {BODY} TEXT,
            {WINDOW_ID} INTEGER,
            {TAB_INDEX} INTEGER,
            {HOST} TEXT,
            {FIRST_SEEN} INTEGER,
            {SCRAPE_STATUS} INTEGER
        );"""
        self.con.execute(create_tabs)
        self.con.commit()
        if self.is_remote:
            self.con.sync()

    def get_tabs(self) -> Iterable[TabRow]:
        """Return all tabs."""
        cur: libsql.Cursor = self.con.cursor()
        yield from cur.execute(
            (
                "SELECT "  # noqa: S608
                f"{URL}, {TITLE}, {BODY}, {WINDOW_ID}, "
                f"{TAB_INDEX}, {HOST}, {FIRST_SEEN}, {SCRAPE_STATUS} "
                f"FROM {TABS};",
            ),
        )
        cur.close()

    def insert_tabs(self, tabs: list[TabRow]) -> None:
        """Insert tabs into the database."""
        insert = f"INSERT OR IGNORE INTO {TABS} VALUES(?, ?, ?, ?, ?, ?, ?, ?);"
        self.con.executemany(insert, tabs)
        self.con.commit()
        logger.info("Local database updated successfully")
        if self.is_remote:
            logger.info("Syncing to remote database")
            self.con.sync()
            logger.info("Finished syncing")
