"""
home_tab.py

Home tab implementation.

This module implements the Home tab of the Aksara Nusantara
desktop application.

Responsibilities
----------------
- Provide the application's landing page.
- Display the welcome message.
- Serve as the starting point for future dashboard features.

Future versions may display:
- Active ScriptPack
- Learning progress
- Recent activity
- Project news
- Quick actions

This module SHALL NOT implement business logic.

References
----------
APPLICATION_ARCHITECTURE.md
    - Section 11 : Workspace Layout
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class HomeTab(QWidget):
    """
    Home tab.

    The HomeTab class represents the application's landing page.

    This widget is responsible for presenting introductory
    information to the user and will gradually evolve into the
    application's dashboard.

    Business logic SHALL NOT be implemented in this class.
    """

    def __init__(self) -> None:
        """
        Initialize the Home tab.
        """

        super().__init__()

        self._layout: QVBoxLayout | None = None
        self._welcome_label: QLabel | None = None

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        """
        Initialize the user interface.
        """

        self._layout = QVBoxLayout(self)

        self._welcome_label = QLabel(
            "Welcome to Aksara Nusantara"
        )

        self._welcome_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self._layout.addWidget(self._welcome_label)