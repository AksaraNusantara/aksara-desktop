# -*- coding: utf-8 -*-
"""
Aksara Nusantara

alphabet_tab.py

Alphabet learning module.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QScrollArea,  QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.aksara_card import AksaraCard
from data.aksara_jawa import HONOCOROKO_DATA

class AlphabetTab(QWidget):
    def __init__(self, javanese_font):
        super().__init__()
        self.javanese_font = javanese_font
        self.init_ui()

    def init_ui(self):	
        main_layout = QVBoxLayout(self)
        
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