"""
Learning Engine statistics service.

This module provides derived statistics calculated from persisted
learning data.

Architecture references:
    AD-LE-008 — Statistics are Derived Data and are not the
                authoritative source of learning history.
"""

from dataclasses import dataclass

from core.learning.models.learning_profile import LearningProfile


@dataclass(frozen=True)
class LearningStatistics:
    """
    Represents derived learning statistics.

    Statistics are calculated output and are not Primary Data.

    Attributes:
        total_sessions: Total completed learning sessions.
        total_questions: Total questions processed.
        correct_answers: Total correct answers.
        incorrect_answers: Total incorrect answers.
        accuracy: Correct-answer ratio expressed as a percentage.
    """

    total_sessions: int
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    accuracy: float


class StatisticsService:
    """
    Calculate derived statistics from LearningProfile data.

    The service does not persist statistics and does not modify the
    LearningProfile.
    """

    def calculate(
        self,
        profile: LearningProfile,
    ) -> LearningStatistics:
        """
        Calculate statistics from a LearningProfile.

        Args:
            profile: LearningProfile containing aggregated learning state.

        Returns:
            Derived LearningStatistics.
        """

        if not isinstance(profile, LearningProfile):
            raise TypeError(
                "profile must be an instance of LearningProfile."
            )

        if profile.total_questions == 0:
            accuracy = 0.0
        else:
            accuracy = (
                profile.correct_answers
                / profile.total_questions
                * 100.0
            )

        return LearningStatistics(
            total_sessions=profile.total_sessions,
            total_questions=profile.total_questions,
            correct_answers=profile.correct_answers,
            incorrect_answers=profile.incorrect_answers,
            accuracy=accuracy,
        )