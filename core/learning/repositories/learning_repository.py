"""
Learning Engine repository implementation.

This module defines the LearningRepository persistence boundary and its
StorageAdapter-based reference implementation.

ADR-0003 boundary:
    LearningRepository
    ├── StudySession
    └── LearningProfile

LearnerIdentity persistence belongs to LearnerRepository.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from core.learning.models.activity import ActivityType
from core.learning.models.learning_profile import LearningProfile
from core.learning.models.payload import QuizResult
from core.learning.models.study_session import StudySession
from core.learning.storage.storage_adapter import StorageAdapter


class LearningRepository(ABC):
    """Abstract persistence interface for learning data."""

    @abstractmethod
    def save_session(self, session: StudySession) -> None:
        """Persist a completed StudySession."""
        raise NotImplementedError

    @abstractmethod
    def load_sessions(self, learner_id: str) -> list[StudySession]:
        """Load persisted StudySession records for a learner."""
        raise NotImplementedError

    @abstractmethod
    def save_profile(self, profile: LearningProfile) -> None:
        """Persist a LearningProfile aggregate."""
        raise NotImplementedError

    @abstractmethod
    def load_profile(
        self,
        learner_id: str,
    ) -> LearningProfile | None:
        """Load a LearningProfile for a learner."""
        raise NotImplementedError


class StorageLearningRepository(LearningRepository):
    """StorageAdapter-backed LearningRepository implementation."""

    SESSIONS_KEY = "learning_sessions"
    PROFILES_KEY = "learning_profiles"

    def __init__(self, storage: StorageAdapter) -> None:
        self.storage = storage

    def save_session(self, session: StudySession) -> None:
        """Persist a StudySession, replacing an existing matching ID."""
        sessions_data = self.storage.load(self.SESSIONS_KEY)

        if sessions_data is None:
            sessions_data = []

        sessions = [
            self._deserialize_session(item)
            for item in sessions_data
        ]

        sessions = [
            existing
            for existing in sessions
            if existing.session_id != session.session_id
        ]

        sessions.append(session)

        self.storage.save(
            self.SESSIONS_KEY,
            [
                self._serialize_session(item)
                for item in sessions
            ],
        )

    def load_sessions(self, learner_id: str) -> list[StudySession]:
        """Load StudySession records belonging to a learner."""
        data = self.storage.load(self.SESSIONS_KEY)

        if data is None:
            return []

        sessions = [
            self._deserialize_session(item)
            for item in data
        ]

        return [
            session
            for session in sessions
            if session.learner_id == learner_id
        ]

    def save_profile(self, profile: LearningProfile) -> None:
        """Persist a LearningProfile."""
        profiles = self.storage.load(self.PROFILES_KEY)

        if profiles is None:
            profiles = {}

        profiles[profile.learner_id] = self._serialize_profile(profile)

        self.storage.save(
            self.PROFILES_KEY,
            profiles,
        )

    def load_profile(
        self,
        learner_id: str,
    ) -> LearningProfile | None:
        """Load a LearningProfile for a learner."""
        profiles = self.storage.load(self.PROFILES_KEY)

        if profiles is None:
            return None

        data = profiles.get(learner_id)

        if data is None:
            return None

        return self._deserialize_profile(data)

    @staticmethod
    def _serialize_session(
        session: StudySession,
    ) -> dict[str, Any]:
        """Convert a StudySession into storage-neutral data."""
        payload = session.payload

        if isinstance(payload, QuizResult):
            payload_data = {
                "type": "quiz",
                "difficulty_level": payload.difficulty_level,
                "total_questions": payload.total_questions,
                "correct_answers": payload.correct_answers,
                "incorrect_answers": payload.incorrect_answers,
            }
        else:
            raise TypeError(
                f"Unsupported payload type: {type(payload).__name__}"
            )

        return {
            "session_id": session.session_id,
            "learner_id": session.learner_id,
            "timestamp": session.timestamp.isoformat(),
            "activity_type": session.activity_type.value,
            "payload": payload_data,
        }

    @staticmethod
    def _deserialize_session(
        data: dict[str, Any],
    ) -> StudySession:
        """Reconstruct a StudySession from stored data."""
        activity_type = ActivityType(data["activity_type"])
        payload_data = data["payload"]

        if payload_data["type"] == "quiz":
            payload = QuizResult(
                difficulty_level=payload_data["difficulty_level"],
                total_questions=payload_data["total_questions"],
                correct_answers=payload_data["correct_answers"],
                incorrect_answers=payload_data["incorrect_answers"],
            )
        else:
            raise ValueError(
                f"Unsupported payload type: {payload_data['type']}"
            )

        return StudySession(
            session_id=data["session_id"],
            learner_id=data["learner_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            activity_type=activity_type,
            payload=payload,
        )

    @staticmethod
    def _serialize_profile(
        profile: LearningProfile,
    ) -> dict[str, Any]:
        """Convert a LearningProfile into storage-neutral data."""
        return {
            "learner_id": profile.learner_id,
            "total_sessions": profile.total_sessions,
            "total_questions": profile.total_questions,
            "correct_answers": profile.correct_answers,
            "incorrect_answers": profile.incorrect_answers,
            "last_activity": (
                profile.last_activity.isoformat()
                if profile.last_activity is not None
                else None
            ),
        }

    @staticmethod
    def _deserialize_profile(
        data: dict[str, Any],
    ) -> LearningProfile:
        """Reconstruct a LearningProfile from stored data."""
        last_activity = data.get("last_activity")

        return LearningProfile(
            learner_id=data["learner_id"],
            total_sessions=data["total_sessions"],
            total_questions=data["total_questions"],
            correct_answers=data["correct_answers"],
            incorrect_answers=data["incorrect_answers"],
            last_activity=(
                datetime.fromisoformat(last_activity)
                if last_activity is not None
                else None
            ),
        )
