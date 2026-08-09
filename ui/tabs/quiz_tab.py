"""
Quiz feature tab.

Coordinates Quiz application components with the Qt user interface.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from application.learning.quiz.quiz_difficulty import QuizDifficulty
from application.learning.quiz.quiz_session import QuizSession


class QuizTab(QWidget):
    """
    Quiz user-interface boundary.

    QuizSession remains the source of truth for Quiz lifecycle.
    """

    quiz_started = Signal()
    quiz_completed = Signal()
    quiz_cancelled = Signal()

    def __init__(
        self,
        generator,
        learning_service,
        learner_id: str,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._generator = generator
        self._learning_service = learning_service
        self._learner_id = learner_id

        self._session: QuizSession | None = None
        self._current_question = None
        self._difficulty: QuizDifficulty | None = None

    @property
    def session(self) -> QuizSession | None:
        """Return the active QuizSession, if any."""

        return self._session

    def start_quiz(
        self,
        difficulty: QuizDifficulty,
        total_questions: int,
    ) -> None:
        """Start a new Quiz session."""

        if self._session is not None:
            raise RuntimeError(
                "A Quiz is already active."
            )

        self._difficulty = difficulty

        self._session = QuizSession(
            total_questions=total_questions,
        )

        self._current_question = (
            self._generator.generate(
                difficulty=difficulty,
            )
        )

        self.quiz_started.emit()

    def cancel_quiz(self) -> None:
        """Cancel the active Quiz."""

        if self._session is None:
            return

        self._session.cancel()

        self._session = None
        self._current_question = None
        self._difficulty = None

        self.quiz_cancelled.emit()

    def submit_answer(
        self,
        selected_answer: str,
    ) -> bool:
        """Submit the selected answer."""

        if self._session is None:
            raise RuntimeError(
                "No active Quiz."
            )

        if self._current_question is None:
            raise RuntimeError(
                "No active Quiz question."
            )

        if self._difficulty is None:
            raise RuntimeError(
                "No active Quiz difficulty."
            )

        is_correct = self._session.answer(
            self._current_question,
            selected_answer,
        )

        if self._session.is_complete:
            result = self._session.build_result()

            self._learning_service.record_quiz_result(
                learner_id=self._learner_id,
                result=result,
            )

            self._session = None
            self._current_question = None
            self._difficulty = None

            self.quiz_completed.emit()

            return is_correct

        self._current_question = (
            self._generator.generate(
                difficulty=self._difficulty,
            )
        )

        return is_correct