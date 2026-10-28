"""SQLite store: one conversation and one case file per user (WhatsApp number or web session)."""

import json
import sqlite3
import uuid
from datetime import datetime, timezone

from app.config import settings

MAX_HISTORY = 20

_SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    user_id TEXT PRIMARY KEY,
    history TEXT NOT NULL,
    case_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS seen_messages (
    message_id TEXT PRIMARY KEY
);
"""


def _connect() -> sqlite3.Connection:
    settings.var_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.db_path)
    conn.executescript(_SCHEMA)
    return conn


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_case() -> dict:
    return {
        "case_id": uuid.uuid4().hex[:8].upper(),
        "file_token": uuid.uuid4().hex,
        "created_at": _now(),
        "facts": {},
        "documents": [],
        "transcripts": [],
        "sources": [],
        "eligibility": None,
        "office": None,
        "draft": None,
        "escalated": None,
    }


def load(user_id: str) -> tuple[list[dict], dict]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT history, case_json FROM conversations WHERE user_id = ?", (user_id,)
        ).fetchone()
    if row is None:
        return [], new_case()
    return json.loads(row[0]), json.loads(row[1])


def save(user_id: str, history: list[dict], case: dict) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO conversations (user_id, history, case_json, updated_at) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET history = excluded.history, "
            "case_json = excluded.case_json, updated_at = excluded.updated_at",
            (
                user_id,
                json.dumps(history[-MAX_HISTORY:], ensure_ascii=False),
                json.dumps(case, ensure_ascii=False),
                _now(),
            ),
        )


def reset(user_id: str) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))


def mark_seen(message_id: str) -> bool:
    """Record a webhook message id. Returns False if it was already processed (WhatsApp retries)."""
    with _connect() as conn:
        try:
            conn.execute("INSERT INTO seen_messages (message_id) VALUES (?)", (message_id,))
        except sqlite3.IntegrityError:
            return False
    return True
