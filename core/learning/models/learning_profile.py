"""
Learning Engine learning profile model.

This module defines the LearningProfile domain model used to represent
the aggregated learning state of a learner.

LearningProfile is derived from StudySession records and may be
persisted for efficient access.

Architecture references:
    AD-LE-001 — LearningProfile represents aggregated learning state
                and does not store activity-specific payload.
    AD-LE-002 — StudySession is the primary learning activity record.
    AD-LE-008 — Statistics are derived data.
"""


from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LearningProfile:
    """
    Represents the aggregated learning state of one learner.

    LearningProfile is a persisted derived aggregate. It is not the
    authoritative source for learning activity history.

    Attributes:
        learner_id: Unique identifier of the learner.
        total_sessions: Total number of completed learning sessions.
        total_questions: Total number of questions processed.
        correct_answers: Total number of correct answers.
        incorrect_answers: Total number of incorrect answers.
        last_activity: Timestamp of the most recent completed activity.
    """

    learner_id: str
    total_sessions: int = 0
    total_questions: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    last_activity: datetime | None = None

    def __post_init__(self) -> None:
        """Validate the integrity of the learning profile."""

        if not self.learner_id:
            raise ValueError("learner_id cannot be empty.")

        if self.total_sessions < 0:
            raise ValueError("total_sessions cannot be negative.")

        if self.total_questions < 0:
            raise ValueError("total_questions cannot be negative.")

        if self.correct_answers < 0:
            raise ValueError("correct_answers cannot be negative.")

        if self.incorrect_answers < 0:
            raise ValueError("incorrect_answers cannot be negative.")

        if (
            self.correct_answers + self.incorrect_answers
            > self.total_questions
        ):
            raise ValueError(
                "correct_answers + incorrect_answers "
                "cannot exceed total_questions."
            )