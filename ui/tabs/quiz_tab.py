# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
Aksara Nusantara
================

quiz_tab.py

Quiz learning module.

This module implements the interactive quiz interface for the
Aksara Nusantara desktop application.

Unlike the legacy implementation, this version operates on the
shared Core Engine and the active ScriptPack instead of using
hardcoded character datasets. Quiz questions are generated
dynamically from the currently activated writing system, making
the module reusable for any supported script.

Responsibilities
----------------
- Display quiz questions.
- Generate randomized answer choices.
- Validate user answers.
- Track quiz session score.
- Play character pronunciation through AudioService.
- Refresh quiz content from the active ScriptPack.

The QuizTab acts as the presentation layer of the quiz system.
Business logic related to ScriptPack access is delegated to the
Core Engine, while audio playback is delegated to AudioService.

Copyright
---------
Copyright (c) 2026 Aksara Nusantara Project

Licensed under the MIT License.
"""
import random

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QComboBox, QButtonGroup, QRadioButton,
                               QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class QuizTab(QWidget):
    """
    Quiz learning module.

    This widget provides an interactive multiple-choice quiz for
    learning and practicing characters from the currently active
    ScriptPack.

    Questions are generated dynamically from the Core Engine,
    allowing the same quiz implementation to support different
    writing systems without modification.

    The QuizTab is responsible only for presenting quiz content,
    collecting user answers, and displaying quiz results.
    Character data is obtained from the Core Engine, while
    pronunciation playback is delegated to AudioService.

    Notes
    -----
    This class represents the presentation layer of the quiz
    feature. Business logic should remain independent from the
    user interface whenever possible to simplify future migration
    to a dedicated QuizSession component.
    """
    def __init__(
        self,
        engine: CoreEngine,
        audio: AudioService,
    ) -> None:
        """
        Initialize the quiz learning module.

        Parameters
        ----------
        engine:
            Shared CoreEngine instance.
        audio:
            Shared AudioService instance.

        Returns
        -------
        None
        """
        super().__init__()

        self._engine = engine
        self._audio = audio

        self._characters: list[dict] = []

        self._current_score = 0
        self._current_total = 0

        self._current_answer = ""
        self._current_name = ""

        self._current_level = 1

        self._option_count = 4

        self._initialize_ui()

    # ------------------------------------------------------------------
    # UI Initialization
    # ------------------------------------------------------------------

    def _initialize_ui(self):
        layout = QVBoxLayout(self)
        
        # Level Selector
        level_layout = QHBoxLayout()
        level_layout.addWidget(QLabel("Level Kesulitan:"))
        self._level_combo = QComboBox()
        self._level_combo.addItems(["Level 1 (Mudah - 1 aksara)", 
                                   "Level 2 (2 aksara)", 
                                   "Level 3 (3 aksara)", 
                                   "Level 4 (Sulit - 4 aksara)"])
        self._level_combo.currentIndexChanged.connect(self.change_level)
        level_layout.addWidget(self._level_combo)
        layout.addLayout(level_layout)
        
        self._score_label = QLabel(f"Skor Tertinggi: {self.progress.get('high_score', 0)}")
        self._score_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self._score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._score_label)
        
        title = QLabel("Quiz Honocoroko")
        layout.addSpacing(10)
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self._question_label = QLabel()
        self._question_label.setFont(self.javanese_font)
        self._question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._question_label.setStyleSheet("padding: 40px; min-height: 120px;")
        layout.addWidget(self._question_label)
        
        instr = QLabel("Pilih jawaban yang benar:")
        instr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instr)
        
        self._options_group = QButtonGroup()
        self._option_buttons = []
        for _ in range(self._option_count):
            btn = QRadioButton()
            btn.setFont(QFont("Arial", 14))
            self._options_group.addButton(btn)
            self._option_buttons.append(btn)
            layout.addWidget(btn)
        
        btn_layout = QHBoxLayout()
        #self.btn_sound = QPushButton("?? Dengar Pengucapan")
        layout.addSpacing(15)
        self._listen_button = QPushButton("Periksa Jawaban")
        self._listen_button.setToolTip(
            "Periksa jawaban yang dipilih"
        )
        
        #self.btn_sound.clicked.connect(self.play_quiz_sound)
        self._listen_button.clicked.connect(self.check_answer)
        
        #btn_layout.addWidget(self.btn_sound)
        btn_layout.addWidget(self._listen_button)
        layout.addLayout(btn_layout)

        self._load_characters()

        self.__load_new_question()

    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------

    def _change_level(self, index):
        self._current_level = index + 1
        self.__load_new_question()

    # ------------------------------------------------------------------
    # Quiz Logic
    # ------------------------------------------------------------------
    
    def _load_new_question(
        self,
    ) -> None:
        """
        Generate a new quiz question from the active ScriptPack.

        The question and answer choices are generated dynamically
        using characters provided by the currently active ScriptPack.

        Returns
        -------
        None
        """
        # Reset pilihan jawaban
        self._options_group.setExclusive(False)
        for btn in self._option_buttons:
            btn.setChecked(False)
        self._options_group.setExclusive(True)

        # Level menentukan berapa aksara yang ditampilkan
        num_chars = self._current_level
        
        selected = random.sample(
            self._characters,
            num_chars,
        )

        glyph_text = " ".join(
            character["glyph"]
            for character in selected
        )

        self._current_answer = " ".join(
            character["latin"]
            for character in selected
        )

        self._current_name = " ".join(
            character["description"]
            for character in selected
        )

        self._question_label.setText(
            glyph_text,
        )
        
        # Generate options
        options = [self._current_answer]
        while len(options) < self._option_count:
            wrong = " ".join(
                character["latin"]
                for character in random.sample(
                    self._characters,
                    num_chars,
                )
            )
            if wrong not in options:
                options.append(wrong)
        random.shuffle(options)
        
        for i, btn in enumerate(self._option_buttons):
            btn.setText(options[i])
    
    def _play_quiz_sound(self):
        try:
            from gtts import gTTS
            import os
            from playsound3 import playsound
            
            text = f"{self._current_name}, {self._current_answer}"
            tts = gTTS(text=text, lang='id')
            filename = "temp_quiz.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            QMessageBox.warning(self, "Error Suara", f"Gagal memutar suara:\n{str(e)}")
    
    def _check_answer(self):
        """Validate the selected answer."""
        # Number of characters determined by the selected level.
        num_chars = self._current_level

        # Ensure enough characters are available.
        if len(self._characters) < num_chars:
            return

        selected = random.sample(
            self._characters,
            num_chars,
        )

        if not selected:
            QMessageBox.warning(self, "Pilih Jawaban", "Silakan pilih salah satu!")
            return
        
        self._current_total += 1
        is_correct = selected.text() == self._current_answer
        
        if is_correct:
            self._current_score += 1
            result = (
                f"✅ Benar!\n\n"
                f"Skor sesi: {self._current_score}/{self._current_total}"
            )
        else:
            result = result = f"❌ Salah.\n\nJawaban yang benar adalah:\n{self._current_answer}"
        
        QMessageBox.information(self, "Hasil", result)
        
        # Update high score jika lebih tinggi
        if self._current_score > self.progress.get("high_score", 0):
            self.progress["high_score"] = self._current_score
            self._score_label.setText(f"Skor Tertinggi: {self.progress['high_score']}")
            self.save_progress()
        
        self.__load_new_question()

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    def _shuffle_options(self) -> None:
        """
        Shuffle answer options.
        """
        ...
        pass

    def _load_characters(
        self,
    ) -> None:
        """
        Load characters from the active ScriptPack.

        Returns
        -------
        None
        """
        scriptpack = self._engine.active_scriptpack

        if scriptpack is None:
            self._characters = []
            return

        self._characters = scriptpack.characters