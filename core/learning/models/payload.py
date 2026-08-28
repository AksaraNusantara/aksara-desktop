"""
Learning Engine payload models.

This module defines activity-specific payloads used by StudySession.

Architecture reference:
    AD-LE-005 — Payload represents the activity-specific result
                associated with a StudySession.
"""

from dataclasses import dataclass

from .activity import ActivityType


@dataclass(frozen=True)
class QuizResult:
    """
    Represents the completed result of a Quiz activity.

    Attributes:
        total_questions: Number of questions presented.
        correct_answers: Number of correctly answered questions.
        incorrect_answers: Number of incorrectly answered questions.
        difficulty_level: Difficulty level used for the Quiz.
    """

    total_questions: int
    correct_answers: int
    incorrect_answers: int
    difficulty_level: int

    @property
    def activity_type(self) -> ActivityType:
        """
        Return the Activity Classification associated with this payload.
        """

        return ActivityType.QUIZ

    def __post_init__(self) -> None:
        """Validate the integrity of the Quiz result."""

        if self.total_questions < 0:
            raise ValueError("total_questions cannot be negative.")

        if self.correct_answers < 0:
            raise ValueError("correct_answers cannot be negative.")

        if self.incorrect_answers < 0:
            raise ValueError("incorrect_answers cannot be negative.")

        if (
            self.correct_answers + self.incorrect_answers
            != self.total_questions
        ):
            raise ValueError(
                "correct_answers + incorrect_answers "
                "must equal total_questions."
            )