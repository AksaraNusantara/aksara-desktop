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

from data.aksara_jawa import HONOCOROKO_DATA
from ui.aksara_card import AksaraCard
from tabs.flashcard_tab import FlashcardTab
from tabs.transliterasi_tab import TransliterasiTab
from tabs.quiz_tab import QuizTab

# Simple transliteration dictionary (bisa dikembangkan)
#trans_dict = {
#    "ha": "ꦲ", "na": "ꦤ", "ca": "ꦕ", "ra": "ꦫ", "ka": "ꦏ",
#    "da": "ꦢ", "ta": "ꦠ", "sa": "ꦱ", "wa": "ꦮ", "la": "ꦭ",
#    "pa": "ꦥ", "dha": "ꦝ", "ja": "ꦗ", "ya": "ꦪ", "nya": "ꦚ",
#    "ma": "ꦩ", "ga": "ꦒ", "ba": "ꦧ", "tha": "ꦛ", "nga": "ꦔ",
#    # Tambah sandhangan nanti
#    "a": "", "i": "ꦶ", "u": "ꦸ", "e": "ꦺ", "o": "ꦾ"
#}


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
        tabs.addTab(QuizTab(self.javanese_font, self.progress), "❓ Quiz")
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
        
        title_jawa = QLabel("ꦲꦤꦕꦫꦏ")
        title_jawa.setFont(QFont(self.javanese_font.family(), 18))
        title_jawa.setAlignment(Qt.AlignCenter)

        title_latin = QLabel("Honocoroko")
        title_latin.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_latin.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title_jawa)
        main_layout.addWidget(title_latin)
        
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())