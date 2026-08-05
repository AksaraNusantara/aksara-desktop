"""
===============================================================================

Aksara Nusantara

Module:
    ui.widgets.learning_module

Module Type:
    User Interface

Purpose:
    Base class for all learning modules.

Responsibilities:
    - Check active ScriptPack state.
    - Display placeholder when no ScriptPack is active.
    - Display learning content when a ScriptPack is active.

===============================================================================
"""

from __future__ import annotations

from PySide6.QtCore import (
    Signal,
    Qt,
)
from PySide6.QtWidgets import (
#    QLabel,
#    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from core.engine import CoreEngine
from ui.widgets.empty_state import EmptyStateWidget


class LearningModule(QWidget):
    """
    Base widget for every learning module.
    """

    open_home_requested = Signal()

    def __init__(
        self,
        engine: CoreEngine,
        module_name: str,
    ) -> None:
        """
        Initialize the learning module.
        """
        super().__init__()

        self._engine = engine
        self._module_name = module_name

        self._stack = QStackedWidget(self)

        self._placeholder_page = self._create_placeholder_page()
        self._content_page = self._create_content_page()

        self._stack.addWidget(self._placeholder_page)
        self._stack.addWidget(self._content_page)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._stack)

        self._engine.register_listener(
            self.refresh,
        )

        self.refresh()

    def refresh(self) -> None:
        """
        Refresh the module state.
        """
        if self.has_active_scriptpack():
            self._stack.setCurrentWidget(self._content_page)
            self.on_scriptpack_activated()
        else:
            self._stack.setCurrentWidget(self._placeholder_page)

    def has_active_scriptpack(self) -> bool:
        """
        Return True if a ScriptPack is active.
        """
        return self._engine.get_active_scriptpack() is not None

    def content_widget(self) -> QWidget:
        """
        Return the content widget.
        """
        return self._content_page

    def _create_placeholder_page(self) -> QWidget:
        """
        Create the placeholder page displayed when no
        ScriptPack is active.
        """

        page = EmptyStateWidget(
            title=self._module_name,
            description=(
                "No ScriptPack is currently active.\n\n"
                "Please activate a ScriptPack from the Home tab "
                "before using this learning module."
            ),
            action_text="Open Home",
        )

        page.action_requested.connect(
            self.open_home_requested.emit,
        )

        return page

    def _create_content_page(self) -> QWidget:
        """
        Create the learning content page.

        Subclasses must override this method.
        """

        raise NotImplementedError(
            "_create_content_page() must be implemented "
            "by subclasses."
        )

    def on_scriptpack_activated(self) -> None:
        """
        Called after a ScriptPack becomes active.

        Subclasses may override.
        """
        return
