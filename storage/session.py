"""Storage session management module."""

from pathlib import Path
from typing import Optional
from storage.database import DatabaseManager, DEFAULT_DB_PATH

_global_db_manager: Optional[DatabaseManager] = None


def get_database_manager(db_path: Optional[Path] = None) -> DatabaseManager:
    """Retrieve or construct global DatabaseManager instance."""
    global _global_db_manager
    if _global_db_manager is None or (db_path is not None and _global_db_manager.db_path != db_path):
        _global_db_manager = DatabaseManager(db_path or DEFAULT_DB_PATH)
    return _global_db_manager
