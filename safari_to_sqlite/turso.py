import json
import shutil
import subprocess
from pathlib import Path

from loguru import logger

from safari_to_sqlite.constants import TURSO_AUTH_TOKEN, TURSO_SAFARI, TURSO_URL


def turso_setup() -> tuple[str, str]:
    """Set up Turso database with their CLI and return URL and auth token."""
    db_name = "safari-tabs"
    if shutil.which("turso") is None:
        logger.warning("Turso not found, trying to install it with brew.")
        subprocess.run(["brew", "install", "tursodatabase/tap/turso"], check=True)
    subprocess.run(["turso", "auth", "signup"], check=True)
    subprocess.run(["turso", "db", "create", db_name], check=False)
    logger.info(f"Turso database created: {db_name}")
    result = subprocess.run(
        ["turso", "db", "show", "--url", db_name],
        capture_output=True,
        check=False,
    )
    url = result.stdout.decode().strip()
    logger.info(f"Turso database URL: {url}")
    result = subprocess.run(
        ["turso", "db", "tokens", "create", db_name],
        capture_output=True,
        check=False,
    )
    auth_token = result.stdout.decode().strip()
    logger.info(f"Turso auth token: {auth_token[:10]}...")
    return url, auth_token


def save_auth(auth_path: str, url: str, auth_token: str) -> None:
    """Save Turso auth data to JSON file."""
    logger.info(f"Saving Turso auth data to {auth_path}")
    auth_json_path = Path(auth_path)
    if auth_json_path.exists():
        auth_data = json.loads(auth_json_path.read_text())
    else:
        auth_data = {}
    auth_data[TURSO_SAFARI] = {TURSO_URL: url, TURSO_AUTH_TOKEN: auth_token}
    auth_json_path.write_text(json.dumps(auth_data, indent=4) + "\n")
