"""
Learning Engine storage adapter abstraction.

This module defines the storage boundary used by the Learning
Repository to communicate with a concrete persistence mechanism.

Architecture references:
    AD-LE-006 — Persistence operations are handled through
                Learning Repository.
    AD-LE-009 — Learning Engine SHALL NOT depend on a specific
                storage technology.
"""

from abc import ABC, abstractmethod
from typing import Any


class StorageAdapter(ABC):
    """
    Abstract interface for Learning Engine persistent storage.

    StorageAdapter hides concrete storage technology from the
    Learning Repository.

    Implementations may use JSON files, SQLite, cloud storage,
    or another persistence mechanism.
    """

    @abstractmethod
    def save(
        self,
        key: str,
        data: Any,
    ) -> None:
        """
        Persist data under a logical key.

        Args:
            key: Logical storage key.
            data: Serializable data to persist.
        """
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        key: str,
    ) -> Any | None:
        """
        Load data associated with a logical key.

        Args:
            key: Logical storage key.

        Returns:
            Stored data, or None when the key does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete data associated with a logical key.

        Args:
            key: Logical storage key.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Determine whether a logical key exists.

        Args:
            key: Logical storage key.

        Returns:
            True if the key exists, otherwise False.
        """
        raise NotImplementedError