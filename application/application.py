"""
application.py

Application lifecycle coordinator.

This module implements the root Application object responsible for
coordinating the application lifecycle.

Responsibilities
----------------
- Application bootstrap.
- Runtime lifecycle.
- Core Engine lifecycle.
- Application shutdown.

References
----------
APPLICATION_ARCHITECTURE.md
    - Section 5 : Application Bootstrap
    - Section 13: Startup Sequence
"""

from __future__ import annotations

from pathlib import Path

from core.engine import CoreEngine
from core.services.audio_service import AudioService
from ui.main_window import MainWindow


class Application:
    """
    Application lifecycle coordinator.
    """

    def __init__(self) -> None:

        self._initialized: bool = False

        self._engine = CoreEngine()

        self._audio: AudioService | None = None

        self._main_window: MainWindow | None = None

    @property
    def initialized(self) -> bool:
        """
        Return the application initialization state.
        """
        return self._initialized

    @property
    def engine(self) -> CoreEngine:
        """
        Return the application's Core Engine.
        """
        return self._engine

    @property
    def main_window(self) -> MainWindow | None:
        return self._main_window

    def initialize(self) -> None:

        if self._initialized:
            return

        #
        # Initialize Core Engine.
        #

        self._engine.initialize(
            Path("scriptpacks")
        )

        #
        # Initialize shared services.
        #

        self._audio = AudioService()   

        #
        # Create Main Window.
        #

        self._main_window = MainWindow(
            engine=self._engine,
            audio=self._audio,
        )

        self._initialized = True

    def run(self) -> None:

        if not self._initialized:
            raise RuntimeError(
                "Application has not been initialized."
            )

        assert self._main_window is not None

        self._main_window.show()

    def shutdown(self) -> None:

        if not self._initialized:
            return

        self._initialized = False
