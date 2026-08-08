"""
Learning Engine activity classification.

This module defines the activity classifications used by StudySession
to identify the type of completed learning activity.

Architecture reference:
    AD-LE-004 — Activity Classification identifies the type of
                learning activity represented by a StudySession.
"""

from enum import Enum


class ActivityType(str, Enum):
    """
    Identifies a learning activity type.

    Additional activity types may be introduced by future
    implementations without changing the StudySession model.
    """

    QUIZ = "quiz"