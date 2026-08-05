"""
empty_state.py
==============

Reusable empty state widget for Aksara Nusantara Desktop.

This widget provides a consistent user interface for modules that
cannot operate because a required prerequisite has not been fulfilled,
such as the absence of an active ScriptPack.

The widget is intentionally presentation-only. It does not contain
business logic, application state, or navigation logic. Instead, it
emits a Qt signal when the action button is pressed, allowing the
owning module to decide how the request should be handled.

Typical use cases
-----------------
- Flashcard module
- Script Explorer
- Quiz (future)
- Transliteration (future)

Design Principles
-----------------
- Reusable presentation component
- No dependency on Core Engine
- No dependency on ScriptPack
- No dependency on MainWindow
- Signal-based communication
- Theme-friendly styling

Copyright
---------
Aksara Nusantara Project
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class EmptyStateWidget(QWidget):
    """
    A reusable widget for displaying an application's empty state.

    The widget presents a title, description, optional illustration,
    and a single primary action button. It is intended for modules
    that cannot continue until a prerequisite has been satisfied.

    The widget itself performs no application-specific actions.
    Instead, it emits the ``action_requested`` signal when the user
    presses the action button, allowing the parent widget to handle
    the request appropriately.

    Signals
    -------
    action_requested
        Emitted when the primary action button is clicked.

    Notes
    -----
    This widget belongs to the presentation layer and should never
    access business logic directly.
    """

    action_requested = Signal()

    def __init__(
        self,
        title: str,
        description: str,
        action_text: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._build_ui(title, description, action_text)

    def _build_ui(
        self,
        title: str,
        description: str,
        action_text: str,
    ) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        # ------------------------------------------------------------------
        # Icon / Illustration
        # ------------------------------------------------------------------

        self.icon_label = QLabel("📚")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet(
            "font-size: 56px;"
        )

        # ------------------------------------------------------------------
        # Title
        # ------------------------------------------------------------------

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet(
            "font-size: 22px; font-weight: 600;"
        )

        # ------------------------------------------------------------------
        # Description
        # ------------------------------------------------------------------

        self.description_label = QLabel(description)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        self.description_label.setMaximumWidth(520)

        # ------------------------------------------------------------------
        # Action Button
        # ------------------------------------------------------------------

        self.action_button = QPushButton(action_text)
        self.action_button.setMinimumWidth(180)
        self.action_button.clicked.connect(
            self.action_requested.emit
        )

        layout.addStretch()
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addSpacing(8)
        layout.addWidget(
            self.action_button,
            alignment=Qt.AlignCenter,
        )
        layout.addStretch()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_title(self, text: str) -> None:
        self.title_label.setText(text)

    def set_description(self, text: str) -> None:
        self.description_label.setText(text)

    def set_action_text(self, text: str) -> None:
        self.action_button.setText(text)

    def set_action_visible(self, visible: bool) -> None:
        self.action_button.setVisible(visible)

    def set_icon(self, text: str) -> None:
        """
        Set a simple emoji/text icon.

        Later this can be upgraded to support QPixmap
        without changing the public API.
        """
        self.icon_label.setText(text)