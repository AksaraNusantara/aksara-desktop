# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Aksara Nusantara
Data Aksara Jawa (Carakan)
"""

# ==========================================================
# AKSARA DASAR (HONOCOROKO)
# ==========================================================

HONOCOROKO_DATA = [
    # Baris 1
    ("ꦲ", "Ha", "ha"),
    ("ꦤ", "Na", "na"),
    ("ꦕ", "Ca", "ca"),
    ("ꦫ", "Ra", "ra"),
    ("ꦏ", "Ka", "ka"),

    # Baris 2
    ("ꦢ", "Da", "da"),
    ("ꦠ", "Ta", "ta"),
    ("ꦱ", "Sa", "sa"),
    ("ꦮ", "Wa", "wa"),
    ("ꦭ", "La", "la"),

    # Baris 3
    ("ꦥ", "Pa", "pa"),
    ("ꦝ", "Dha", "dha"),
    ("ꦗ", "Ja", "ja"),
    ("ꦪ", "Ya", "ya"),
    ("ꦚ", "Nya", "nya"),

    # Baris 4
    ("ꦩ", "Ma", "ma"),
    ("ꦒ", "Ga", "ga"),
    ("ꦧ", "Ba", "ba"),
    ("ꦛ", "Tha", "tha"),
    ("ꦔ", "Nga", "nga"),
]

# ==========================================================
# TRANSLITERASI LATIN -> AKSARA JAWA
# (Versi awal, akan dikembangkan)
# ==========================================================

TRANSLITERATION_MAP = {

    # Aksara Dasar
    "ha": "ꦲ",
    "na": "ꦤ",
    "ca": "ꦕ",
    "ra": "ꦫ",
    "ka": "ꦏ",

    "da": "ꦢ",
    "ta": "ꦠ",
    "sa": "ꦱ",
    "wa": "ꦮ",
    "la": "ꦭ",

    "pa": "ꦥ",
    "dha": "ꦝ",
    "ja": "ꦗ",
    "ya": "ꦪ",
    "nya": "ꦚ",

    "ma": "ꦩ",
    "ga": "ꦒ",
    "ba": "ꦧ",
    "tha": "ꦛ",
    "nga": "ꦔ",

    # Sandhangan (sementara)
    "a": "",
    "i": "ꦶ",
    "u": "ꦸ",
    "e": "ꦺ",
    "o": "ꦾ"
}

# ==========================================================
# KATEGORI
# ==========================================================

CATEGORIES = {
    "Honocoroko": HONOCOROKO_DATA,
}