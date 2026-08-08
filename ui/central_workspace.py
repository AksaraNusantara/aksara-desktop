"""
===============================================================================

Aksara Nusantara

Module:
    ui.central_workspace

Module Type:
    User Interface

Purpose:
    Provides the application's central workspace.

Responsibilities:
    - Own the application's tab container.
    - Host all feature tabs.
    - Coordinate workspace layout.

The CentralWorkspace SHALL NOT implement business logic.
All application logic SHALL be delegated to the Core Engine
and feature-specific UI components.

References:
    APPLICATION_ARCHITECTURE.md

    docs/standards/PYTHON_MODULE_TEMPLATE.md

    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

from __future__ import annotations

from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from core.engine import CoreEngine
from core.services.audio_service import AudioService
from application.learning.flashcard.flashcard_session import (
    FlashcardSession,
)

from .tabs.home_tab import HomeTab
from .tabs.flashcard_tab import FlashcardTab
from .tabs.script_explorer_tab import ScriptExplorerTab


class CentralWorkspace(QWidget):
    """
    Central application workspace.

    The CentralWorkspace class owns the application's
    central content area.

    Feature modules such as Home, Flashcard, Quiz,
    and Transliteration SHALL be hosted inside the
    internal QTabWidget.

    Business logic SHALL NOT be implemented in this class.
    """

    def __init__(
        self,
        engine: CoreEngine,
        audio: AudioService,
        flashcard_session: FlashcardSession,
    ) -> None:
        """
        Initialize the central workspace.

        This method creates the workspace layout,
        instantiates the tab widget,
        and registers all feature tabs.

        Returns
        -------
        None
        """
        super().__init__()
        self._engine = engine
        self._audio = audio
        self._flashcard_session = flashcard_session
        self._tab_widget: QTabWidget | None = None
        self._home_tab: HomeTab | None = None
        self._flashcard_tab: FlashcardTab | None = None
        self._initialize_ui()

    def _initialize_ui(self) -> None:
        """
        Initialize the central workspace.

        Parameters
        ----------
        engine:
            Shared Core Engine instance used by all
            workspace components.
        """
        layout = QVBoxLayout(self)

        self._tab_widget = QTabWidget()

        self._home_tab = HomeTab(
            self._engine,
        )

        self._tab_widget.addTab(
            self._home_tab,
            "Home",
        )

        self._script_explorer_tab = ScriptExplorerTab(
            engine=self._engine,
            audio=self._audio,
        )

        self._tab_widget.addTab(
            self._script_explorer_tab,
            "Script Explorer",
        )

        self._script_explorer_tab.open_home_requested.connect(
            self._show_home_tab,
        )

        self._flashcard_tab = FlashcardTab(
            engine=self._engine,
            session=self._flashcard_session,
            audio=self._audio,
        )

        self._tab_widget.addTab(
            self._flashcard_tab,
            "Flashcard",
        )

        self._flashcard_tab.open_home_requested.connect(
            self._show_home_tab,
        )

        layout.addWidget(self._tab_widget)

    def _show_home_tab(self) -> None:
        """
        Display the Home tab.
        """

        self._tab_widget.setCurrentWidget(
            self._home_tab,
        )