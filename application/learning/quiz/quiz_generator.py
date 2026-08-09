"""
Quiz question generator.

This module generates QuizQuestion instances from characters supplied
by the active ScriptPack.

The generator has no dependency on PySide6 or Learning Engine
persistence.
"""

import random
from typing import Sequence

from .quiz_difficulty import QuizDifficulty
from .quiz_question import QuizQuestion


class QuizGenerator:
    """
    Generate randomized Quiz questions.

    Character records are expected to provide at least:
        glyph
        latin
        description
    """

    def __init__(
        self,
        characters: Sequence[dict],
        option_count: int = 4,
    ) -> None:
        """
        Initialize the Quiz generator.

        Args:
            characters:
                Characters supplied by the active ScriptPack.

            option_count:
                Number of answer choices per question.
        """

        if not characters:
            raise ValueError(
                "characters cannot be empty."
            )

        if option_count < 2:
            raise ValueError(
                "option_count must be at least 2."
            )

        self._characters = list(characters)
        self._option_count = option_count

    def generate(
        self,
        difficulty: QuizDifficulty,
    ) -> QuizQuestion:
        """
        Generate one QuizQuestion.

        Args:
            difficulty:
                Difficulty level controlling the number of characters
                included in the question.

        Returns:
            A generated QuizQuestion.

        Raises:
            ValueError:
                If difficulty is invalid or requires more characters
                than are available.
        """

        if not isinstance(
            difficulty,
            QuizDifficulty,
        ):
            raise ValueError(
                "difficulty must be a QuizDifficulty."
            )

        character_count = difficulty.character_count

        if character_count > len(self._characters):
            raise ValueError(
                "difficulty requires more characters than available."
            )

        selected = random.sample(
            self._characters,
            character_count,
        )

        prompt = " ".join(
            character["glyph"]
            for character in selected
        )

        correct_answer = " ".join(
            character["latin"]
            for character in selected
        )

        options = [
            correct_answer,
        ]

        while len(options) < self._option_count:
            candidate = " ".join(
                character["latin"]
                for character in random.sample(
                    self._characters,
                    character_count,
                )
            )

            if candidate not in options:
                options.append(candidate)

        random.shuffle(options)

        return QuizQuestion(
            prompt=prompt,
            correct_answer=correct_answer,
            options=tuple(options),
        )