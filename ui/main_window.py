"""
main_window.py

Main application window.

This module implements the primary application window of the
Aksara Nusantara desktop application.

Responsibilities
----------------
- Create the main application window.
- Own the menu bar.
- Own the tool bar.
- Own the status bar.
- Host the central workspace.

This module SHALL NOT implement business logic.

References
----------
APPLICATION_ARCHITECTURE.md
    - Section 8 : MainWindow
    - Section 11: Workspace Layout
    - Section 12: Communication Model
"""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QStatusBar
from PySide6.QtWidgets import QToolBar

from core.engine import CoreEngine
from core.services.audio_service_legacy import AudioService
from application.learning.flashcard.flashcard_session import (
    FlashcardSession,
)
from .central_workspace import CentralWorkspace


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(
        self,
        engine: CoreEngine,
        audio: AudioService,
        flashcard_session: FlashcardSession,
    ) -> None:
        super().__init__()

        self._engine = engine

        self._audio = audio

        self._flashcard_session = flashcard_session

        self._status_bar: QStatusBar | None = None
        self._main_toolbar: QToolBar | None = None

        self._initialize_ui()

    def _initialize_ui(self) -> None:

        self.setWindowTitle("Aksara Nusantara")
        self.resize(1280, 720)

        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        self._create_central_workspace()

    def _create_menu_bar(self) -> None:

        menu_bar = self.menuBar()

        menu_bar.addMenu("&File")
        menu_bar.addMenu("&Help")

    def _create_tool_bar(self) -> None:

        self._main_toolbar = QToolBar("Main Toolbar")

        self.addToolBar(self._main_toolbar)

    def _create_status_bar(self) -> None:

        self._status_bar = QStatusBar()

        self._status_bar.showMessage("Ready")

        self.setStatusBar(self._status_bar)

    def _create_central_workspace(self) -> None:

        self.setCentralWidget(
            CentralWorkspace(
                engine=self._engine,
                audio=self._audio,
                flashcard_session=self._flashcard_session
            )
        )