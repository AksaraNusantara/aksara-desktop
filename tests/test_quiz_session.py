"""
Tests for QuizSession.

QuizSession manages temporary Quiz activity state and produces
QuizResult when the Quiz is completed.
"""

from pathlib import Path
import sys
import unittest


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from application.learning.quiz.quiz_question import QuizQuestion
from application.learning.quiz.quiz_session import QuizSession
from core.learning.models.payload import QuizResult

from application.learning.quiz.quiz_session import (
    QuizSession,
    QuizSessionState,
)


class TestQuizSession(unittest.TestCase):
    """Test QuizSession behavior."""

    def setUp(self) -> None:
        """Create a standard QuizQuestion."""

        self.question = QuizQuestion(
            prompt="ꦲ",
            correct_answer="ha",
            options=(
                "ha",
                "na",
                "ca",
                "ra",
            ),
        )

    def test_initial_state(self):
        """A new QuizSession starts without answers."""

        session = QuizSession(
            total_questions=10,
        )

        self.assertEqual(
            session.total_questions,
            10,
        )

        self.assertEqual(
            session.answered_questions,
            0,
        )

        self.assertEqual(
            session.correct_answers,
            0,
        )

        self.assertEqual(
            session.incorrect_answers,
            0,
        )

        self.assertFalse(
            session.is_complete,
        )

    def test_correct_answer(self):
        """A correct answer increments the correct count."""

        session = QuizSession(
            total_questions=1,
        )

        result = session.answer(
            self.question,
            "ha",
        )

        self.assertTrue(
            result,
        )

        self.assertEqual(
            session.answered_questions,
            1,
        )

        self.assertEqual(
            session.correct_answers,
            1,
        )

        self.assertEqual(
            session.incorrect_answers,
            0,
        )

        self.assertTrue(
            session.is_complete,
        )

    def test_incorrect_answer(self):
        """An incorrect answer increments the incorrect count."""

        session = QuizSession(
            total_questions=1,
        )

        result = session.answer(
            self.question,
            "na",
        )

        self.assertFalse(
            result,
        )

        self.assertEqual(
            session.answered_questions,
            1,
        )

        self.assertEqual(
            session.correct_answers,
            0,
        )

        self.assertEqual(
            session.incorrect_answers,
            1,
        )

    def test_multiple_answers(self):
        """Multiple answers accumulate correctly."""

        session = QuizSession(
            total_questions=3,
        )

        session.answer(
            self.question,
            "ha",
        )

        session.answer(
            self.question,
            "na",
        )

        session.answer(
            self.question,
            "ha",
        )

        self.assertEqual(
            session.answered_questions,
            3,
        )

        self.assertEqual(
            session.correct_answers,
            2,
        )

        self.assertEqual(
            session.incorrect_answers,
            1,
        )

        self.assertTrue(
            session.is_complete,
        )

    def test_invalid_selected_answer_is_rejected(self):
        """Selected answer must be one of the available options."""

        session = QuizSession(
            total_questions=1,
        )

        with self.assertRaises(ValueError):
            session.answer(
                self.question,
                "invalid",
            )

    def test_cannot_answer_completed_session(self):
        """A completed QuizSession cannot accept another answer."""

        session = QuizSession(
            total_questions=1,
        )

        session.answer(
            self.question,
            "ha",
        )

        with self.assertRaises(RuntimeError):
            session.answer(
                self.question,
                "na",
            )

    def test_result_cannot_be_built_before_completion(self):
        """QuizResult requires a completed QuizSession."""

        session = QuizSession(
            total_questions=2,
        )

        with self.assertRaises(RuntimeError):
            session.build_result()

    def test_build_result(self):
        """Completed QuizSession produces QuizResult."""

        session = QuizSession(
            total_questions=2,
        )

        session.answer(
            self.question,
            "ha",
        )

        session.answer(
            self.question,
            "na",
        )

        result = session.build_result()

        self.assertIsInstance(
            result,
            QuizResult,
        )

        self.assertEqual(
            result.total_questions,
            2,
        )

        self.assertEqual(
            result.correct_answers,
            1,
        )

        self.assertEqual(
            result.incorrect_answers,
            1,
        )

    def test_invalid_total_questions_is_rejected(self):
        """QuizSession requires at least one question."""

        with self.assertRaises(ValueError):
            QuizSession(
                total_questions=0,
            )

    def test_initial_state_is_active(self):
        """A newly created QuizSession is active."""

        session = QuizSession(
            total_questions=1,
        )

        self.assertIs(
            session.state,
            QuizSessionState.ACTIVE,
        )


    def test_completed_state(self):
        """Answering the final question completes the session."""

        session = QuizSession(
            total_questions=1,
        )

        session.answer(
            self.question,
            "ha",
        )

        self.assertIs(
            session.state,
            QuizSessionState.COMPLETED,
        )


    def test_cancelled_state(self):
        """An active QuizSession can be cancelled."""

        session = QuizSession(
            total_questions=2,
        )

        session.cancel()

        self.assertIs(
            session.state,
            QuizSessionState.CANCELLED,
        )

        self.assertTrue(
            session.is_cancelled,
        )


    def test_cancelled_session_cannot_build_result(self):
        """A cancelled QuizSession cannot produce QuizResult."""

        session = QuizSession(
            total_questions=2,
        )

        session.cancel()

        with self.assertRaises(RuntimeError):
            session.build_result()


    def test_cancelled_session_cannot_accept_answer(self):
        """A cancelled QuizSession cannot accept answers."""

        session = QuizSession(
            total_questions=2,
        )

        session.cancel()

        with self.assertRaises(RuntimeError):
            session.answer(
                self.question,
                "ha",
            )


    def test_completed_session_cannot_be_cancelled(self):
        """A completed QuizSession cannot be cancelled."""

        session = QuizSession(
            total_questions=1,
        )

        session.answer(
            self.question,
            "ha",
        )

        with self.assertRaises(RuntimeError):
            session.cancel()


if __name__ == "__main__":
    unittest.main(verbosity=2)