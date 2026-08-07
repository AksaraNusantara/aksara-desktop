"""
===============================================================================

Aksara Nusantara

Module:
    ui.tabs.flashcard_tab

Module Type:
    User Interface

Purpose:
    Provides the Flashcard learning module.

Responsibilities:
    - Display characters from the active ScriptPack.
    - Navigate through character definitions.
    - Present learning information.
    - React to ScriptPack activation events.

The FlashcardTab SHALL NOT access ScriptPack assets directly.
All character data SHALL be obtained through the Core Engine.

References:
    APPLICATION_ARCHITECTURE.md

    docs/governance/ENGINEERING_PRINCIPLES.md

    docs/standards/PYTHON_MODULE_TEMPLATE.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtGui import QKeyEvent
from PySide6.QtGui import QMouseEvent

from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QSizePolicy

from core.engine import CoreEngine

from ui.widgets.learning_module import LearningModule


class FlashcardTab(LearningModule):
    """
    Flashcard learning module.

    This class displays the characters provided by the
    currently active ScriptPack.
    """

    def __init__(
        self,
        engine: CoreEngine,
        session: FlashcardSession,
    ) -> None:
        """
        Initialize the Flashcard module.

        Parameters
        ----------
        engine:
            Shared Core Engine instance.
        session:
            FlashcardSession
        """

        self._session = session

        self._script_value: QLabel | None = None

        self._category_value: QLabel | None = None

        self._lesson_selector: QComboBox | None = None

        self._glyph_label: QLabel | None = None

        self._latin_label: QLabel | None = None

        self._description_label: QLabel | None = None

        self._progress_label: QLabel | None = None

        self._listen_button: QPushButton | None = None

        self._previous_button: QPushButton | None = None

        self._next_button: QPushButton | None = None

        super().__init__(
            engine,
            "Flashcard",
        )

        self._session.register_listener(
            self._refresh_ui,
        )

        self._lesson_selector.currentIndexChanged.connect(
            self._lesson_changed,
        )

        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus,
        )

    def _create_content_page(
        self,
    ) -> QWidget:
        """
        Create the Flashcard content page.

        Returns
        -------
        QWidget
            Flashcard content widget.
        """

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.setContentsMargins(
            40,
            30,
            40,
            30,
        )

        layout.setSpacing(20)

        header_layout = QGridLayout()

        header_layout.addWidget(
            QLabel("Current Script"),
            0,
            0,
        )

        self._script_value = QLabel("-")

        header_layout.addWidget(
            self._script_value,
            0,
            1,
        )

        header_layout.addWidget(
            QLabel("Lesson"),
            1,
            0,
        )

        self._lesson_selector = QComboBox()

        header_layout.addWidget(
            self._lesson_selector,
            1,
            1,
        )

        header_layout.setColumnStretch(
            1,
            1,
        )

        layout.addLayout(
            header_layout,
        )

        layout.addStretch()

        self._glyph_label = QLabel()

        self._glyph_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )

        self._glyph_label.setFont(
            QFont(
                "Noto Sans Javanese",
                84,
            )
        )

        layout.addWidget(
            self._glyph_label,
        )

        self._latin_label = QLabel()

        self._latin_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )

        latin_font = QFont()

        latin_font.setPointSize(
            18,
        )

        latin_font.setBold(
            True,
        )

        self._latin_label.setFont(
            latin_font,
        )

        layout.addWidget(
            self._latin_label,
        )

        self._description_label = QLabel()

        self._description_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )

        self._description_label.setWordWrap(
            True,
        )

#        self._description_label.setMaximumWidth(
#            520,
#        )
        self._description_label.setMinimumHeight(80)

        layout.addWidget(
            self._description_label,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        layout.addStretch()

        self._listen_button = QPushButton(
            "🔊 Listen",
        )

        self._listen_button.setEnabled(
            False,
        )

        self._listen_button.setMinimumWidth(
            160,
        )

        self._listen_button.setToolTip(
            (
                "Audio support is not available "
                "for the current ScriptPack."
            )
        )

        layout.addWidget(
            self._listen_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        navigation_layout = QHBoxLayout()

        self._previous_button = QPushButton(
            "◀ Previous",
        )

        self._next_button = QPushButton(
            "Next ▶",
        )

        self._previous_button.setMinimumWidth(
            120,
        )

        self._next_button.setMinimumWidth(
            120,
        )

        self._previous_button.clicked.connect(
            self._show_previous,
        )

        self._next_button.clicked.connect(
            self._show_next,
        )

        navigation_layout.addWidget(
            self._previous_button,
        )

        navigation_layout.addStretch()

        navigation_layout.addWidget(
            self._next_button,
        )

        layout.addLayout(
            navigation_layout,
        )

        self._progress_label = QLabel()

        self._progress_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )

        layout.addWidget(
            self._progress_label,
        )

        layout.addStretch()

        return page

    def on_scriptpack_activated(
        self,
    ) -> None:
        """
        Refresh the Flashcard after a ScriptPack
        has been activated.
        """
        self._session.start()

    def _refresh_ui(
        self,
    ) -> None:
        """
        Refresh the current Flashcard.
        """

        if self._session.count() == 0:
            return

        scriptpack = (
            self._engine.get_active_scriptpack()
        )

        if scriptpack is None:
            return

        character = self._session.current()

        self._script_value.setText(
            scriptpack.metadata["name"]
        )

        self._lesson_selector.blockSignals(True)

        self._lesson_selector.setCurrentText(
            self._engine.get_current_dataset_display_name()
        )

        self._lesson_selector.blockSignals(False)

        self._glyph_label.setText(
            character["glyph"]
        )

        self._latin_label.setText(
            character["latin"].capitalize()
        )

        self._description_label.setWordWrap(True)

        self._description_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        
        self._description_label.setText(
            character["description"]
        )

        self._progress_label.setText(
            (
                f"Character "
                f"{self._session.index() + 1}"
                f" of "
                f"{self._session.count()}"
            )
        )

        self._update_navigation()

    def _update_navigation(
        self,
    ) -> None:
        """
        Update the navigation buttons.
        """

        self._previous_button.setEnabled(
            self._session.has_previous()
        )

        self._next_button.setEnabled(
            self._session.has_next()
        )

    def _show_previous(
        self,
    ) -> None:
        """
        Display the previous character.
        """
        self._session.previous()

    def _show_next(
        self,
    ) -> None:
        """
        Display the next character.
        """
        self._session.next()

    def keyPressEvent(
        self,
        event: QKeyEvent,
    ) -> None:
        """
        Handle keyboard navigation.

        Parameters
        ----------
        event:
            Key press event.
        """

        match event.key():

            case Qt.Key.Key_Left:
                self._show_previous()

            case Qt.Key.Key_Right:
                self._show_next()

            case _:
                super().keyPressEvent(
                    event,
                )

    def mousePressEvent(
        self,
        event: QMouseEvent,
    ) -> None:
        """
        Acquire keyboard focus when the user
        clicks inside the Flashcard module.
        """

        self.setFocus()

        super().mousePressEvent(
            event,
        )

    def _lesson_changed(
        self,
        index: int,
    ) -> None:
        """
        Handle lesson selection.
        """

        if index < 0:
            return

        dataset = (
            self._lesson_selector.currentData()
        )

        self._engine.set_current_dataset(
            dataset,
        )

        self._session.start()