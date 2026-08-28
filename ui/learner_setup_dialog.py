from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from core.learning.models.learner_setup_result import (
    LearnerSetupMode,
    LearnerSetupResult,
)


class LearnerSetupDialog(QDialog):
    """Initial learner setup dialog."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Learner Setup")
        self.setModal(True)

        self._result: LearnerSetupResult | None = None

        self._title_label = QLabel(
            "Siapkah anda belajar\nAksaraNusantara?"
        )
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._name_label = QLabel("Nama:")
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("Nama Anda (opsional)")

        self._guest_button = QPushButton("Guest")
        self._start_button = QPushButton("MULAI")

        self._button_box = QDialogButtonBox()
        self._button_box.addButton(
            self._start_button,
            QDialogButtonBox.ButtonRole.AcceptRole,
        )

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._title_label)
        self._layout.addWidget(self._name_label)
        self._layout.addWidget(self._name_input)
        self._layout.addWidget(self._guest_button)
        self._layout.addWidget(self._button_box)

        self._guest_button.clicked.connect(self._on_guest_clicked)
        self._start_button.clicked.connect(self._on_start_clicked)

    def result(self) -> LearnerSetupResult | None:
        """Return the setup result after a successful selection."""

        return self._result

    def _on_guest_clicked(self) -> None:
        self._result = LearnerSetupResult(
            mode=LearnerSetupMode.GUEST,
        )
        self.accept()

    def _on_start_clicked(self) -> None:
        display_name = self._name_input.text().strip()

        if not display_name:
            self._result = LearnerSetupResult(
                mode=LearnerSetupMode.GUEST,
            )
        else:
            self._result = LearnerSetupResult(
                mode=LearnerSetupMode.NAMED,
                display_name=display_name,
            )

        self.accept()
