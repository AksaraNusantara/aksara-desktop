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

from PySide6.QtGui import QFontDatabase

from core.engine import CoreEngine
from ui.main_window import MainWindow


class Application:
    """
    Application lifecycle coordinator.
    """

    def __init__(self) -> None:

        self._initialized: bool = False

        self._engine = CoreEngine()

        self._main_window: MainWindow | None = None

    def _load_fonts(self) -> None:
        """
        Register bundled application fonts.
        """

        font_directory = (
            Path(__file__).parent.parent
            / "assets"
            / "fonts"
        )

        print(f"Font directory : {font_directory}")

        font_files = sorted(
            font_directory.glob("*.ttf")
        )

        print(f"Found fonts    : {font_files}")

        for font_file in font_files:

            font_id = QFontDatabase.addApplicationFont(
                str(font_file)
            )

            if font_id == -1:
                raise RuntimeError(
                    f"Failed to load font: {font_file.name}"
                )

            families = QFontDatabase.applicationFontFamilies(
                font_id
            )

            print(f"Loaded : {font_file.name}")
            print(f"Family : {families}")

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
        # Register bundled fonts.
        #

        self._load_fonts()

        #
        # Initialize Core Engine.
        #

        self._engine.initialize(
            Path("scriptpacks")
        )

        #
        # Create Main Window.
        #

        self._main_window = MainWindow(
            self._engine
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