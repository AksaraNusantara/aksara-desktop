# -*- coding: utf-8 -*-
"""
Aksara Nusantara

transliterasi_tab.py

Transliterasi learning module.
"""

from PySide6.QtWidgets import (QWidget, QLabel, QTextEdit,
                               QVBoxLayout, QHBoxLayout, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from data.aksara_jawa import TRANSLITERATION_MAP

class TransliterasiTab(QWidget):
    def __init__(self, javanese_font):
        super().__init__()
        self.javanese_font = javanese_font
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Transliterasi Latin ↔ Aksara Jawa")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Input Latin
        layout.addWidget(QLabel("Ketik teks Latin:"))
        self.input_latin = QTextEdit()
        self.input_latin.setMaximumHeight(80)
        layout.addWidget(self.input_latin)
        
        btn_layout = QHBoxLayout()
        self.btn_to_jawa = QPushButton("→ Ke Aksara Jawa")
        self.btn_to_latin = QPushButton("← Ke Latin")
        btn_layout.addWidget(self.btn_to_jawa)
        btn_layout.addWidget(self.btn_to_latin)
        layout.addLayout(btn_layout)
        
        # Output
        layout.addWidget(QLabel("Hasil:"))
        self.output = QTextEdit()
        self.output.setFont(self.javanese_font)
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        
        self.btn_to_jawa.clicked.connect(self.latin_to_jawa)
        self.btn_to_latin.clicked.connect(self.jawa_to_latin)
    
    def latin_to_jawa(self):
        text = self.input_latin.toPlainText().lower().strip()
        result = ""
        for word in text.split():
            for syllable in TRANSLITERATION_MAP:
                if syllable in word:
                    word = word.replace(
                        syllable,
                        TRANSLITERATION_MAP[syllable]
                    )
            result += word + " "
        self.output.setText(result.strip())
    
    def jawa_to_latin(self):
        # Sederhana dulu, hanya tampilkan pesan
        self.output.setText("Fitur ini masih dalam pengembangan\n(Membaca aksara Jawa ke Latin lebih kompleks)")

