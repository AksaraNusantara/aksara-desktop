"""
===============================================================================

Aksara Nusantara

Module:
    ui.tabs.home_tab

Purpose:
    Provides the HomeTab implementation for browsing and activating
    available ScriptPacks.

Implements:
    HomeTab

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

from __future__ import annotations

# =============================================================================
# Standard Library Imports
# =============================================================================

# None

# =============================================================================
# Third-Party Imports
# =============================================================================

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# =============================================================================
# Local Application Imports
# =============================================================================

from core.engine import CoreEngine


class HomeTab(QWidget):
    """
    Home tab for ScriptPack management.

    The HomeTab allows users to:

    - Browse available ScriptPacks.
    - View ScriptPack information.
    - Activate the selected ScriptPack.

    Notes
    -----
    This class communicates only with the CoreEngine. It does not access
    the file system, ScriptPack directories, or JSON resources directly.
    """

    def __init__(
        self,
        engine: CoreEngine,
        parent: QWidget | None = None,
    ) -> None:
        """
        Initialize the HomeTab.

        Parameters
        ----------
        engine:
            Shared CoreEngine instance.

        parent:
            Parent widget.
        """
        super().__init__(parent)

        self._engine = engine

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

        self.load_scriptpacks()

    # =========================================================================
    # UI Construction
    # =========================================================================

    def _create_widgets(self) -> None:
        """
        Create all widgets used by the HomeTab.

        This method is responsible only for widget instantiation.
        Widget hierarchy, layout management, and signal connections
        are handled separately.
        """

        # =====================================================================
        # Left Panel
        # =====================================================================

        self.left_panel = QFrame(self)

        self.scriptpack_title = QLabel(
            "Available ScriptPacks",
            self.left_panel,
        )

        self.scriptpack_list = QListWidget(self.left_panel)

        # =====================================================================
        # Right Panel
        # =====================================================================

        self.right_panel = QFrame(self)

        self.information_title = QLabel(
            "ScriptPack Information",
            self.right_panel,
        )

        # ---------------------------------------------------------------------
        # ScriptPack Information
        # ---------------------------------------------------------------------

        self.name_title = QLabel("Name")
        self.name_value = QLabel("-")

        self.identifier_title = QLabel("Identifier")
        self.identifier_value = QLabel("-")

        self.version_title = QLabel("Version")
        self.version_value = QLabel("-")

        self.author_title = QLabel("Author")
        self.author_value = QLabel("-")

        self.description_title = QLabel("Description")
        self.description_value = QLabel("-")

        self.description_value.setWordWrap(True)

        # ---------------------------------------------------------------------
        # Action
        # ---------------------------------------------------------------------

        self.activate_button = QPushButton("Activate")

    def _create_layout(self) -> None:
        """
        Create and arrange all layouts for the HomeTab.

        This method is responsible only for widget placement.
        No widget creation, signal connection, or business logic
        should be performed here.
        """

        # =====================================================================
        # Main Layout
        # =====================================================================

        self.main_layout = QHBoxLayout(self)

        # =====================================================================
        # Left Panel Layout
        # =====================================================================

        self.left_layout = QVBoxLayout(self.left_panel)

        self.left_layout.addWidget(self.scriptpack_title)
        self.left_layout.addWidget(self.scriptpack_list)

        # =====================================================================
        # Information Layout
        # =====================================================================

        self.information_layout = QFormLayout()

        self.information_layout.addRow(
            self.name_title,
            self.name_value,
        )

        self.information_layout.addRow(
            self.identifier_title,
            self.identifier_value,
        )

        self.information_layout.addRow(
            self.version_title,
            self.version_value,
        )

        self.information_layout.addRow(
            self.author_title,
            self.author_value,
        )

        self.information_layout.addRow(
            self.description_title,
            self.description_value,
        )

        # =====================================================================
        # Right Panel Layout
        # =====================================================================

        self.right_layout = QVBoxLayout(self.right_panel)

        self.right_layout.addWidget(self.information_title)
        self.right_layout.addLayout(self.information_layout)
        self.right_layout.addStretch()
        self.right_layout.addWidget(
            self.activate_button,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

        # =====================================================================
        # Main Layout Composition
        # =====================================================================

        self.main_layout.addWidget(
            self.left_panel,
            stretch=1,
        )

        self.main_layout.addWidget(
            self.right_panel,
            stretch=2,
        )

    def _connect_signals(self) -> None:
        """
        Connect all widget signals.

        This method establishes all signal-slot connections used by
        the HomeTab. No business logic should be implemented here.
        """

        # =====================================================================
        # ScriptPack Selection
        # =====================================================================

        self.scriptpack_list.currentItemChanged.connect(
            self._on_selection_changed
        )

        # =====================================================================
        # Activation
        # =====================================================================

        self.activate_button.clicked.connect(
            self.activate_selected
        )

    # =========================================================================
    # Public API
    # =========================================================================

    def load_scriptpacks(self) -> None:
        """
        Load all available ScriptPacks from the CoreEngine.

        This method clears the ScriptPack list, retrieves all registered
        ScriptPacks from the CoreEngine, populates the list widget, and
        selects the first available item.
        """

        self.scriptpack_list.clear()

        for identifier in self._engine.list():

            scriptpack = self._engine.get(identifier)

            item = QListWidgetItem(
                scriptpack.metadata["name"]
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                identifier,
            )

            self.scriptpack_list.addItem(item)

        if self.scriptpack_list.count() > 0:

            self.scriptpack_list.setCurrentRow(0)

    def _refresh_ui(self) -> None:
        """
        Refresh the HomeTab user interface.

        This method synchronizes all visual components with the current
        application state.
        """

        self._refresh_list()
        self._refresh_information()
        self._refresh_button()

    def activate_selected(self) -> None:
        """
        Activate the currently selected ScriptPack.
        """
        current_item = self.scriptpack_list.currentItem()

        if current_item is None:
            return

        identifier = current_item.data(
            Qt.ItemDataRole.UserRole,
        )

        self._engine.activate(identifier)

        self._refresh_ui()

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _refresh_information(self) -> None:
        """
        Refresh the ScriptPack information panel.

        The displayed information is synchronized with the currently
        selected ScriptPack.
        """

        current_item = self.scriptpack_list.currentItem()

        if current_item is None:

            self.name_value.setText("-")
            self.identifier_value.setText("-")
            self.version_value.setText("-")
            self.author_value.setText("-")
            self.description_value.setText("-")

            return

        identifier = current_item.data(
            Qt.ItemDataRole.UserRole,
        )

        scriptpack = self._engine.get(identifier)

        metadata = scriptpack.metadata

        self.name_value.setText(
            metadata["name"]
        )

        self.identifier_value.setText(
            metadata["identifier"]
        )

        self.version_value.setText(
            metadata["version"]
        )

        self.author_value.setText(
            metadata["author"]
        )

        self.description_value.setText(
            metadata["description"]
        )

    def _refresh_button(self) -> None:
        """
        Refresh the activation button.

        The activation button reflects whether the currently selected
        ScriptPack is already active.
        """

        current_item = self.scriptpack_list.currentItem()

        if current_item is None:

            self.activate_button.setEnabled(False)
            self.activate_button.setText("Activate")

            return

        identifier = current_item.data(
            Qt.ItemDataRole.UserRole,
        )

        if self._engine.is_active(identifier):

            self.activate_button.setText("Active")
            self.activate_button.setEnabled(False)

        else:

            self.activate_button.setText("Activate")
            self.activate_button.setEnabled(True)

    def _refresh_list(self) -> None:
        """
        Refresh the ScriptPack list.

        The currently active ScriptPack is marked with a check mark to
        provide immediate visual feedback to the user.
        """

        for index in range(self.scriptpack_list.count()):

            item = self.scriptpack_list.item(index)

            if item is None:
                continue

            identifier = item.data(Qt.ItemDataRole.UserRole)

            scriptpack = self._engine.get(identifier)

            name = scriptpack.metadata["name"]

            if self._engine.is_active(identifier):
                item.setText(f"✓ {name}")
            else:
                item.setText(name)

    # =========================================================================
    # Event Handlers
    # =========================================================================

    def _on_selection_changed(
        self,
        current: QListWidgetItem | None,
        previous: QListWidgetItem | None,
    ) -> None:
        """
        Handle ScriptPack selection changes.

        Parameters
        ----------
        current:
            The newly selected ScriptPack item.

        previous:
            The previously selected ScriptPack item.
        """

        del previous

        if current is None:
            return

        self._refresh_ui()
#
#    def refresh(self) -> None:
#        """
#        Refresh the HomeTab user interface.
#
#        This method synchronizes all visual components with the current
#        application state.
#        """
#
#        self._refresh_information()
#
#        self._refresh_button()
#
#    def _refresh_list(self) -> None:
#        """
#        Refresh the ScriptPack list.
#
#        This method updates the visual state of the ScriptPack list
#        without reloading its contents.
#        """
#
#        self.scriptpack_list.viewport().update()