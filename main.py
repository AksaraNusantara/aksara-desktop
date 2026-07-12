# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import random
import json
from datetime import datetime

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QGridLayout, QLabel, QTabWidget,
                               QScrollArea, QFrame, QPushButton, QRadioButton,
                               QButtonGroup, QMessageBox, QTextEdit, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase, QPalette, QColor

from gtts import gTTS
import os
from playsound3 import playsound

# Fix Import
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from data_aksara import HONOCOROKO_DATA


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


# Simple transliteration dictionary (bisa dikembangkan)
trans_dict = {
    "ha": "ꦲ", "na": "ꦤ", "ca": "ꦕ", "ra": "ꦫ", "ka": "ꦏ",
    "da": "ꦢ", "ta": "ꦠ", "sa": "ꦱ", "wa": "ꦮ", "la": "ꦭ",
    "pa": "ꦥ", "dha": "ꦝ", "ja": "ꦗ", "ya": "ꦪ", "nya": "ꦚ",
    "ma": "ꦩ", "ga": "ꦒ", "ba": "ꦧ", "tha": "ꦛ", "nga": "ꦔ",
    # Tambah sandhangan nanti
    "a": "", "i": "ꦶ", "u": "ꦸ", "e": "ꦺ", "o": "ꦾ"
}

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
            for syllable in trans_dict:
                if syllable in word:
                    word = word.replace(syllable, trans_dict[syllable])
            result += word + " "
        self.output.setText(result.strip())
    
    def jawa_to_latin(self):
        # Sederhana dulu, hanya tampilkan pesan
        self.output.setText("Fitur ini masih dalam pengembangan\n(Membaca aksara Jawa ke Latin lebih kompleks)")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Belajar Honocoroko - Aksara Jawa")
        self.resize(1250, 820)
        
        self.javanese_font = self.load_embedded_font()
        self.current_level = 1
        self.progress = None
        self.load_progress()
        self.current_theme = "default"
        
        self.apply_theme("default")  # tema awal

        # Load Progress
        self.progress = self.load_progress()

        # Menu Bar
        menubar = self.menuBar()
        theme_menu = menubar.addMenu("🎨 Tema")
        
        action_default = theme_menu.addAction("Default (Dark Mode)")
        action_krem = theme_menu.addAction("Krem")
        action_classic = theme_menu.addAction("Klasik Jawa")
        action_high_contrast = theme_menu.addAction("High Contrast")
        
        action_default.triggered.connect(lambda: self.apply_theme("default"))
        action_krem.triggered.connect(lambda: self.apply_theme("krem"))
        action_classic.triggered.connect(lambda: self.apply_theme("classic"))
        action_high_contrast.triggered.connect(lambda: self.apply_theme("high_contrast"))
        
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        
        tabs.addTab(self.create_alphabet_tab(), "📖 Aksara Lengkap")
        tabs.addTab(FlashcardTab(self.javanese_font), "🃏 Flashcard")
        tabs.addTab(self.create_quiz_tab(), "❓ Quiz")
        tabs.addTab(TransliterasiTab(self.javanese_font), "🔄 Transliterasi")

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        palette = QPalette()
        
        if theme_name == "krem":
            palette.setColor(QPalette.ColorRole.Window, QColor(245, 235, 220))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(60, 40, 20))
            palette.setColor(QPalette.ColorRole.Button, QColor(205, 133, 63))
        elif theme_name == "classic":
            palette.setColor(QPalette.ColorRole.Window, QColor(139, 69, 19))   # Saddle Brown
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 248, 220))
            palette.setColor(QPalette.ColorRole.Button, QColor(205, 133, 63))
        elif theme_name == "high_contrast":
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Button, QColor(0, 100, 0))
        else:  # default
            palette.setColor(QPalette.ColorRole.Window, QColor(40, 40, 40))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.Button, QColor(80, 80, 80))
        
        self.setPalette(palette)
        print(f"Tema diubah ke: {theme_name}")

    def load_embedded_font(self):
        font_path = Path("fonts/NotoSansJavanese-Regular.ttf")
        if font_path.exists():
            font_id = QFontDatabase.addApplicationFont(str(font_path))
            if font_id != -1:
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                print(f"✅ Font Jawa ter-load: {font_family}")
                return QFont(font_family, 55)
        print("⚠️ Menggunakan font default")
        return QFont("Arial", 55)
    
    def apply_javanese_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(245, 235, 220))      # Krem
        palette.setColor(QPalette.ColorRole.WindowText, QColor(60, 40, 20))
        palette.setColor(QPalette.ColorRole.Button, QColor(205, 133, 63))       # Coklat kayu
        self.setPalette(palette)
    
    def create_alphabet_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        
        title = QLabel("ꦲꦤꦕꦫꦏ  Honocoroko")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)
        
        content = QWidget()
        grid = QGridLayout(content)
        grid.setSpacing(15)
        
        row = col = 0
        for aksara, nama, latin in HONOCOROKO_DATA:
            card = AksaraCard(aksara, nama, latin, self.javanese_font)
            grid.addWidget(card, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        scroll.setWidget(content)
        return widget

    # ==================== SAVE & LOAD PROGRESS ====================
    def load_progress(self):
        try:
            filename = f"progress_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except:
            return {"high_score": 0, "total_played": 0}
    
    def save_progress(self):
        try:
            filename = f"progress_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Gagal save progress:", e)
    
    # ==================== QUIZ TAB (dengan progress) ====================
    def create_quiz_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
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
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.question_label = QLabel()
        self.question_label.setFont(self.javanese_font)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("padding: 40px; min-height: 120px;")
        layout.addWidget(self.question_label)
        
        instr = QLabel("Pilih bacaan yang benar:")
        instr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instr)
        
        self.options_group = QButtonGroup()
        self.option_buttons = []
        for i in range(4):
            btn = QRadioButton()
            btn.setFont(QFont("Arial", 14))
            self.options_group.addButton(btn)
            self.option_buttons.append(btn)
            layout.addWidget(btn)
        
        btn_layout = QHBoxLayout()
        self.btn_sound = QPushButton("🔊 Dengar Pengucapan")
        self.btn_check = QPushButton("Check Answer")
        self.btn_next = QPushButton("Next Question")
        
        self.btn_sound.clicked.connect(self.play_quiz_sound)
        self.btn_check.clicked.connect(self.check_answer)
        self.btn_next.clicked.connect(self.load_new_question)
        
        btn_layout.addWidget(self.btn_sound)
        btn_layout.addWidget(self.btn_check)
        btn_layout.addWidget(self.btn_next)
        layout.addLayout(btn_layout)
        
        self.current_score = 0
        self.current_total = 0
        self.current_answer = ""
        self.current_nama = ""
        self.current_level = 1
        self.load_new_question()
        return widget

    def change_level(self, index):
        self.current_level = index + 1
        self.load_new_question()
    
    def load_new_question(self):
        # Level menentukan berapa aksara yang ditampilkan
        num_chars = self.current_level
        
        selected = random.sample(HONOCOROKO_DATA, num_chars)
        aksara_text = " ".join([item[0] for item in selected])
        self.current_answer = " ".join([item[2] for item in selected])  # latin
        self.current_nama = " ".join([item[1] for item in selected])
        
        self.question_label.setText(aksara_text)
        
        # Generate options
        options = [self.current_answer]
        while len(options) < 4:
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
        selected = self.options_group.checkedButton()
        if not selected:
            QMessageBox.warning(self, "Pilih Jawaban", "Silakan pilih salah satu!")
            return
        
        self.current_total += 1
        is_correct = selected.text() == self.current_answer
        
        if is_correct:
            self.current_score += 1
            result = f"🎉 Benar! Skor sesi ini: {self.current_score}/{self.current_total}"
        else:
            result = f"❌ Salah. Jawaban benar: **{self.current_answer}**"
        
        QMessageBox.information(self, "Hasil", result)
        
        # Update high score jika lebih tinggi
        if self.current_score > self.progress.get("high_score", 0):
            self.progress["high_score"] = self.current_score
            self.score_label.setText(f"Skor Tertinggi: {self.progress['high_score']} 🎉")
            self.save_progress()
        
        self.load_new_question()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())