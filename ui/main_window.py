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

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QStatusBar
from PySide6.QtWidgets import QToolBar
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class MainWindow(QMainWindow):
    """
    Main application window.

    The MainWindow class represents the graphical shell of the
    Aksara Nusantara desktop application.

    It is responsible for presenting the application's user
    interface and coordinating visual components.

    Business logic SHALL NOT be implemented in this class.
    """

    def __init__(self) -> None:
        """
        Initialize the main window.
        """

        super().__init__()

        self._central_widget: QWidget | None = None
        self._central_layout: QVBoxLayout | None = None
        self._status_bar: QStatusBar | None = None
        self._main_toolbar: QToolBar | None = None

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        """
        Initialize the user interface.
        """

        self.setWindowTitle("Aksara Nusantara")
        self.resize(1280, 720)

        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        self._create_central_workspace()

    def _create_menu_bar(self) -> None:
        """
        Create the main menu bar.
        """

        menu_bar = self.menuBar()

        menu_bar.addMenu("&File")
        menu_bar.addMenu("&Help")

    def _create_tool_bar(self) -> None:
        """
        Create the main tool bar.
        """

        self._main_toolbar = QToolBar("Main Toolbar")

        self.addToolBar(self._main_toolbar)

    def _create_status_bar(self) -> None:
        """
        Create the status bar.
        """

        self._status_bar = QStatusBar()

        self._status_bar.showMessage("Ready")

        self.setStatusBar(self._status_bar)

    def _create_central_workspace(self) -> None:
        """
        Create the central workspace.
        """

        self._central_widget = QWidget()

        self._central_layout = QVBoxLayout(self._central_widget)

        welcome_label = QLabel("Welcome to Aksara Nusantara")

        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._central_layout.addWidget(welcome_label)

        self.setCentralWidget(self._central_widget)