from PySide6.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)

label = QLabel("Qt Test")
label.resize(300, 100)
label.show()

print("Before exec")

result = app.exec()

print("After exec", result)