"""
Quiz session application model.

This module manages the state of one active Quiz session.

A QuizSession is temporary application state. It becomes learning
history only when completed and converted into QuizResult.
"""

from dataclasses import dataclass
from enum import Enum

from core.learning.models.payload import QuizResult

from .quiz_difficulty import QuizDifficulty
from .quiz_question import QuizQuestion


class QuizSessionState(Enum):
    """
    Lifecycle state of a QuizSession.

    A QuizSession becomes part of learning history only after it
    reaches COMPLETED state.
    """

    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class QuizAnswer:
    """
    Represents one answered Quiz question.

    Attributes:
        question: The question that was answered.
        selected_answer: The answer selected by the learner.
        is_correct: Whether the selected answer was correct.
    """

    question: QuizQuestion
    selected_answer: str
    is_correct: bool


class QuizSession:
    """
    Manage one active Quiz session.

    QuizSession owns temporary Quiz state and produces QuizResult when
    the session is completed.
    """

    def __init__(
        self,
        total_questions: int,
        difficulty: QuizDifficulty,
    ) -> None:
        """
        Initialize a Quiz session.

        Args:
            total_questions: Number of questions in this session.
        """

        if total_questions < 1:
            raise ValueError(
                "total_questions must be at least 1."
            )

        self._total_questions = total_questions
        self._difficulty = difficulty
        self._answers: list[QuizAnswer] = []
        self._state = QuizSessionState.ACTIVE

    @property
    def total_questions(self) -> int:
        """Return the configured number of questions."""

        return self._total_questions

    @property
    def difficulty(self) -> QuizDifficulty:
        """Return the Quiz difficulty."""

        return self._difficulty

    @property
    def answered_questions(self) -> int:
        """Return the number of answered questions."""

        return len(self._answers)

    @property
    def correct_answers(self) -> int:
        """Return the number of correct answers."""

        return sum(
            answer.is_correct
            for answer in self._answers
        )

    @property
    def incorrect_answers(self) -> int:
        """Return the number of incorrect answers."""

        return sum(
            not answer.is_correct
            for answer in self._answers
        )

    @property
    def state(self) -> QuizSessionState:
        """Return the current QuizSession state."""

        return self._state

    @property
    def is_complete(self) -> bool:
        """Return whether the QuizSession completed successfully."""

        return self._state is QuizSessionState.COMPLETED

    @property
    def is_cancelled(self) -> bool:
        """Return whether the QuizSession was cancelled."""

        return self._state is QuizSessionState.CANCELLED

    def answer(
        self,
        question: QuizQuestion,
        selected_answer: str,
    ) -> bool:
        """
        Record an answer for a Quiz question.

        Args:
            question: Question being answered.
            selected_answer: Answer selected by the learner.

        Returns:
            True if the answer is correct.
        """

        if self._state is not QuizSessionState.ACTIVE:
            raise RuntimeError(
                "QuizSession is not active."
            )

        if self.answered_questions >= self.total_questions:
            raise RuntimeError(
                "QuizSession has no remaining questions."
            )

        if selected_answer not in question.options:
            raise ValueError(
                "selected_answer must exist in question options."
            )

        is_correct = (
            selected_answer
            == question.correct_answer
        )

        self._answers.append(
            QuizAnswer(
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct,
            )
        )

        if self.answered_questions >= self.total_questions:
            self._state = QuizSessionState.COMPLETED

        return is_correct

    def cancel(self) -> None:
        """
        Cancel the active QuizSession.

        A cancelled QuizSession does not produce a QuizResult and is
        not persisted as learning history.
        """

        if self._state is not QuizSessionState.ACTIVE:
            raise RuntimeError(
                "Only an active QuizSession can be cancelled."
            )

        self._state = QuizSessionState.CANCELLED

    def build_result(self) -> QuizResult:
        """
        Build the final QuizResult.

        Returns:
            QuizResult representing the completed QuizSession.

        Raises:
            RuntimeError: If the QuizSession is not completed.
        """

        if self._state is not QuizSessionState.COMPLETED:
            raise RuntimeError(
                "QuizSession must be completed before building a result."
            )

        return QuizResult(
            total_questions=self.total_questions,
            correct_answers=self.correct_answers,
            incorrect_answers=self.incorrect_answers,
            difficulty_level=self.difficulty.value,
        )