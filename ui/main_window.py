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
- Host the active workspace.

This module SHALL NOT implement business logic.

References
----------
APPLICATION_ARCHITECTURE.md
    - Section 8 : MainWindow
    - Section 11: Workspace Layout
    - Section 12: Communication Model
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """
    Main application window.

    The MainWindow class represents the graphical shell of the
    Aksara Nusantara desktop application.

    It is responsible for presenting the user interface and
    coordinating visual components.

    Business logic SHALL NOT be implemented in this class.
    """

    def __init__(self) -> None:
        """
        Initialize the main window.
        """

        super().__init__()

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        """
        Initialize the user interface.

        This method creates and configures all widgets owned by
        the MainWindow.
        """

        self.setWindowTitle("Aksara Nusantara")
        self.resize(1280, 720)

        welcome_label = QLabel("Welcome to Aksara Nusantara")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(welcome_label)