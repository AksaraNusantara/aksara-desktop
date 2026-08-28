"""Application-owned persistent state storage."""

from typing import Any

from core.learning.storage.storage_adapter import StorageAdapter


class ApplicationStateStorage:
    """Persist and retrieve Application-owned state."""

    APPLICATION_STATE_KEY = "application_state"

    def __init__(self, storage: StorageAdapter) -> None:
        self._storage = storage

    def save(self, state: dict[str, Any]) -> None:
        """Persist Application state."""

        self._storage.save(
            self.APPLICATION_STATE_KEY,
            state,
        )

    def load(self) -> dict[str, Any] | None:
        """Load persisted Application state."""

        return self._storage.load(
            self.APPLICATION_STATE_KEY,
        )
