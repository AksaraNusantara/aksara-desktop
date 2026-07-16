# -*- coding: utf-8 -*-
"""
Aksara Nusantara

quiz_tab.py

Quiz learning module.
"""

import random

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QComboBox, QButtonGroup, QRadioButton,
                               QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from data.aksara_jawa import HONOCOROKO_DATA

class QuizTab(QWidget):
    def __init__(self, javanese_font, progress):
        super().__init__()

        self.javanese_font = javanese_font
        self.progress = progress
        
        self.current_score = 0
        self.current_total = 0
        self.current_answer = ""
        self.current_nama = ""
        self.current_level = 1
        self.OPTION_COUNT = 4

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Level Selector
        level_layout = QHBoxLayout()
        level_layout.addWidget(QLabel("Level Kesulitan:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Level 1 (Mudah - 1 aksara)", 
                                   "Level 2 (2 aksara)", 
                                   "Level 3 (3 aksara)", 
                                   "Level 4 (Sulit - 4 aksara)"])
        self.level_combo.currentIndexChanged.connect(self.change_level)
        level_layout.addWidget(self.level_combo)
        layout.addLayout(level_layout)
        
        self.score_label = QLabel(f"Skor Tertinggi: {self.progress.get('high_score', 0)}")
        self.score_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_label)
        
        title = QLabel("Quiz Honocoroko")
        layout.addSpacing(10)
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.question_label = QLabel()
        self.question_label.setFont(self.javanese_font)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("padding: 40px; min-height: 120px;")
        layout.addWidget(self.question_label)
        
        instr = QLabel("Pilih jawaban yang benar:")
        instr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instr)
        
        self.options_group = QButtonGroup()
        self.option_buttons = []
        for _ in range(self.OPTION_COUNT):
            btn = QRadioButton()
            btn.setFont(QFont("Arial", 14))
            self.options_group.addButton(btn)
            self.option_buttons.append(btn)
            layout.addWidget(btn)
        
        btn_layout = QHBoxLayout()
        #self.btn_sound = QPushButton("?? Dengar Pengucapan")
        layout.addSpacing(15)
        self.btn_check = QPushButton("Periksa Jawaban")
        self.btn_check.setToolTip(
            "Periksa jawaban yang dipilih"
        )
        
        #self.btn_sound.clicked.connect(self.play_quiz_sound)
        self.btn_check.clicked.connect(self.check_answer)
        
        #btn_layout.addWidget(self.btn_sound)
        btn_layout.addWidget(self.btn_check)
        layout.addLayout(btn_layout)
        
        self.load_new_question()

    def change_level(self, index):
        self.current_level = index + 1
        self.load_new_question()
    
    def load_new_question(self):
        """Generate a new quiz question."""
        # Reset pilihan jawaban
        self.options_group.setExclusive(False)
        for btn in self.option_buttons:
            btn.setChecked(False)
        self.options_group.setExclusive(True)

        # Level menentukan berapa aksara yang ditampilkan
        num_chars = self.current_level
        
        selected = random.sample(HONOCOROKO_DATA, num_chars)
        aksara_text = " ".join([item[0] for item in selected])
        self.current_answer = " ".join([item[2] for item in selected])  # latin
        self.current_nama = " ".join([item[1] for item in selected])
        
        self.question_label.setText(aksara_text)
        
        # Generate options
        options = [self.current_answer]
        while len(options) < self.OPTION_COUNT:
            wrong = " ".join([item[2] for item in random.sample(HONOCOROKO_DATA, num_chars)])
            if wrong not in options:
                options.append(wrong)
        random.shuffle(options)
        
        for i, btn in enumerate(self.option_buttons):
            btn.setText(options[i])
    
    def play_quiz_sound(self):
        try:
            from gtts import gTTS
            import os
            from playsound3 import playsound
            
            text = f"{self.current_nama}, {self.current_answer}"
            tts = gTTS(text=text, lang='id')
            filename = "temp_quiz.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            QMessageBox.warning(self, "Error Suara", f"Gagal memutar suara:\n{str(e)}")
    
    def check_answer(self):
        """Validate the selected answer."""
        selected = self.options_group.checkedButton()
        if not selected:
            QMessageBox.warning(self, "Pilih Jawaban", "Silakan pilih salah satu!")
            return
        
        self.current_total += 1
        is_correct = selected.text() == self.current_answer
        
        if is_correct:
            self.current_score += 1
            result = (
                f"✅ Benar!\n\n"
                f"Skor sesi: {self.current_score}/{self.current_total}"
            )
        else:
            result = result = f"❌ Salah.\n\nJawaban yang benar adalah:\n{self.current_answer}"
        
        QMessageBox.information(self, "Hasil", result)
        
        # Update high score jika lebih tinggi
        if self.current_score > self.progress.get("high_score", 0):
            self.progress["high_score"] = self.current_score
            self.score_label.setText(f"Skor Tertinggi: {self.progress['high_score']}")
            self.save_progress()
        
        self.load_new_question()