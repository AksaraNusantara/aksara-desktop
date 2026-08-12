"""
Learning Engine study session model.

This module defines the StudySession domain model used to represent
one completed learning activity.

Architecture references:
    AD-LE-002 — StudySession is the fundamental unit for recording
                completed learning activities.
    AD-LE-003 — History is derived from StudySession records.
    AD-LE-004 — Activity Classification identifies the activity type.
    AD-LE-005 — Payload represents the activity-specific result.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .activity import ActivityType


@dataclass(frozen=True)
class StudySession:
    """
    Represents one completed learning activity.

    StudySession is primary data and the authoritative source for
    learning activity history.

    Attributes:
        session_id: Unique identifier of the learning session.
        learner_id: Unique identifier of the learner who owns the session.
        timestamp: Date and time when the activity was completed.
        activity_type: Classification of the learning activity.
        payload: Activity-specific result associated with the session.
    """

    session_id: str
    learner_id: str
    timestamp: datetime
    activity_type: ActivityType
    payload: Any

    def __post_init__(self) -> None:
        """Validate StudySession domain invariants."""

        if not self.session_id:
            raise ValueError("session_id cannot be empty.")

        if not self.learner_id:
            raise ValueError("learner_id cannot be empty.")

        if not isinstance(self.activity_type, ActivityType):
            raise TypeError(
                "activity_type must be an instance of ActivityType."
            )

        if self.payload is None:
            raise ValueError("payload cannot be None.")

        payload_type = getattr(self.payload, "activity_type", None)

        if payload_type != self.activity_type:
            raise ValueError(
                "payload activity type must match "
                "StudySession activity_type."
            )
