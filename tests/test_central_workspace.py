"""
Tests for CentralWorkspace navigation control.

These tests validate workspace-level navigation behavior only.
No Quiz business logic is tested here.
"""

from pathlib import Path
import sys
import unittest


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QWidget

from ui.central_workspace import CentralWorkspace


class TestCentralWorkspaceNavigation(unittest.TestCase):
    """
    Test CentralWorkspace navigation locking.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Create the Qt application context."""

        cls.app = QApplication.instance()

        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self) -> None:
        """Create a real CentralWorkspace instance."""

        self.workspace = CentralWorkspace.__new__(
            CentralWorkspace,
        )

        QWidget.__init__(
            self.workspace,
        )

        self.workspace._tab_widget = QTabWidget(
            self.workspace,
        )

        self.workspace._tab_widget.addTab(
            QLabel("Home"),
            "Home",
        )

        self.workspace._tab_widget.addTab(
            QLabel("Script Explorer"),
            "Script Explorer",
        )

        self.workspace._tab_widget.addTab(
            QLabel("Flashcard"),
            "Flashcard",
        )

        self.workspace._navigation_locked = False
        self.workspace._navigation_lock_states = {}

    def tearDown(self) -> None:
        """Destroy the workspace fixture."""

        self.workspace.deleteLater()

    def test_navigation_is_unlocked_initially(self):
        """Navigation is unlocked by default."""

        self.assertFalse(
            self.workspace.navigation_locked,
        )

    def test_lock_disables_other_tabs(self):
        """Locking disables every tab except the current tab."""

        self.workspace._tab_widget.setCurrentIndex(
            2,
        )

        self.workspace.set_navigation_locked(
            True,
        )

        self.assertFalse(
            self.workspace._tab_widget.isTabEnabled(0),
        )

        self.assertFalse(
            self.workspace._tab_widget.isTabEnabled(1),
        )

        self.assertTrue(
            self.workspace._tab_widget.isTabEnabled(2),
        )

        self.assertTrue(
            self.workspace.navigation_locked,
        )

    def test_unlock_restores_tab_states(self):
        """Unlocking restores the previous enabled states."""

        self.workspace._tab_widget.setTabEnabled(
            1,
            False,
        )

        self.workspace._tab_widget.setCurrentIndex(
            2,
        )

        self.workspace.set_navigation_locked(
            True,
        )

        self.workspace.set_navigation_locked(
            False,
        )

        self.assertTrue(
            self.workspace._tab_widget.isTabEnabled(0),
        )

        self.assertFalse(
            self.workspace._tab_widget.isTabEnabled(1),
        )

        self.assertTrue(
            self.workspace._tab_widget.isTabEnabled(2),
        )

    def test_unlock_without_lock_is_safe(self):
        """Unlocking an already unlocked workspace is harmless."""

        self.workspace.set_navigation_locked(
            False,
        )

        self.assertFalse(
            self.workspace.navigation_locked,
        )

    def test_locking_twice_is_idempotent(self):
        """Repeated lock requests do not corrupt navigation state."""

        self.workspace._tab_widget.setCurrentIndex(
            1,
        )

        self.workspace.set_navigation_locked(
            True,
        )

        self.workspace.set_navigation_locked(
            True,
        )

        self.assertTrue(
            self.workspace.navigation_locked,
        )

        self.assertFalse(
            self.workspace._tab_widget.isTabEnabled(0),
        )

        self.assertTrue(
            self.workspace._tab_widget.isTabEnabled(1),
        )

        self.assertFalse(
            self.workspace._tab_widget.isTabEnabled(2),
        )

    def test_lock_preserves_active_tab(self):
        """The active tab remains enabled while navigation is locked."""

        self.workspace._tab_widget.setCurrentIndex(
            1,
        )

        self.workspace.set_navigation_locked(
            True,
        )

        self.assertEqual(
            self.workspace._tab_widget.currentIndex(),
            1,
        )

        self.assertTrue(
            self.workspace._tab_widget.isTabEnabled(1),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)