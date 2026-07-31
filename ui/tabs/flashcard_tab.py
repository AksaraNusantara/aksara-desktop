"""
===============================================================================

Aksara Nusantara

Module:
    ui.tabs.flashcard_tab

Module Type:
    User Interface

Purpose:
    Provides the Flashcard learning interface.

Responsibilities:
    - Display characters provided by the Core Engine.
    - Navigate between available characters.
    - Present character information.

The FlashcardTab SHALL NOT implement business logic.

All character data SHALL be retrieved through the Core Engine.

References:
    APPLICATION_ARCHITECTURE.md

    docs/standards/PYTHON_MODULE_TEMPLATE.md

    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

# =============================================================================
# Standard Library
# =============================================================================

from __future__ import annotations

# =============================================================================
# Third-party Packages
# =============================================================================

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from PySide6.QtGui import QFont

# =============================================================================
# Local Project Imports
# =============================================================================

from core.engine import CoreEngine



# =============================================================================
# FlashcardTab
# =============================================================================

class FlashcardTab(QWidget):
    """
    Flashcard learning interface.

    The FlashcardTab presents characters supplied by the
    Core Engine.

    The widget SHALL NOT access ScriptPack assets directly.
    """

    def __init__(
        self,
        engine: CoreEngine,
    ) -> None:
        """
        Initialize the Flashcard tab.

        Parameters
        ----------
        engine:
            Shared Core Engine instance.
        """

        super().__init__()

        self._engine = engine

        self._characters: list[dict] = []

        self._current_index = 0

        self._glyph_label: QLabel | None = None
        self._latin_label: QLabel | None = None
        self._unicode_label: QLabel | None = None
        self._description_label: QLabel | None = None
        self._counter_label: QLabel | None = None

        self._previous_button: QPushButton | None = None
        self._next_button: QPushButton | None = None

        self._initialize_ui()

        self._load_characters()

        self._show_current_character()

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def _initialize_ui(
        self,
    ) -> None:
        """
        Initialize the Flashcard user interface.
        """

        root_layout = QVBoxLayout(self)

        root_layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        root_layout.setSpacing(20)

        #
        # Character Glyph
        #

        self._glyph_label = QLabel()

        self._glyph_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self._glyph_label = QLabel()

        self._glyph_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        font = QFont(
            "Noto Sans Javanese",
            72,
        )

        self._glyph_label.setFont(font)

        root_layout.addWidget(
            self._glyph_label
        )

        #
        # Latin
        #

        self._latin_label = QLabel()

        self._latin_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self._latin_label.setStyleSheet(
            """
            font-size:22pt;
            font-weight:bold;
            """
        )

        root_layout.addWidget(
            self._latin_label
        )

        #
        # Unicode
        #

        self._unicode_label = QLabel()

        self._unicode_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        root_layout.addWidget(
            self._unicode_label
        )

        #
        # Description
        #

        self._description_label = QLabel()

        self._description_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self._description_label.setWordWrap(True)

        root_layout.addWidget(
            self._description_label
        )

        root_layout.addStretch()

        #
        # Footer
        #

        footer_layout = QHBoxLayout()

        self._previous_button = QPushButton(
            "◀ Previous"
        )

        self._counter_label = QLabel()

        self._counter_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self._next_button = QPushButton(
            "Next ▶"
        )

        footer_layout.addWidget(
            self._previous_button
        )

        footer_layout.addStretch()

        footer_layout.addWidget(
            self._counter_label
        )

        footer_layout.addStretch()

        footer_layout.addWidget(
            self._next_button
        )

        root_layout.addLayout(
            footer_layout
        )

        self._previous_button.clicked.connect(
            self._previous_character
        )

        self._next_button.clicked.connect(
            self._next_character
        )

    # -------------------------------------------------------------------------
    # Data
    # -------------------------------------------------------------------------

    def _load_characters(self) -> None:
        """
        Load character data from the Core Engine.

        Raises
        ------
        RuntimeError
            If the requested ScriptPack contains no characters.
        """

        self._characters = self._engine.get_characters(
            "javanese"
        )

        if not self._characters:
            raise RuntimeError(
                "The Javanese ScriptPack contains no characters."
            )

    # -------------------------------------------------------------------------
    # Presentation
    # -------------------------------------------------------------------------

    def _show_current_character(self) -> None:
        """
        Display the currently selected character.
        """

        if not self._characters:
            return

        character = self._characters[self._current_index]

        assert self._glyph_label is not None
        assert self._latin_label is not None
        assert self._unicode_label is not None
        assert self._description_label is not None
        assert self._counter_label is not None

        self._glyph_label.setText(
            character["glyph"]
        )

        self._latin_label.setText(
            character["latin"]
        )

        self._unicode_label.setText(
            character["unicode"]
        )

        self._description_label.setText(
            character["description"]
        )

        self._counter_label.setText(
            f"{self._current_index + 1} / {len(self._characters)}"
        )

        self._update_navigation()

    # -------------------------------------------------------------------------
    # Navigation
    # -------------------------------------------------------------------------

    def _next_character(self) -> None:
        """
        Display the next character.
        """

        if self._current_index >= len(self._characters) - 1:
            return

        self._current_index += 1

        self._show_current_character()

    def _previous_character(self) -> None:
        """
        Display the previous character.
        """

        if self._current_index <= 0:
            return

        self._current_index -= 1

        self._show_current_character()

    def _update_navigation(self) -> None:
        """
        Update navigation button states.
        """

        assert self._previous_button is not None
        assert self._next_button is not None

        self._previous_button.setEnabled(
            self._current_index > 0
        )

        self._next_button.setEnabled(
            self._current_index < len(self._characters) - 1
        )