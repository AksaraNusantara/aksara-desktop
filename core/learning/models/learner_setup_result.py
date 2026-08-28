"""Learner setup result model."""

from dataclasses import dataclass
from enum import Enum


class LearnerSetupMode(Enum):
    """Possible outcomes of learner setup."""

    NAMED = "named"
    GUEST = "guest"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class LearnerSetupResult:
    """Result produced by the learner setup UI."""

    mode: LearnerSetupMode
    display_name: str | None = None
