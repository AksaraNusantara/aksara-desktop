"""
workspace.py

Central application workspace.

This module implements the central workspace of the
Aksara Nusantara desktop application.

Responsibilities
----------------
- Host the application's primary content.
- Provide a stable container for feature modules.
- Own the central layout.

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


class Workspace(QWidget):
    """
    Central application workspace.

    The Workspace class owns the application's central content
    area. Feature modules such as Flashcard, Quiz, and
    Transliteration will be hosted inside this widget.
    """

    def __init__(self) -> None:
        """
        Initialize the workspace.
        """

        super().__init__()

        self._layout: QVBoxLayout | None = None

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        """
        Initialize the workspace user interface.
        """

        self._layout = QVBoxLayout(self)

        welcome_label = QLabel("Welcome to Aksara Nusantara")

        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._layout.addWidget(welcome_label)