"""
Learning Engine application service.

This module coordinates completed learning activities, StudySession
creation, LearningProfile updates, and persistence.

Architecture references:
    AD-LE-001 — LearningProfile is a persisted derived aggregate.
    AD-LE-002 — StudySession represents a completed activity.
    AD-LE-006 — Persistence is performed through LearningRepository.
    AD-LE-007 — LearningService is the primary business-logic entry point.
"""

from datetime import datetime, timezone
from uuid import uuid4

from core.learning.models.activity import ActivityType
from core.learning.models.learning_profile import LearningProfile
from core.learning.models.payload import QuizResult
from core.learning.models.study_session import StudySession
from core.learning.repositories.learning_repository import (
    LearningRepository,
)


class LearningService:
    """
    Coordinate learning activity processing.

    LearningService contains application-level orchestration. It does
    not know how domain data is persisted or which storage technology
    is being used.
    """

    def __init__(
        self,
        repository: LearningRepository,
    ) -> None:
        """
        Initialize the LearningService.

        Args:
            repository: LearningRepository used for persistence.
        """

        self.repository = repository

    def record_quiz_result(
        self,
        learner_id: str,
        result: QuizResult,
        timestamp: datetime | None = None,
    ) -> StudySession:
        """
        Record a completed Quiz activity.

        The operation creates a StudySession, updates the learner's
        LearningProfile, and persists both through LearningRepository.

        Args:
            learner_id: Unique identifier of the learner.
            result: Completed Quiz result.
            timestamp: Completion timestamp. If omitted, the current
                UTC time is used.

        Returns:
            The newly created StudySession.
        """

        if not learner_id:
            raise ValueError("learner_id cannot be empty.")

        if not isinstance(result, QuizResult):
            raise TypeError(
                "result must be an instance of QuizResult."
            )

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        if timestamp.tzinfo is None:
            raise ValueError(
                "timestamp must be timezone-aware."
            )

        session = StudySession(
            session_id=str(uuid4()),
            learner_id=learner_id,
            timestamp=timestamp,
            activity_type=ActivityType.QUIZ,
            payload=result,
        )

        self.repository.save_session(
            session,
        )

        profile = self.repository.load_profile(
            learner_id,
        )

        if profile is None:
            profile = LearningProfile(
                learner_id=learner_id,
            )

        updated_profile = LearningProfile(
            learner_id=profile.learner_id,
            total_sessions=profile.total_sessions + 1,
            total_questions=(
                profile.total_questions
                + result.total_questions
            ),
            correct_answers=(
                profile.correct_answers
                + result.correct_answers
            ),
            incorrect_answers=(
                profile.incorrect_answers
                + result.incorrect_answers
            ),
            last_activity=timestamp,
        )

        self.repository.save_profile(
            updated_profile,
        )

        return session