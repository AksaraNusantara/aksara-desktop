"""Tests for Active Learner propagation in CentralWorkspace."""

from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
)

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.learning.models.learner_identity import LearnerIdentity
from ui.central_workspace import CentralWorkspace


class FakeQuizTab(QWidget):
    """Minimal QWidget-compatible QuizTab test double."""

    open_home_requested = Signal()
    quiz_started = Signal()
    quiz_cancelled = Signal()
    quiz_finished = Signal()

    def refresh(self):
        """Minimal refresh hook used by CentralWorkspace."""
        pass


class TestCentralWorkspaceLearner(unittest.TestCase):
    """Test Active Learner propagation to QuizTab."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_active_learner_is_passed_to_quiz_tab(self):
        """CentralWorkspace passes Active Learner to QuizTab."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
            is_guest=False,
        )

        engine = MagicMock()
        audio = MagicMock()
        flashcard_session = MagicMock()
        learning_service = MagicMock()

        quiz_tab = QWidget()

        fake_quiz_tab = FakeQuizTab()

        with patch(
            "ui.central_workspace.QuizTab",
            return_value=fake_quiz_tab,
        ) as quiz_tab_class:

            CentralWorkspace(
                engine=engine,
                audio=audio,
                flashcard_session=flashcard_session,
                learning_service=learning_service,
                active_learner=learner,
            )

        quiz_tab_class.assert_called_once()

        kwargs = quiz_tab_class.call_args.kwargs

        self.assertEqual(
            kwargs["learner_id"],
            "learner-001",
        )

        self.assertEqual(
            kwargs["learner_display_name"],
            "Budi",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
