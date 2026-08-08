"""
Tests for Learning Engine StatisticsService.

Architecture reference:
    AD-LE-008 — Statistics are Derived Data.
"""

from pathlib import Path
import sys
import unittest


# ---------------------------------------------------------------------------
# Project path
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from core.learning.models.learning_profile import LearningProfile
from core.learning.services.statistics_service import (
    LearningStatistics,
    StatisticsService,
)


class TestStatisticsService(unittest.TestCase):
    """Test derived learning statistics."""

    def setUp(self) -> None:
        """Create a fresh StatisticsService."""

        self.service = StatisticsService()

    def test_calculate_statistics(self):
        """Statistics are calculated correctly."""

        profile = LearningProfile(
            learner_id="learner-001",
            total_sessions=5,
            total_questions=50,
            correct_answers=40,
            incorrect_answers=10,
        )

        statistics = self.service.calculate(
            profile,
        )

        self.assertIsInstance(
            statistics,
            LearningStatistics,
        )

        self.assertEqual(
            statistics.total_sessions,
            5,
        )

        self.assertEqual(
            statistics.total_questions,
            50,
        )

        self.assertEqual(
            statistics.correct_answers,
            40,
        )

        self.assertEqual(
            statistics.incorrect_answers,
            10,
        )

        self.assertEqual(
            statistics.accuracy,
            80.0,
        )

    def test_zero_questions_produces_zero_accuracy(self):
        """Accuracy is zero when no questions have been answered."""

        profile = LearningProfile(
            learner_id="learner-001",
        )

        statistics = self.service.calculate(
            profile,
        )

        self.assertEqual(
            statistics.accuracy,
            0.0,
        )

    def test_perfect_accuracy(self):
        """All correct answers produce 100 percent accuracy."""

        profile = LearningProfile(
            learner_id="learner-001",
            total_sessions=1,
            total_questions=10,
            correct_answers=10,
            incorrect_answers=0,
        )

        statistics = self.service.calculate(
            profile,
        )

        self.assertEqual(
            statistics.accuracy,
            100.0,
        )

    def test_zero_accuracy(self):
        """All incorrect answers produce zero percent accuracy."""

        profile = LearningProfile(
            learner_id="learner-001",
            total_sessions=1,
            total_questions=10,
            correct_answers=0,
            incorrect_answers=10,
        )

        statistics = self.service.calculate(
            profile,
        )

        self.assertEqual(
            statistics.accuracy,
            0.0,
        )

    def test_invalid_profile_type_is_rejected(self):
        """StatisticsService accepts only LearningProfile."""

        with self.assertRaises(TypeError):
            self.service.calculate(
                "invalid",
            )

    def test_statistics_are_immutable(self):
        """Derived statistics cannot be modified after creation."""

        profile = LearningProfile(
            learner_id="learner-001",
            total_questions=10,
            correct_answers=8,
            incorrect_answers=2,
        )

        statistics = self.service.calculate(
            profile,
        )

        with self.assertRaises(AttributeError):
            statistics.accuracy = 90.0


if __name__ == "__main__":
    unittest.main(verbosity=2)