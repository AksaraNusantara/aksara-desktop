"""
===============================================================================

Aksara Nusantara

Module:
    ui.tabs.script_explorer_tab

Module Type:
    User Interface

Purpose:
    Provides the Script Explorer reference module.

Responsibilities:
    - Display categories from the active ScriptPack.
    - Display characters from the selected category.
    - Display character metadata.
    - React to ScriptPack activation events.

The ScriptExplorerTab SHALL NOT modify ScriptPack data.

The ScriptExplorerTab SHALL NOT access ScriptPack assets
directly. All information SHALL be obtained through the
Core Engine.

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
from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QFrame,
#    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QPushButton,
)

from PySide6.QtGui import QFont

from core.engine import CoreEngine
from ui.widgets.empty_state import EmptyStateWidget


class ScriptExplorerTab(QWidget):
    """
    Script Explorer reference module.

    This widget provides a reference browser for the
    currently active ScriptPack.

    The module is presentation-only and obtains all data
    from the Core Engine.
    """

    open_home_requested = Signal()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        engine: CoreEngine,
    ) -> None:
        """
        Initialize the Script Explorer.
        """

        super().__init__()

        self._engine = engine

        self._stack: QStackedWidget | None = None

        self._empty_state: EmptyStateWidget | None = None

        self._search_box: QLineEdit | None = None

        self._dataset_list: QListWidget | None = None

        self._character_area: QWidget | None = None

        self._character_grid: QGridLayout | None = None

        self._detail_area: QWidget | None = None

        self._build_ui()

        self._engine.register_listener(
            self.refresh,
        )

        self._datasets: list[tuple[str, str]] = []

        self._characters: list[dict] = []

        self._dataset_list.currentRowChanged.connect(
            self._dataset_changed,
        )

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """
        Build the Script Explorer user interface.
        """

        self._stack = QStackedWidget()

        self._stack.addWidget(
            self._create_empty_page()
        )

        self._stack.addWidget(
            self._create_explorer_page()
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            self._stack,
        )

        self.refresh()

    def _create_empty_page(
        self,
    ) -> QWidget:
        """
        Create the empty state page.
        """

        self._empty_state = EmptyStateWidget(
            title="No ScriptPack Activated",
            description=(
                "Activate a ScriptPack from Home "
                "to explore available characters."
            ),
            action_text="Open Home",
        )

        self._empty_state.set_icon("📖")

        self._empty_state.action_requested.connect(
            self.open_home_requested.emit,
        )

        return self._empty_state

    def _create_explorer_page(
        self,
    ) -> QWidget:
        """
        Create the explorer page.

        Notes
        -----
        This method currently builds only the UI skeleton.

        TODO(AD-5):
            Populate categories from ScriptPack.

        TODO(AD-5):
            Implement character grid.

        TODO(AD-5):
            Implement details panel.

        TODO(AD-5):
            Connect Audio Service.
        """

        page = QWidget()

        root_layout = QVBoxLayout(page)

        #
        # Header
        #

        self._search_box = QLineEdit()

        self._search_box.setPlaceholderText(
            "Search..."
        )

        root_layout.addWidget(
            self._search_box,
        )

        #
        # Main splitter
        #

        splitter = QSplitter(
            Qt.Orientation.Horizontal,
        )

        #
        # Categories
        #

        left_panel = QWidget()

        left_layout = QVBoxLayout(left_panel)

        left_layout.addWidget(
            QLabel("Categories")
        )

        self._dataset_list = QListWidget()

        left_layout.addWidget(
            self._dataset_list,
        )

        #
        # Explorer
        #

        right_panel = QWidget()

        right_layout = QVBoxLayout(right_panel)

        #
        # Character Grid
        #

        self._character_area = QWidget()

        self._character_grid = QGridLayout(
            self._character_area,
        )

        self._character_grid.setSpacing(12)

        right_layout.addWidget(
            self._character_area,
            3,
        )

        #
        # Detail Area
        #

        self._detail_area = QFrame()

        self._detail_area.setFrameShape(
            QFrame.Shape.StyledPanel,
        )

        right_layout.addWidget(
            self._detail_area,
            2,
        )
        splitter.addWidget(
            left_panel,
        )

        splitter.addWidget(
            right_panel,
        )

        splitter.setStretchFactor(
            0,
            1,
        )

        splitter.setStretchFactor(
            1,
            4,
        )

        root_layout.addWidget(
            splitter,
        )

        return page

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Refresh the Script Explorer state.
        """

        if self._engine.get_active_scriptpack() is None:
            self._stack.setCurrentIndex(0)
            return

        self._stack.setCurrentIndex(1)

        self._populate_datasets()

        self._populate_character_grid()

    def _populate_datasets(self) -> None:
        """
        Populate the dataset list from the active ScriptPack.
        """

        self._dataset_list.blockSignals(True)

        self._dataset_list.clear()

        self._datasets = (
            self._engine.get_available_datasets()
        )

        current = (
            self._engine.get_current_dataset()
        )

        current_row = 0

        for row, (internal, display) in enumerate(self._datasets):

            self._dataset_list.addItem(display)

            if internal == current:
                current_row = row

        self._dataset_list.setCurrentRow(current_row)

        self._dataset_list.blockSignals(False)

    def _dataset_changed(
        self,
        row: int,
    ) -> None:
        """
        Handle dataset selection.
        """

        if row < 0:
            return

        internal, _ = self._datasets[row]

        self._engine.set_current_dataset(
            internal,
        )

        self._populate_character_grid()
        
    def _clear_character_grid(
        self,
    ) -> None:
        """
        Remove every widget from the character grid.
        """

        while self._character_grid.count():

            item = self._character_grid.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _populate_character_grid(
        self,
    ) -> None:
        """
        Populate the character grid from the current dataset.
        """

        self._clear_character_grid()

        self._characters = (
            self._engine.get_characters()
        )

        GRID_COLUMNS = 5

        for index, character in enumerate(
            self._characters
        ):

            button = QPushButton(
                character["glyph"],
            )

            button.setFont(
                QFont(
                    "Noto Sans Javanese",
                    32,
                )
            )

            button.setMinimumSize(
                72,
                72,
            )

            row = index // GRID_COLUMNS

            column = index % GRID_COLUMNS

            self._character_grid.addWidget(
                button,
                row,
                column,
            )

