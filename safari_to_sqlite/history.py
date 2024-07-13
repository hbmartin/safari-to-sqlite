import sqlite3
from collections.abc import Iterable
from pathlib import Path

from safari_to_sqlite.constants import Browser
from safari_to_sqlite.datastore import TabRow


def read_history() -> Iterable[TabRow]:
    db_path = Path.home() / "Library/Safari/History.db"
    print(db_path)
    con = sqlite3.connect(db_path)
    query = (
        "SELECT history_items.url, title, visit_time, history_visits.origin "
        "FROM history_visits LEFT JOIN history_items "
        "ON history_visits.history_item=history_items.id;"
    )
    cur = con.cursor()
    for row in cur.execute(query):
        yield TabRow(
            url=row[0],
            title=row[1] or "",
            body="",
            window_id=-1,
            tab_index=-1,
            host="",
            first_seen=int(row[2]),
            scrape_status=-1,
            browser=Browser.Safari.value if row[3] == 1 else Browser.iCloud.value,
        )
    cur.close()
    con.close()
