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
    - Coordinate navigation availability.

The CentralWorkspace SHALL NOT implement business logic.
All application logic SHALL be delegated to the Core Engine
and feature-specific UI components.

Navigation locking is a workspace-level UI concern. It does not
contain learning or feature-specific business rules.

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

    The CentralWorkspace owns the application's central content area.

    Feature modules such as Home, Flashcard, Quiz, and Transliteration
    SHALL be hosted inside the internal QTabWidget.

    Business logic SHALL NOT be implemented in this class.

    Navigation locking is provided as a generic workspace capability.
    Feature-specific components may request navigation isolation through
    the workspace without exposing their business logic to this class.
    """

    def __init__(
        self,
        engine: CoreEngine,
        audio: AudioService,
        flashcard_session: FlashcardSession,
    ) -> None:
        """
        Initialize the central workspace.

        Args:
            engine:
                Shared Core Engine instance used by workspace components.

            audio:
                Shared AudioService instance used by feature tabs.

            flashcard_session:
                Shared FlashcardSession instance.
        """

        super().__init__()

        self._engine = engine
        self._audio = audio
        self._flashcard_session = flashcard_session

        self._tab_widget: QTabWidget | None = None

        self._home_tab: HomeTab | None = None
        self._script_explorer_tab: ScriptExplorerTab | None = None
        self._flashcard_tab: FlashcardTab | None = None

        self._navigation_locked = False
        self._navigation_lock_states: dict[int, bool] = {}

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        """
        Initialize the central workspace UI.

        This method creates the workspace layout, instantiates the
        tab widget, and registers all currently available feature tabs.
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

    def set_navigation_locked(
        self,
        locked: bool,
    ) -> None:
        """
        Lock or unlock workspace tab navigation.

        When navigation is locked, the currently active tab remains
        enabled while all other tabs become disabled.

        The previous enabled state of every tab is preserved and
        restored when navigation is unlocked.

        This method controls workspace navigation only. It does not
        implement any feature-specific business logic.

        Args:
            locked:
                True to lock navigation, False to restore navigation.
        """

        if self._tab_widget is None:
            return

        if locked == self._navigation_locked:
            return

        if locked:
            self._navigation_lock_states.clear()

            current_index = self._tab_widget.currentIndex()

            for index in range(
                self._tab_widget.count(),
            ):
                self._navigation_lock_states[index] = (
                    self._tab_widget.isTabEnabled(index)
                )

                self._tab_widget.setTabEnabled(
                    index,
                    index == current_index,
                )

            self._navigation_locked = True

            return

        for index, enabled in self._navigation_lock_states.items():
            if index < self._tab_widget.count():
                self._tab_widget.setTabEnabled(
                    index,
                    enabled,
                )

        self._navigation_lock_states.clear()
        self._navigation_locked = False

    @property
    def navigation_locked(self) -> bool:
        """
        Return whether workspace navigation is currently locked.
        """

        return self._navigation_locked