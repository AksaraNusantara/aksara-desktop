"""
JSON storage implementation for Learning Engine.

This module provides the Reference Implementation of StorageAdapter
using JSON files on the local filesystem.

Architecture references:
    AD-LE-009 — Learning Engine SHALL NOT depend on a specific
                storage technology.

This implementation is replaceable and must not leak JSON-specific
concerns into the Domain Model or Service Layer.
"""

import json
from pathlib import Path
from typing import Any

from .storage_adapter import StorageAdapter


class JSONAdapter(StorageAdapter):
    """
    JSON file-based implementation of StorageAdapter.

    Each logical storage key is represented by one JSON file inside
    the configured storage directory.
    """

    def __init__(self, storage_dir: str | Path) -> None:
        """
        Initialize JSON storage.

        Args:
            storage_dir: Directory used for persistent JSON files.
        """

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _get_path(self, key: str) -> Path:
        """
        Return the filesystem path associated with a storage key.

        Args:
            key: Logical storage key.

        Returns:
            Path of the corresponding JSON file.
        """

        return self.storage_dir / f"{key}.json"

    def save(
        self,
        key: str,
        data: Any,
    ) -> None:
        """
        Persist data as JSON.

        Args:
            key: Logical storage key.
            data: JSON-serializable data.
        """

        path = self._get_path(key)

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def load(
        self,
        key: str,
    ) -> Any | None:
        """
        Load JSON data from storage.

        Args:
            key: Logical storage key.

        Returns:
            Stored data, or None when the file does not exist.
        """

        path = self._get_path(key)

        if not path.exists():
            return None

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete stored JSON data.

        Args:
            key: Logical storage key.
        """

        path = self._get_path(key)

        if path.exists():
            path.unlink()

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check whether a storage key exists.

        Args:
            key: Logical storage key.

        Returns:
            True if the corresponding JSON file exists.
        """

        return self._get_path(key).exists()
