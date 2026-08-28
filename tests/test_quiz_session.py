"""
Contract tests for QuizSession.

QuizSession owns the domain state of one Quiz activity:
statistics, lifecycle, answer validation, and QuizResult creation.

UI concerns are intentionally excluded.
"""

from pathlib import Path
import sys
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from application.learning.quiz.quiz_difficulty import QuizDifficulty
from application.learning.quiz.quiz_question import QuizQuestion
from application.learning.quiz.quiz_session import (
    QuizSession,
    QuizSessionState,
)
from core.learning.models.payload import QuizResult


def make_question(
    correct_answer: str = "ha",
) -> QuizQuestion:
    """Create a deterministic QuizQuestion for tests."""
    return QuizQuestion(
        prompt="ꦲ",
        options=("ha", "na", "ca", "ra"),
        correct_answer=correct_answer,
    )


class TestQuizSession(unittest.TestCase):
    """Verify the QuizSession domain contract."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_initial_state(self):
        """A new session starts ACTIVE with zero statistics."""
        session = QuizSession(
            total_questions=3,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        self.assertEqual(session.total_questions, 3)
        self.assertEqual(
            session.difficulty,
            QuizDifficulty.LEVEL_1,
        )
        self.assertEqual(session.answered_questions, 0)
        self.assertEqual(session.correct_answers, 0)
        self.assertEqual(session.incorrect_answers, 0)
        self.assertIs(
            session.state,
            QuizSessionState.ACTIVE,
        )
        self.assertFalse(session.is_complete)
        self.assertFalse(session.is_cancelled)

    def test_total_questions_must_be_positive(self):
        """A session requires at least one question."""
        with self.assertRaises(ValueError):
            QuizSession(
                total_questions=0,
                difficulty=QuizDifficulty.LEVEL_1,
            )

    def test_session_preserves_difficulty(self):
        """The configured difficulty belongs to the session."""
        session = QuizSession(
            total_questions=1,
            difficulty=QuizDifficulty.LEVEL_3,
        )

        self.assertIs(
            session.difficulty,
            QuizDifficulty.LEVEL_3,
        )

    # ------------------------------------------------------------------
    # Answer processing
    # ------------------------------------------------------------------

    def test_correct_answer_is_recorded(self):
        """A correct answer returns True and updates statistics."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        result = session.answer(
            make_question(),
            "ha",
        )

        self.assertTrue(result)
        self.assertEqual(session.answered_questions, 1)
        self.assertEqual(session.correct_answers, 1)
        self.assertEqual(session.incorrect_answers, 0)

    def test_incorrect_answer_is_recorded(self):
        """An incorrect answer returns False and updates statistics."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        result = session.answer(
            make_question(),
            "na",
        )

        self.assertFalse(result)
        self.assertEqual(session.answered_questions, 1)
        self.assertEqual(session.correct_answers, 0)
        self.assertEqual(session.incorrect_answers, 1)

    def test_non_final_answer_keeps_session_active(self):
        """A non-final answer does not complete the session."""
        session = QuizSession(
            total_questions=3,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        session.answer(
            make_question(),
            "ha",
        )

        self.assertEqual(session.answered_questions, 1)
        self.assertFalse(session.is_complete)
        self.assertFalse(session.is_cancelled)
        self.assertIs(
            session.state,
            QuizSessionState.ACTIVE,
        )

    def test_final_answer_completes_session(self):
        """The final answer transitions ACTIVE to COMPLETED."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        question = make_question()

        session.answer(question, "ha")
        self.assertFalse(session.is_complete)

        session.answer(question, "na")

        self.assertEqual(session.answered_questions, 2)
        self.assertTrue(session.is_complete)
        self.assertFalse(session.is_cancelled)
        self.assertIs(
            session.state,
            QuizSessionState.COMPLETED,
        )

    def test_multiple_answers_accumulate_statistics(self):
        """Statistics represent all answers in the session."""
        session = QuizSession(
            total_questions=3,
            difficulty=QuizDifficulty.LEVEL_2,
        )

        question = make_question()

        session.answer(question, "ha")
        session.answer(question, "na")
        session.answer(question, "ca")

        self.assertEqual(session.answered_questions, 3)
        self.assertEqual(session.correct_answers, 1)
        self.assertEqual(session.incorrect_answers, 2)
        self.assertTrue(session.is_complete)

    def test_invalid_selected_answer_is_rejected(self):
        """An answer outside the question options is rejected."""
        session = QuizSession(
            total_questions=1,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        with self.assertRaises(ValueError):
            session.answer(
                make_question(),
                "invalid",
            )

        self.assertEqual(session.answered_questions, 0)
        self.assertEqual(session.correct_answers, 0)
        self.assertEqual(session.incorrect_answers, 0)
        self.assertIs(
            session.state,
            QuizSessionState.ACTIVE,
        )

    def test_answer_cannot_exceed_question_limit(self):
        """A completed question quota cannot be exceeded."""
        session = QuizSession(
            total_questions=1,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        question = make_question()

        session.answer(question, "ha")

        with self.assertRaises(RuntimeError):
            session.answer(question, "ha")

    def test_completed_session_cannot_accept_answer(self):
        """A completed session rejects further answers."""
        session = QuizSession(
            total_questions=1,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        session.answer(
            make_question(),
            "ha",
        )

        self.assertIs(
            session.state,
            QuizSessionState.COMPLETED,
        )

        with self.assertRaises(RuntimeError):
            session.answer(
                make_question(),
                "ha",
            )

    # ------------------------------------------------------------------
    # Cancellation
    # ------------------------------------------------------------------

    def test_cancel_transitions_active_to_cancelled(self):
        """Cancelling an active session enters CANCELLED."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        session.cancel()

        self.assertTrue(session.is_cancelled)
        self.assertFalse(session.is_complete)
        self.assertIs(
            session.state,
            QuizSessionState.CANCELLED,
        )

    def test_cancelled_session_cannot_accept_answer(self):
        """A cancelled session rejects answers."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        session.cancel()

        with self.assertRaises(RuntimeError):
            session.answer(
                make_question(),
                "ha",
            )

    def test_cancelled_session_cannot_build_result(self):
        """A cancelled session cannot produce a QuizResult."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        session.cancel()

        with self.assertRaises(RuntimeError):
            session.build_result()

    def test_completed_session_cannot_be_cancelled(self):
        """A completed session cannot transition to CANCELLED."""
        session = QuizSession(
            total_questions=1,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        session.answer(
            make_question(),
            "ha",
        )

        with self.assertRaises(RuntimeError):
            session.cancel()

        self.assertTrue(session.is_complete)
        self.assertIs(
            session.state,
            QuizSessionState.COMPLETED,
        )

    def test_cancelled_session_cannot_be_cancelled_again(self):
        """Cancellation is only valid from ACTIVE."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        session.cancel()

        with self.assertRaises(RuntimeError):
            session.cancel()

        self.assertTrue(session.is_cancelled)

    # ------------------------------------------------------------------
    # Result
    # ------------------------------------------------------------------

    def test_build_result_requires_completed_session(self):
        """A non-completed session cannot build a result."""
        session = QuizSession(
            total_questions=1,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        with self.assertRaises(RuntimeError):
            session.build_result()

    def test_build_result_returns_quiz_result(self):
        """A completed session produces a QuizResult."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_2,
        )

        question = make_question()

        session.answer(question, "ha")
        session.answer(question, "na")

        result = session.build_result()

        self.assertIsInstance(
            result,
            QuizResult,
        )

    def test_build_result_preserves_statistics(self):
        """QuizResult contains the final session statistics."""
        session = QuizSession(
            total_questions=3,
            difficulty=QuizDifficulty.LEVEL_3,
        )

        question = make_question()

        session.answer(question, "ha")
        session.answer(question, "na")
        session.answer(question, "ca")

        result = session.build_result()

        self.assertEqual(result.total_questions, 3)
        self.assertEqual(result.correct_answers, 1)
        self.assertEqual(result.incorrect_answers, 2)

    def test_build_result_preserves_difficulty(self):
        """QuizResult contains the session difficulty."""
        session = QuizSession(
            total_questions=1,
            difficulty=QuizDifficulty.LEVEL_3,
        )

        session.answer(
            make_question(),
            "ha",
        )

        result = session.build_result()

        self.assertEqual(
            result.difficulty_level,
            QuizDifficulty.LEVEL_3.value,
        )

    # ------------------------------------------------------------------
    # Result stability
    # ------------------------------------------------------------------

    def test_build_result_is_consistent_for_completed_session(self):
        """Repeated result creation reflects the same completed state."""
        session = QuizSession(
            total_questions=2,
            difficulty=QuizDifficulty.LEVEL_1,
        )

        question = make_question()

        session.answer(question, "ha")
        session.answer(question, "na")

        first = session.build_result()
        second = session.build_result()

        self.assertEqual(
            first.total_questions,
            second.total_questions,
        )
        self.assertEqual(
            first.correct_answers,
            second.correct_answers,
        )
        self.assertEqual(
            first.incorrect_answers,
            second.incorrect_answers,
        )
        self.assertIs(
            first.difficulty_level,
            second.difficulty_level,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
