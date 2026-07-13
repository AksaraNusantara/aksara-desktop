"""
Aksara Nusantara

aksara_tab.py

Flashcard learning module.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class AksaraCard(QFrame):
    def __init__(self, aksara, nama, latin, javanese_font):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(160)
        layout = QVBoxLayout(self)
        
        label = QLabel(aksara)
        label.setFont(javanese_font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info = QLabel(f"<b>{nama}</b><br><span style='color:#555;'>{latin}</span>")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(label)
        layout.addWidget(info)
