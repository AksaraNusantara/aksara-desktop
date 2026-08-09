"""
Quiz feature tab.

Coordinates Quiz application components with the Qt user interface.
"""

from __future__ import annotations

from PySide6.QtCore import (
    Signal,
    Qt,
)
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

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

        # Dependencies
        self._generator = generator
        self._learning_service = learning_service
        self._learner_id = learner_id

        # Quiz state
        self._session = None
        self._current_question = None
        self._difficulty = None
        self._selected_answer = None

        # UI state contract
        self._difficulty_enabled = True
        self._start_enabled = True
        self._cancel_enabled = False
        self._check_enabled = False

        # Visual skeleton
        self._build_ui()

    @property
    def session(self) -> QuizSession | None:
        """Return the active QuizSession, if any."""

        return self._session

    @property
    def is_quiz_active(self) -> bool:
        """Return whether a Quiz is currently active."""

        return self._session is not None

    @property
    def difficulty_enabled(self) -> bool:
        """Return whether difficulty selection is enabled."""

        return self._difficulty_enabled

    @property
    def start_enabled(self) -> bool:
        """Return whether starting a Quiz is enabled."""

        return self._start_enabled

    @property
    def cancel_enabled(self) -> bool:
        """Return whether cancelling the Quiz is enabled."""

        return self._cancel_enabled

    @property
    def check_enabled(self) -> bool:
        """Return whether answer checking is enabled."""

        return self._check_enabled

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

        self._selected_answer = None

        self._difficulty_enabled = False
        self._start_enabled = False
        self._cancel_enabled = True
        self._check_enabled = False

        self.quiz_started.emit()

    def cancel_quiz(self) -> None:
        """Cancel the active Quiz."""

        if self._session is None:
            return

        self._session.cancel()

        self._session = None
        self._current_question = None
        self._difficulty = None
        self._selected_answer = None

        self._difficulty_enabled = True
        self._start_enabled = True
        self._cancel_enabled = False
        self._check_enabled = False

        self.quiz_cancelled.emit()

    def select_answer(
        self,
        selected_answer: str,
    ) -> None:
        """Select an answer without submitting it."""

        if self._session is None:
            raise RuntimeError(
                "No active Quiz."
            )

        if self._current_question is None:
            raise RuntimeError(
                "No active Quiz question."
            )

        if selected_answer not in (
            self._current_question.options
        ):
            raise ValueError(
                "Selected answer is not an available option."
            )

        self._selected_answer = selected_answer
        self._check_enabled = True

    def submit_answer(
        self,
        selected_answer: str | None = None,
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

        if selected_answer is None:
            selected_answer = self._selected_answer

        if selected_answer is None:
            raise RuntimeError(
                "No answer has been selected."
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
            self._selected_answer = None

            self._difficulty_enabled = True
            self._start_enabled = True
            self._cancel_enabled = False
            self._check_enabled = False

            self.quiz_completed.emit()

            return is_correct

        self._current_question = (
            self._generator.generate(
                difficulty=self._difficulty,
            )
        )

        self._selected_answer = None
        self._check_enabled = False

        return 

    def _build_header(
        self,
        root_layout: QVBoxLayout,
    ) -> None:
        """Build the Quiz header."""

        header_layout = QHBoxLayout()

        self.title_label = QLabel("QUIZ")
        self.progress_label = QLabel("Soal 0 / 0")

        header_layout.addWidget(
            self.title_label,
        )

        header_layout.addStretch()

        header_layout.addWidget(
            self.progress_label,
        )

        root_layout.addLayout(
            header_layout,
        )

    def _build_configuration(
        self,
        root_layout: QVBoxLayout,
    ) -> None:
        """Build Quiz configuration controls."""

        configuration_layout = QHBoxLayout()

        difficulty_label = QLabel(
            "Difficulty:"
        )

        self.difficulty_combo = QComboBox()

        self.difficulty_combo.addItems(
            [
                "Level 1 — 1 aksara",
                "Level 2 — 2 aksara",
                "Level 3 — 3 aksara",
                "Level 4 — 4 aksara",
            ]
        )

        configuration_layout.addWidget(
            difficulty_label,
        )

        configuration_layout.addWidget(
            self.difficulty_combo,
        )

        configuration_layout.addStretch()

        root_layout.addLayout(
            configuration_layout,
        )

    def _build_question_area(
        self,
        root_layout: QVBoxLayout,
    ) -> None:
        """Build the Quiz question area."""

        self.question_label = QLabel("—")

        self.question_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )

        self.instruction_label = QLabel(
            "Pilih transliterasi yang benar."
        )

        self.instruction_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )

        root_layout.addWidget(
            self.question_label,
        )

        root_layout.addWidget(
            self.instruction_label,
        )

    def _build_answer_area(
        self,
        root_layout: QVBoxLayout,
    ) -> None:
        """Build the answer button grid."""

        answer_layout = QGridLayout()

        self.answer_buttons = []

        for index in range(4):
            button = QPushButton("—")

            self.answer_buttons.append(
                button,
            )

            row = index // 2
            column = index % 2

            answer_layout.addWidget(
                button,
                row,
                column,
            )

        root_layout.addLayout(
            answer_layout,
        )

    def _build_action_area(
        self,
        root_layout: QVBoxLayout,
    ) -> None:
        """Build Quiz action buttons."""

        action_layout = QHBoxLayout()

        self.check_button = QPushButton(
            "PERIKSA"
        )

        self.cancel_button = QPushButton(
            "BATALKAN"
        )

        action_layout.addStretch()

        action_layout.addWidget(
            self.check_button,
        )

        action_layout.addWidget(
            self.cancel_button,
        )

        action_layout.addStretch()

        root_layout.addLayout(
            action_layout,
        )

    def _build_statistics(
        self,
        root_layout: QVBoxLayout,
    ) -> None:
        """Build Quiz statistics display."""

        statistics_layout = QHBoxLayout()

        self.correct_label = QLabel(
            "Benar: 0"
        )

        self.incorrect_label = QLabel(
            "Salah: 0"
        )

        self.accuracy_label = QLabel(
            "Akurasi: 0%"
        )

        statistics_layout.addStretch()

        statistics_layout.addWidget(
            self.correct_label,
        )

        statistics_layout.addWidget(
            self.incorrect_label,
        )

        statistics_layout.addWidget(
            self.accuracy_label,
        )

        statistics_layout.addStretch()

        root_layout.addLayout(
            statistics_layout,
        )

    def _build_ui(self) -> None:
        """Build the static QuizTab visual skeleton."""

        root_layout = QVBoxLayout(self)

        self._build_header(root_layout)
        self._build_configuration(root_layout)
        self._build_question_area(root_layout)
        self._build_answer_area(root_layout)
        self._build_action_area(root_layout)
        self._build_statistics(root_layout)

        root_layout.addStretch()