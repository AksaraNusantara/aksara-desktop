"""
Quiz question model.

This module defines the question-level model used by the Quiz
application layer.

The model is independent from PySide6 and the Learning Engine
persistence layer.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class QuizQuestion:
    """
    Represents one generated Quiz question.

    Attributes:
        prompt: Character glyph or sequence presented to the learner.
        correct_answer: Expected transliteration answer.
        options: Available answer choices.
    """

    prompt: str
    correct_answer: str
    options: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate the Quiz question."""

        if not self.prompt:
            raise ValueError("prompt cannot be empty.")

        if not self.correct_answer:
            raise ValueError("correct_answer cannot be empty.")

        if not self.options:
            raise ValueError("options cannot be empty.")

        if self.correct_answer not in self.options:
            raise ValueError(
                "correct_answer must exist in options."
            )

        if len(set(self.options)) != len(self.options):
            raise ValueError(
                "Quiz options must be unique."
            )