"""
central_workspace.py

Central application workspace.

This module implements the central workspace of the
Aksara Nusantara desktop application.

Responsibilities
----------------
- Host the application's primary content.
- Own the application's tab container.
- Provide a stable entry point for feature modules.

This module SHALL NOT implement business logic.

References
----------
APPLICATION_ARCHITECTURE.md
    - Section 11 : Workspace Layout
"""

from __future__ import annotations

from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from .tabs.home_tab import HomeTab


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

    def __init__(self) -> None:
        """
        Initialize the central workspace.
        """

        super().__init__()

        self._layout: QVBoxLayout | None = None
        self._tab_widget: QTabWidget | None = None

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        """
        Initialize the workspace user interface.
        """

        self._layout = QVBoxLayout(self)

        self._tab_widget = QTabWidget()

        self._tab_widget.addTab(
            HomeTab(),
            "Home",
        )

        self._layout.addWidget(self._tab_widget)