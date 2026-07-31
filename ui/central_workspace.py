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

from .tabs.home_tab import HomeTab
from .tabs.flashcard_tab import FlashcardTab


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
        self._tab_widget: QTabWidget | None = None
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
        self._tab_widget.addTab(
            HomeTab(),
            "Home",
        )

        self._tab_widget.addTab(
            FlashcardTab(
                self._engine,
            ),
            "Flashcard",
        )

        layout.addWidget(self._tab_widget)