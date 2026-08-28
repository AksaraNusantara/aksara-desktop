"""
Learning Engine learner identity model.

This module defines the LearnerIdentity domain model used to represent
the identity of one learner.

Architecture references:
    ADR-0003 — Learner Identity and Guest Mode
"""


from dataclasses import dataclass


@dataclass(frozen=True)
class LearnerIdentity:
    """
    Represents the identity of one learner.

    LearnerIdentity is the authoritative domain representation of
    learner identity.

    Attributes:
        learner_id: Stable unique identifier of the learner.
        display_name: User-facing name of the learner.
        is_guest: True when the learner is using Guest mode.
    """

    learner_id: str
    display_name: str
    is_guest: bool = False

    def __post_init__(self) -> None:
        """Validate the integrity of the learner identity."""

        if not self.learner_id:
            raise ValueError("learner_id cannot be empty.")

        if not self.display_name:
            raise ValueError("display_name cannot be empty.")

        if self.is_guest and self.display_name != "Guest":
            raise ValueError(
                'Guest learner must use display_name "Guest".'
            )