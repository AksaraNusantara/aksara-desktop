"""
Aksara Nusantara

aksara_tab.py

Flashcard learning module.
"""

from PySide6.QtWidgets import (QFrame, QVBoxLayout, QWidget, QLabel,
                               QVBoxLayout, QHBoxLayout, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from data.aksara_jawa import HONOCOROKO_DATA

class FlashcardTab(QWidget):
    def __init__(self, javanese_font):
        super().__init__()
        self.javanese_font = javanese_font
        self.current_index = 0
        self.is_flipped = False
        self.cards = HONOCOROKO_DATA.copy()
        self.init_ui()
        self.show_current_card()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Flashcard Honocoroko")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.card_frame = QFrame()
        self.card_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.card_frame.setMinimumHeight(320)
        card_layout = QVBoxLayout(self.card_frame)
        
        self.main_label = QLabel()
        self.main_label.setFont(self.javanese_font)
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.main_label)
        
        self.answer_label = QLabel()
        self.answer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.answer_label)
        
        layout.addWidget(self.card_frame)
        
        # Tombol Suara
        sound_layout = QHBoxLayout()
        self.btn_sound = QPushButton("🔊 Dengar Pengucapan")
        self.btn_sound.clicked.connect(self.play_sound)
        sound_layout.addWidget(self.btn_sound)
        layout.addLayout(sound_layout)
        
        # Tombol Navigasi
        btn_layout = QHBoxLayout()
        self.btn_prev = QPushButton("← Previous")
        self.btn_flip = QPushButton("Show Answer")
        self.btn_next = QPushButton("Next →")
        self.btn_shuffle = QPushButton("Shuffle")
        
        self.btn_prev.clicked.connect(self.prev_card)
        self.btn_flip.clicked.connect(self.flip_card)
        self.btn_next.clicked.connect(self.next_card)
        self.btn_shuffle.clicked.connect(self.shuffle_cards)
        
        btn_layout.addWidget(self.btn_prev)
        btn_layout.addWidget(self.btn_flip)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addWidget(self.btn_shuffle)
        layout.addLayout(btn_layout)
    
    def show_current_card(self):
        aksara, nama, latin = self.cards[self.current_index]
        self.main_label.setText(aksara)
        self.answer_label.setText("")
        self.is_flipped = False
        self.btn_flip.setText("Show Answer")
    
    def flip_card(self):
        if not self.is_flipped:
            _, nama, latin = self.cards[self.current_index]
            self.answer_label.setText(f"<b>{nama}</b> — {latin}")
            self.btn_flip.setText("Hide Answer")
            self.is_flipped = True
        else:
            self.answer_label.setText("")
            self.btn_flip.setText("Show Answer")
            self.is_flipped = False
    
    def next_card(self):
        self.current_index = (self.current_index + 1) % len(self.cards)
        self.show_current_card()
    
    def prev_card(self):
        self.current_index = (self.current_index - 1) % len(self.cards)
        self.show_current_card()
    
    def shuffle_cards(self):
        random.shuffle(self.cards)
        self.current_index = 0
        self.show_current_card()
    
    def play_sound(self):
        aksara, nama, latin = self.cards[self.current_index]
        text = f"{nama}, {latin}"
        
        try:
            from gtts import gTTS
            import os
            from playsound3 import playsound   # ← ini yang benar
            
            tts = gTTS(text=text, lang='id')
            filename = "temp_pronounce.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            QMessageBox.warning(self, "Error Suara", f"Tidak bisa memutar suara:\n{str(e)}")

