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
        self._refresh_ui_state()

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
        self._refresh_question_display()
        self._refresh_ui_state()

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
        self._refresh_ui_state()

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
        self._refresh_ui_state()

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

            self._refresh_ui_state()

            return is_correct

        self._current_question = (
            self._generator.generate(
                difficulty=self._difficulty,
            )
        )

        self._selected_answer = None
        self._check_enabled = False

        self._refresh_ui_state()

        return is_correct

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

        self._difficulty_values = (
            QuizDifficulty.LEVEL_1,
            QuizDifficulty.LEVEL_2,
            QuizDifficulty.LEVEL_3,
            QuizDifficulty.LEVEL_4,
        )

        self.start_button = QPushButton(
            "MULAI QUIZ"
        )

        configuration_layout.addWidget(
            difficulty_label,
        )

        configuration_layout.addWidget(
            self.difficulty_combo,
        )

        configuration_layout.addWidget(
            self.start_button,
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

            button.clicked.connect(
                lambda checked=False, btn=button:
                    self._handle_answer_clicked(btn)
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

        self.check_button.clicked.connect(
            self._handle_check_clicked,
        )

        self.cancel_button = QPushButton(
            "BATALKAN"
        )

        self.cancel_button.clicked.connect(
            self.cancel_quiz,
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

        self.start_button.clicked.connect(
            self._handle_start_clicked,
        )

        root_layout.addStretch()

    def _refresh_question_display(self) -> None:
        """Refresh the visible question and answer options."""

        if self._current_question is None:
            self.question_label.setText("—")

            for button in self.answer_buttons:
                button.setText("—")

            return

        self.question_label.setText(
            self._current_question.prompt
        )

        for button, option in zip(
            self.answer_buttons,
            self._current_question.options,
        ):
            button.setText(option)

    def _selected_difficulty(self) -> QuizDifficulty:
        """Return the currently selected Quiz difficulty."""

        return self._difficulty_values[
            self.difficulty_combo.currentIndex()
        ]

    def _handle_start_clicked(self) -> None:
        """Handle the Start Quiz button."""

        difficulty = self._selected_difficulty()

        self.start_quiz(
            difficulty=difficulty,
            total_questions=10,
        )

        self._refresh_question_display()

    def _handle_answer_clicked(
        self,
        button: QPushButton,
    ) -> None:
        """Handle answer button selection."""

        self.select_answer(
            button.text(),
        )

    def _handle_check_clicked(self) -> None:
        """Handle the Check button."""

        self.submit_answer()

        if self.is_quiz_active:
            self._refresh_question_display()

    def _refresh_ui_state(self) -> None:
        """Synchronize widgets with the Quiz UI state contract."""

        self.difficulty_combo.setEnabled(
            self._difficulty_enabled
        )

        self.start_button.setEnabled(
            self._start_enabled
        )

        self.cancel_button.setEnabled(
            self._cancel_enabled
        )

        self.check_button.setEnabled(
            self._check_enabled
        )

        for button in self.answer_buttons:
            button.setEnabled(
                self._session is not None
            )