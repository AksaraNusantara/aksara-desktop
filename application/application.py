"""
application.py

Application lifecycle coordinator.

Implements:
- APPLICATION_ARCHITECTURE.md
    - Section 5: Application Bootstrap
    - Section 13: Startup Sequence
"""

from __future__ import annotations


class Application:
    """Coordinates the application lifecycle."""

    def __init__(self) -> None:
        self._initialized = False

    @property
    def initialized(self) -> bool:
        """Return whether the application has been initialized."""
        return self._initialized

    def initialize(self) -> None:
        """Initialize the application."""
        self._initialized = True

    def run(self) -> int:
        """Run the application."""
        if not self._initialized:
            raise RuntimeError("Application has not been initialized.")

        return 0

    def shutdown(self) -> None:
        """Shutdown the application."""
        self._initialized = False