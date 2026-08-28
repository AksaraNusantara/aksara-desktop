from pathlib import Path
import sys
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from PySide6.QtWidgets import QApplication

from core.learning.models.learner_setup_result import LearnerSetupMode
from ui.learner_setup_dialog import LearnerSetupDialog


_QT_APP = QApplication.instance() or QApplication(sys.argv)


class TestLearnerSetupDialog(unittest.TestCase):
    def test_dialog_starts_without_result(self):
        dialog = LearnerSetupDialog()
        self.assertIsNone(dialog.result())
        dialog.close()

    def test_named_input_produces_named_result(self):
        dialog = LearnerSetupDialog()
        dialog._name_input.setText("Budi")
        dialog._on_start_clicked()

        result = dialog.result()

        self.assertIsNotNone(result)
        self.assertIs(result.mode, LearnerSetupMode.NAMED)
        self.assertEqual(result.display_name, "Budi")
        dialog.close()

    def test_guest_button_produces_guest_result(self):
        dialog = LearnerSetupDialog()
        dialog._guest_button.click()

        result = dialog.result()

        self.assertIsNotNone(result)
        self.assertIs(result.mode, LearnerSetupMode.GUEST)
        self.assertIsNone(result.display_name)
        dialog.close()

    def test_empty_name_produces_guest_result(self):
        dialog = LearnerSetupDialog()
        dialog._name_input.clear()
        dialog._on_start_clicked()

        result = dialog.result()

        self.assertIsNotNone(result)
        self.assertIs(result.mode, LearnerSetupMode.GUEST)
        self.assertIsNone(result.display_name)
        dialog.close()

    def test_whitespace_only_name_produces_guest_result(self):
        dialog = LearnerSetupDialog()
        dialog._name_input.setText("   ")
        dialog._on_start_clicked()

        result = dialog.result()

        self.assertIsNotNone(result)
        self.assertIs(result.mode, LearnerSetupMode.GUEST)
        self.assertIsNone(result.display_name)
        dialog.close()


if __name__ == "__main__":
    unittest.main()
