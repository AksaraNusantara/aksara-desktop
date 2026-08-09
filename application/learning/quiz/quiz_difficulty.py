"""
Quiz difficulty definitions.

This module defines the difficulty levels supported by the Quiz
application layer.

Difficulty determines the number of characters included in a
Quiz question.
"""

from enum import Enum


class QuizDifficulty(Enum):
    """
    Supported Quiz difficulty levels.

    The numeric value represents the number of characters used
    to construct a Quiz question.
    """

    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4

    @property
    def character_count(self) -> int:
        """
        Return the number of characters associated with this level.
        """

        return self.value