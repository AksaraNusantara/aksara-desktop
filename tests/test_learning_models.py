"""
Tests for Learning Engine domain models.

Architecture references:
    AD-LE-001 — LearningProfile is a derived aggregate.
    AD-LE-002 — StudySession represents a completed activity.
    AD-LE-004 — Activity Classification identifies activity type.
    AD-LE-005 — Payload is associated with an activity classification.
"""

from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest


# ---------------------------------------------------------------------------
# Project path
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ---------------------------------------------------------------------------
# Learning Engine imports
# ---------------------------------------------------------------------------

from core.learning.models.activity import ActivityType
from core.learning.models.learning_profile import LearningProfile
from core.learning.models.payload import QuizResult
from core.learning.models.study_session import StudySession


class TestQuizResult(unittest.TestCase):
    """Test QuizResult domain model."""

    def test_valid_quiz_result(self):
        """A valid QuizResult can be created."""

        result = QuizResult(
            total_questions=10,
            correct_answers=8,
            incorrect_answers=2,
        )

        self.assertEqual(result.total_questions, 10)
        self.assertEqual(result.correct_answers, 8)
        self.assertEqual(result.incorrect_answers, 2)
        self.assertIs(result.activity_type, ActivityType.QUIZ)

    def test_invalid_answer_total(self):
        """Correct and incorrect answers must equal total questions."""

        with self.assertRaises(ValueError):
            QuizResult(
                total_questions=10,
                correct_answers=8,
                incorrect_answers=1,
            )

    def test_negative_values(self):
        """QuizResult must reject negative values."""

        with self.assertRaises(ValueError):
            QuizResult(
                total_questions=-1,
                correct_answers=0,
                incorrect_answers=0,
            )


class TestStudySession(unittest.TestCase):
    """Test StudySession domain model."""

    def _create_quiz_result(self):
        """Create a valid QuizResult for StudySession tests."""

        return QuizResult(
            total_questions=10,
            correct_answers=7,
            incorrect_answers=3,
        )

    def test_valid_study_session(self):
        """A valid Quiz StudySession can be created."""

        result = self._create_quiz_result()
        timestamp = datetime.now(timezone.utc)

        session = StudySession(
            session_id="session-001",
            timestamp=timestamp,
            activity_type=ActivityType.QUIZ,
            payload=result,
        )

        self.assertEqual(session.session_id, "session-001")
        self.assertEqual(session.timestamp, timestamp)
        self.assertIs(session.activity_type, ActivityType.QUIZ)
        self.assertIs(session.payload, result)

    def test_empty_session_id(self):
        """StudySession requires a non-empty session identifier."""

        with self.assertRaises(ValueError):
            StudySession(
                session_id="",
                timestamp=datetime.now(timezone.utc),
                activity_type=ActivityType.QUIZ,
                payload=self._create_quiz_result(),
            )

    def test_none_payload(self):
        """StudySession requires a payload."""

        with self.assertRaises(ValueError):
            StudySession(
                session_id="session-003",
                timestamp=datetime.now(timezone.utc),
                activity_type=ActivityType.QUIZ,
                payload=None,
            )


class TestLearningProfile(unittest.TestCase):
    """Test LearningProfile domain model."""

    def test_default_profile(self):
        """A new LearningProfile starts with empty aggregate values."""

        profile = LearningProfile(
            learner_id="learner-001",
        )

        self.assertEqual(profile.learner_id, "learner-001")
        self.assertEqual(profile.total_sessions, 0)
        self.assertEqual(profile.total_questions, 0)
        self.assertEqual(profile.correct_answers, 0)
        self.assertEqual(profile.incorrect_answers, 0)
        self.assertIsNone(profile.last_activity)

    def test_valid_aggregate(self):
        """LearningProfile accepts a valid aggregated state."""

        timestamp = datetime.now(timezone.utc)

        profile = LearningProfile(
            learner_id="learner-001",
            total_sessions=3,
            total_questions=30,
            correct_answers=24,
            incorrect_answers=6,
            last_activity=timestamp,
        )

        self.assertEqual(profile.total_sessions, 3)
        self.assertEqual(profile.total_questions, 30)
        self.assertEqual(profile.correct_answers, 24)
        self.assertEqual(profile.incorrect_answers, 6)
        self.assertEqual(profile.last_activity, timestamp)

    def test_invalid_answer_total(self):
        """LearningProfile rejects an impossible aggregate."""

        with self.assertRaises(ValueError):
            LearningProfile(
                learner_id="learner-001",
                total_questions=10,
                correct_answers=8,
                incorrect_answers=5,
            )

    def test_negative_values(self):
        """LearningProfile rejects negative aggregate values."""

        with self.assertRaises(ValueError):
            LearningProfile(
                learner_id="learner-001",
                total_sessions=-1,
            )

    def test_empty_learner_id(self):
        """LearningProfile requires a learner identifier."""

        with self.assertRaises(ValueError):
            LearningProfile(
                learner_id="",
            )


class TestDomainModelImmutability(unittest.TestCase):
    """Test immutability of Learning Engine domain models."""

    def test_quiz_result_is_immutable(self):
        """QuizResult cannot be modified after creation."""

        result = QuizResult(
            total_questions=10,
            correct_answers=8,
            incorrect_answers=2,
        )

        with self.assertRaises(AttributeError):
            result.correct_answers = 9

    def test_study_session_is_immutable(self):
        """StudySession cannot be modified after creation."""

        session = StudySession(
            session_id="session-001",
            timestamp=datetime.now(timezone.utc),
            activity_type=ActivityType.QUIZ,
            payload=QuizResult(
                total_questions=10,
                correct_answers=8,
                incorrect_answers=2,
            ),
        )

        with self.assertRaises(AttributeError):
            session.session_id = "session-002"

    def test_learning_profile_is_immutable(self):
        """LearningProfile cannot be modified after creation."""

        profile = LearningProfile(
            learner_id="learner-001",
        )

        with self.assertRaises(AttributeError):
            profile.total_sessions = 1


if __name__ == "__main__":
    unittest.main(verbosity=2)