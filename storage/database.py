"""SQLite database manager and connection helper for TRIBUNAL storage layer."""

from __future__ import annotations

import contextlib
import logging
import sqlite3
from pathlib import Path
from typing import Generator, Union

logger = logging.getLogger("tribunal.storage.database")

DEFAULT_DB_PATH = Path(__file__).resolve().parent / "tribunal.db"

INIT_SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS investigations (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    query TEXT NOT NULL,
    dataset TEXT NOT NULL,
    planner_intent TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    confidence REAL NOT NULL,
    recommendation TEXT NOT NULL,
    status TEXT NOT NULL,
    duration_ms REAL NOT NULL,
    version TEXT NOT NULL,
    report_path TEXT,
    graph_path TEXT,
    case_path TEXT
);

CREATE TABLE IF NOT EXISTS reports (
    investigation_id TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    format TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    FOREIGN KEY(investigation_id) REFERENCES investigations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS graphs (
    investigation_id TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    FOREIGN KEY(investigation_id) REFERENCES investigations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS verdicts (
    investigation_id TEXT PRIMARY KEY,
    winning_hypothesis TEXT NOT NULL,
    runner_up TEXT,
    confidence REAL NOT NULL,
    recommendation TEXT NOT NULL,
    FOREIGN KEY(investigation_id) REFERENCES investigations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id TEXT NOT NULL,
    event TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    details TEXT
);

CREATE INDEX IF NOT EXISTS idx_investigations_created_at ON investigations(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_investigation_id ON audit(investigation_id);
"""


class DatabaseManager:
    """Manages SQLite connection lifecycle, schema initialization, and context scoping."""

    def __init__(self, db_path: Union[str, Path] = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def init_db(self) -> None:
        """Initialize database schema tables if not present."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(INIT_SCHEMA_SQL)
                conn.commit()
            logger.info(f"Initialized SQLite database schema at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize SQLite database at {self.db_path}: {e}")
            raise

    @contextlib.contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager yielding configured SQLite connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()
