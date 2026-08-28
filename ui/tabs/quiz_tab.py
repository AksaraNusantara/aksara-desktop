"""
Quiz feature tab.

Coordinates Quiz application components with the Qt user interface.
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)
from PySide6.QtGui import QFont

from application.learning.quiz.quiz_difficulty import QuizDifficulty
from application.learning.quiz.quiz_session import QuizSession
from core.learning.models.payload import QuizResult
from ui.widgets.empty_state import EmptyStateWidget


class QuizTab(QWidget):
    """
    Quiz user-interface boundary.

    QuizSession remains the source of truth for Quiz lifecycle.
    QuizTab owns only temporary presentation state and coordinates the
    completed result with LearningService.
    """

    quiz_started = Signal()
    quiz_completed = Signal()
    quiz_cancelled = Signal()
    quiz_finished = Signal()
    open_home_requested = Signal()

    def __init__(
        self,
        generator,
        learning_service,
        learner_id: str,
        learner_display_name: str = "Guest",
        parent: QWidget | None = None,
        scriptpack_active: Callable[[], bool] | None = None,
    ) -> None:
        super().__init__(parent)

        self._generator = generator
        self._learning_service = learning_service
        self._learner_id = learner_id
        self._learner_display_name = learner_display_name or "Guest"
        self._scriptpack_active = scriptpack_active or (lambda: True)

        self._session: QuizSession | None = None
        self._current_question = None
        self._current_question_number = 0
        self._selected_answer = None
        self._selected_button = None
        self._quiz_started_at: datetime | None = None
        self._result: QuizResult | None = None

        self._difficulty_enabled = True
        self._start_enabled = True
        self._cancel_enabled = False
        self._check_enabled = False
        self._next_enabled = False

        self._feedback_visible = False
        self._feedback_is_correct: bool | None = None
        self._feedback_text = ""
        self._correct_answer_text = ""
        self._result_visible = False
        self._result_recorded = False

        self._build_ui()
        self._refresh_ui_state()

    @property
    def is_quiz_active(self) -> bool:
        """Return whether a Quiz session is currently active."""
        return self._session is not None and not self._result_visible

    @property
    def is_result_visible(self) -> bool:
        """Return whether the completed Quiz result is currently displayed."""
        return self._result_visible

    @property
    def difficulty_enabled(self) -> bool:
        return self._difficulty_enabled

    @property
    def start_enabled(self) -> bool:
        return self._start_enabled

    @property
    def cancel_enabled(self) -> bool:
        return self._cancel_enabled

    @property
    def check_enabled(self) -> bool:
        return self._check_enabled

    @property
    def feedback_visible(self) -> bool:
        return self._feedback_visible

    @property
    def feedback_is_correct(self) -> bool | None:
        return self._feedback_is_correct

    @property
    def feedback_text(self) -> str:
        return self._feedback_text

    @property
    def correct_answer_text(self) -> str:
        return self._correct_answer_text

    @property
    def next_enabled(self) -> bool:
        return self._next_enabled

    @property
    def selected_answer(self) -> str | None:
        return self._selected_answer

    @property
    def progress_text(self) -> str:
        if self._result_visible or self._current_question_number <= 0:
            return "—"
        if self._session is None:
            return "—"
        return (
            f"Soal {self._current_question_number} "
            f"dari {self._session.total_questions}"
        )

    @property
    def accuracy_text(self) -> str:
        if self._session is not None:
            correct = self._session.correct_answers
            incorrect = self._session.incorrect_answers
        elif self._result is not None:
            correct = self._result.correct_answers
            incorrect = self._result.incorrect_answers
        else:
            return "0%"

        total_answers = correct + incorrect
        if total_answers == 0:
            return "0%"
        accuracy = correct / total_answers * 100
        return f"{int(accuracy)}%" if accuracy.is_integer() else f"{accuracy:.1f}%"

    def refresh(self) -> None:
        """Refresh the Quiz view from the current ScriptPack state."""
        self._refresh_ui_state()

    def start_quiz(self, difficulty: QuizDifficulty, total_questions: int) -> None:
        """Start a new Quiz session."""
        if self._session is not None:
            raise RuntimeError("A Quiz is already active.")
        if total_questions < 1:
            raise ValueError("total_questions must be at least 1.")
        if not self._scriptpack_active():
            raise RuntimeError("No ScriptPack is currently active.")

        self._session = QuizSession(
            total_questions=total_questions,
            difficulty=difficulty,
        )
        self._current_question_number = 1
        self._selected_answer = None
        self._selected_button = None
        self._quiz_started_at = datetime.now()
        self._result = None
        self._result_visible = False
        self._result_recorded = False
        self._reset_feedback()

        self._current_question = self._generator.generate(difficulty=self._session.difficulty)

        self._difficulty_enabled = False
        self._start_enabled = False
        self._cancel_enabled = True
        self._check_enabled = False
        self._next_enabled = False

        self.quiz_started.emit()
        self._show_quiz_view()
        self._refresh_question_display()
        self._refresh_progress_display()
        self._refresh_statistics_display()
        self._refresh_ui_state()

    def cancel_quiz(self) -> None:
        """Cancel the active Quiz without producing a result."""
        if self._result_visible:
            raise RuntimeError("Quiz result is currently displayed.")
        if self._session is None:
            return

        self._session.cancel()
        self._reset_to_ready()
        self.quiz_cancelled.emit()

    def select_answer(self, selected_answer: str) -> None:
        """Select an answer without submitting it."""
        if self._session is None:
            raise RuntimeError("No active Quiz.")
        if self._result_visible:
            raise RuntimeError("Quiz result is currently displayed.")
        if self._feedback_visible:
            raise RuntimeError("Answer selection is closed during feedback.")
        if self._current_question is None:
            raise RuntimeError("No active Quiz question.")
        if selected_answer not in self._current_question.options:
            raise ValueError("Selected answer is not an available option.")

        self._selected_answer = selected_answer
        self._check_enabled = True
        self._apply_selected_button_style()
        self._refresh_ui_state()

    def check_answer(self, selected_answer: str | None = None) -> bool:
        """Check the selected answer and show feedback."""
        if self._session is None:
            raise RuntimeError("No active Quiz.")
        if self._result_visible:
            raise RuntimeError("Quiz result is currently displayed.")
        if self._current_question is None:
            raise RuntimeError("No active Quiz question.")
        if selected_answer is None:
            selected_answer = self._selected_answer
        if selected_answer is None:
            raise RuntimeError("No answer has been selected.")

        is_correct = self._session.answer(
            self._current_question,
            selected_answer,
        )

        self._set_feedback(
            is_correct=is_correct,
            correct_answer=self._current_question.correct_answer,
        )

        self._check_enabled = False

        if self._session.is_complete:
            self._next_enabled = False
            self._complete_quiz()
        else:
            self._next_enabled = True

        self._refresh_statistics_display()
        self._refresh_ui_state()

        return is_correct

    def next_question(self) -> None:
        """Advance to the next Quiz question."""
        if self._result_visible:
            return
        if self._session is None:
            raise RuntimeError("No active Quiz.")
        if not self._next_enabled:
            raise RuntimeError("Next question is not available.")
        if self._session.is_complete:
            raise RuntimeError("No next question is available after the final answer.")

        self._current_question_number += 1
        self._current_question = self._generator.generate(difficulty=self._session.difficulty)
        self._selected_answer = None
        self._selected_button = None
        self._next_enabled = False
        self._check_enabled = False
        self._reset_feedback()

        self._refresh_question_display()
        self._refresh_progress_display()
        self._refresh_ui_state()

    def retry_quiz(self) -> None:
        """Start another Quiz with the same difficulty and question count."""
        if not self._result_visible or self._result is None:
            raise RuntimeError("Quiz result is not available for retry.")

        difficulty = QuizDifficulty(
            self._result.difficulty_level
        )
        total_questions = self._result.total_questions
        self._clear_session_state()
        self._reset_ready_controls()
        self.start_quiz(difficulty=difficulty, total_questions=total_questions)

    def finish_quiz(self) -> None:
        """Finish the completed Quiz and return the tab to READY."""
        if not self._result_visible:
            raise RuntimeError("Quiz result is not available.")

        self._clear_session_state()
        self._reset_ready_controls()
        self._show_quiz_view()
        self._refresh_question_display()
        self._refresh_progress_display()
        self._refresh_statistics_display()
        self._refresh_ui_state()
        self.quiz_finished.emit()

    def _complete_quiz(self) -> None:
        if self._session is None or not self._session.is_complete:
            return
        if self._result_recorded:
            return

        result = self._session.build_result()
        self._result = result
        self._learning_service.record_quiz_result(
            learner_id=self._learner_id,
            result=result,
        )
        self._result_recorded = True
        self._result_visible = True
        self._session = None
        self._current_question = None
        self._selected_answer = None
        self._selected_button = None
        self._cancel_enabled = False
        self._next_enabled = False
        self._check_enabled = False
        self._difficulty_enabled = False
        self._start_enabled = False
        self.quiz_completed.emit()
        self._show_result_view()

    def _reset_to_ready(self) -> None:
        self._clear_session_state()
        self._reset_ready_controls()
        self._show_quiz_view()
        self._refresh_question_display()
        self._refresh_progress_display()
        self._refresh_statistics_display()
        self._refresh_ui_state()

    def _clear_session_state(self) -> None:
        self._session = None
        self._current_question = None
        self._current_question_number = 0
        self._selected_answer = None
        self._selected_button = None
        self._quiz_started_at = None
        self._result = None
        self._result_visible = False
        self._result_recorded = False
        self._reset_feedback()

    def _reset_ready_controls(self) -> None:
        self._difficulty_enabled = True
        self._start_enabled = True
        self._cancel_enabled = False
        self._check_enabled = False
        self._next_enabled = False

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setSpacing(14)

        self._build_header(root_layout)

        self._view_stack = QStackedWidget()

        self._empty_state = EmptyStateWidget(
            title="No ScriptPack Activated",
            description=(
                "Activate a ScriptPack from Home "
                "to start a Quiz."
            ),
            action_text="Open Home",
        )
        self._empty_state.set_icon("📝")
        self._empty_state.action_requested.connect(
            self.open_home_requested.emit,
        )

        self.quiz_content_widget = QWidget()
        content_layout = QVBoxLayout(self.quiz_content_widget)
        content_layout.setSpacing(14)
        self._build_configuration(content_layout)
        self._build_question_area(content_layout)
        self._build_answer_area(content_layout)
        self._build_feedback(content_layout)
        self._build_statistics(content_layout)
        self._build_action_area(content_layout)

        self._build_result_view(self._view_stack)

        self._view_stack.insertWidget(0, self._empty_state)
        self._view_stack.insertWidget(1, self.quiz_content_widget)

        root_layout.addWidget(self._view_stack)
        root_layout.addStretch()

        self.start_button.clicked.connect(self._handle_start_clicked)
        self.check_button.clicked.connect(self._handle_check_clicked)
        self.cancel_button.clicked.connect(self.cancel_quiz)
        self.next_button.clicked.connect(self.next_question)
        self.retry_button.clicked.connect(self.retry_quiz)
        self.finish_button.clicked.connect(self.finish_quiz)

    def _build_header(self, root_layout: QVBoxLayout) -> None:
        header_layout = QHBoxLayout()
        self.title_label = QLabel("QUIZ")
        self.progress_label = QLabel("Soal 0 / 0")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.progress_label)
        root_layout.addLayout(header_layout)

        self.learner_label = QLabel("Guest")
        self.learner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.learner_label.setText(self._learner_display_name)
        root_layout.addWidget(self.learner_label)

        self.start_date_label = QLabel("")
        self.start_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(self.start_date_label)

    def _build_configuration(self, root_layout: QVBoxLayout) -> None:
        configuration_layout = QHBoxLayout()
        configuration_layout.addWidget(QLabel("Difficulty:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems([
            "Level 1 — 1 aksara",
            "Level 2 — 2 aksara",
            "Level 3 — 3 aksara",
            "Level 4 — 4 aksara",
        ])
        self._difficulty_values = (
            QuizDifficulty.LEVEL_1,
            QuizDifficulty.LEVEL_2,
            QuizDifficulty.LEVEL_3,
            QuizDifficulty.LEVEL_4,
        )
        self.start_button = QPushButton("MULAI QUIZ")
        configuration_layout.addWidget(self.difficulty_combo)
        configuration_layout.addWidget(self.start_button)
        configuration_layout.addStretch()
        root_layout.addLayout(configuration_layout)

    def _build_question_area(self, root_layout: QVBoxLayout) -> None:
        self.question_label = QLabel("—")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setMinimumHeight(120)
        self.question_label.setFont(
            QFont(
                "Noto Sans Javanese",
                52,
            )
        )
        self.instruction_label = QLabel("Pilih transliterasi yang benar.")
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(self.question_label)
        root_layout.addWidget(self.instruction_label)

    def _build_answer_area(self, root_layout: QVBoxLayout) -> None:
        answer_layout = QGridLayout()
        self.answer_buttons = []
        for index in range(4):
            button = QPushButton("—")
            button.setMinimumHeight(52)
            self.answer_buttons.append(button)
            button.clicked.connect(
                lambda checked=False, btn=button: self._handle_answer_clicked(btn)
            )
            answer_layout.addWidget(button, index // 2, index % 2)
        root_layout.addLayout(answer_layout)

    def _build_feedback(self, root_layout: QVBoxLayout) -> None:
        self.feedback_widget = QWidget()
        feedback_layout = QVBoxLayout(self.feedback_widget)
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correct_answer_label = QLabel("")
        self.correct_answer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        feedback_layout.addWidget(self.feedback_label)
        feedback_layout.addWidget(self.correct_answer_label)
        root_layout.addWidget(self.feedback_widget)

    def _build_statistics(self, root_layout: QVBoxLayout) -> None:
        statistics_layout = QHBoxLayout()
        self.correct_label = QLabel("Benar: 0")
        self.incorrect_label = QLabel("Salah: 0")
        self.accuracy_label = QLabel("Akurasi: 0%")
        statistics_layout.addStretch()
        statistics_layout.addWidget(self.correct_label)
        statistics_layout.addWidget(self.incorrect_label)
        statistics_layout.addWidget(self.accuracy_label)
        statistics_layout.addStretch()
        root_layout.addLayout(statistics_layout)

    def _build_action_area(self, root_layout: QVBoxLayout) -> None:
        action_layout = QHBoxLayout()
        self.check_button = QPushButton("PERIKSA")
        self.cancel_button = QPushButton("BATALKAN")
        self.next_button = QPushButton("NEXT QUESTION")
        action_layout.addStretch()
        action_layout.addWidget(self.check_button)
        action_layout.addWidget(self.cancel_button)
        action_layout.addWidget(self.next_button)
        action_layout.addStretch()
        root_layout.addLayout(action_layout)

    def _build_result_view(self, root_layout) -> None:
        self.result_widget = QWidget()
        result_layout = QVBoxLayout(self.result_widget)
        result_layout.setSpacing(12)

        self.result_title_label = QLabel("QUIZ SELESAI")
        self.result_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_score_label = QLabel("0 / 0")
        self.result_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_accuracy_label = QLabel("Akurasi: 0%")
        self.result_accuracy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_statistics_label = QLabel("Benar: 0    Salah: 0")
        self.result_statistics_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        result_layout.addWidget(self.result_title_label)
        result_layout.addWidget(self.result_score_label)
        result_layout.addWidget(self.result_accuracy_label)
        result_layout.addWidget(self.result_statistics_label)

        button_layout = QHBoxLayout()
        self.retry_button = QPushButton("COBA LAGI")
        self.finish_button = QPushButton("SELESAI")
        button_layout.addStretch()
        button_layout.addWidget(self.retry_button)
        button_layout.addWidget(self.finish_button)
        button_layout.addStretch()
        result_layout.addLayout(button_layout)

        root_layout.addWidget(self.result_widget)

    def _handle_start_clicked(self) -> None:
        self.start_quiz(
            difficulty=self._selected_difficulty(),
            total_questions=10,
        )

    def _handle_answer_clicked(self, button: QPushButton) -> None:
        self.select_answer(button.text())

    def _handle_check_clicked(self) -> None:
        self.check_answer()

    def _selected_difficulty(self) -> QuizDifficulty:
        return self._difficulty_values[self.difficulty_combo.currentIndex()]

    def _refresh_question_display(self) -> None:
        if self._current_question is None:
            self.question_label.setText("—")
            for button in self.answer_buttons:
                button.setText("—")
            return

        self.question_label.setText(self._current_question.prompt)
        for button, option in zip(self.answer_buttons, self._current_question.options):
            button.setText(option)

    def _refresh_ui_state(self) -> None:
        scriptpack_available = self._scriptpack_active()

        self.difficulty_combo.setEnabled(
            self._difficulty_enabled and scriptpack_available
        )
        self.start_button.setEnabled(
            self._start_enabled and scriptpack_available
        )
        self.cancel_button.setEnabled(self._cancel_enabled)
        self.check_button.setEnabled(self._check_enabled)
        self.next_button.setEnabled(self._next_enabled)

        for button in self.answer_buttons:
            button.setEnabled(
                self._session is not None
                and not self._feedback_visible
                and not self._result_visible
            )

        self.feedback_widget.setVisible(self._feedback_visible)
        self.progress_label.setText(self.progress_text)

        if self._result_visible:
            self._view_stack.setCurrentWidget(self.result_widget)
            self._update_result_display()
        elif self._session is not None or self._scriptpack_active():
            self._view_stack.setCurrentWidget(self.quiz_content_widget)
        else:
            self._view_stack.setCurrentWidget(self._empty_state)

    def _set_feedback(self, is_correct: bool, correct_answer: str) -> None:
        self._feedback_visible = True
        self._feedback_is_correct = is_correct
        if is_correct:
            self._feedback_text = "✓ BENAR!"
            self._correct_answer_text = ""
        else:
            self._feedback_text = "✗ KURANG TEPAT"
            self._correct_answer_text = correct_answer
        self.feedback_label.setText(self._feedback_text)
        self.correct_answer_label.setText(
            f"Jawaban benar: {self._correct_answer_text}"
            if self._correct_answer_text
            else ""
        )

    def _reset_feedback(self) -> None:
        self._feedback_visible = False
        self._feedback_is_correct = None
        self._feedback_text = ""
        self._correct_answer_text = ""
        if hasattr(self, "feedback_label"):
            self.feedback_label.setText("")
            self.correct_answer_label.setText("")

    def _apply_selected_button_style(self) -> None:
        for button in self.answer_buttons:
            button.setStyleSheet("")
        self._selected_button = None
        for button in self.answer_buttons:
            if button.text() == self._selected_answer:
                button.setStyleSheet("border: 2px solid; font-weight: 600;")
                self._selected_button = button
                break

    def _clear_answer_button_style(self) -> None:
        for button in self.answer_buttons:
            button.setStyleSheet("")
        self._selected_button = None

    def _refresh_progress_display(self) -> None:
        self.progress_label.setText(self.progress_text)

    def _statistics_values(self) -> tuple[int, int]:
        if self._session is not None:
            return self._session.correct_answers, self._session.incorrect_answers
        if self._result is not None:
            return self._result.correct_answers, self._result.incorrect_answers
        return 0, 0

    def _refresh_statistics_display(self) -> None:
        correct, incorrect = self._statistics_values()
        self.correct_label.setText(f"Benar: {correct}")
        self.incorrect_label.setText(f"Salah: {incorrect}")
        self.accuracy_label.setText(f"Akurasi: {self.accuracy_text}")

    def _update_result_display(self) -> None:
        if self._result is None:
            self.result_score_label.setText("0 / 0")
            self.result_accuracy_label.setText("Akurasi: 0%")
            self.result_statistics_label.setText("Benar: 0    Salah: 0")
            return

        self.result_score_label.setText(
            f"{self._result.correct_answers} / {self._result.total_questions}"
        )
        self.result_accuracy_label.setText(
            f"Akurasi: {self.accuracy_text}"
        )
        self.result_statistics_label.setText(
            f"Benar: {self._result.correct_answers}    "
            f"Salah: {self._result.incorrect_answers}"
        )

    def _show_result_view(self) -> None:
        self._clear_answer_button_style()
        self._view_stack.setCurrentWidget(self.result_widget)
        self._refresh_ui_state()

    def _show_quiz_view(self) -> None:
        self._view_stack.setCurrentWidget(self.quiz_content_widget)

        if self._quiz_started_at is None:
            self.start_date_label.setText("")
        else:
            self.start_date_label.setText(
                f"Dimulai {self._format_date(self._quiz_started_at)}"
            )

    @staticmethod
    def _format_date(value: datetime) -> str:
        months = (
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember",
        )
        return f"{value.day} {months[value.month - 1]} {value.year}"
