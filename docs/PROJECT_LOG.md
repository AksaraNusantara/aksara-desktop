# PROJECT LOG

---

## Milestone 1.1 – Extract AksaraCard

**Tanggal**
14 Juli 2026

**Status**
✅ Selesai

**Tujuan**
Memisahkan komponen kartu aksara menjadi modul tersendiri agar UI lebih modular.

**Perubahan**
- Membuat folder `ui`
- Membuat `ui/aksara_card.py`
- Memindahkan class `AksaraCard`
- Membersihkan import pada `main.py`

**Git Commit**
refactor: extract AksaraCard into ui package

---

## Milestone 1.2 – Extract FlashcardTab

**Tanggal**
14 Juli 2026

**Status**
✅ Selesai

**Tujuan**
Memisahkan tab Flashcard menjadi modul tersendiri.

**Perubahan**
- Membuat folder `tabs`
- Membuat `tabs/flashcard_tab.py`
- Memindahkan seluruh class `FlashcardTab`
- Memperbaiki dependency dan import
- Memperbaiki masalah encoding UTF-8

**Git Commit**
refactor: extract FlashcardTab into tabs package

---

## Milestone 1.3 – Extract TransliterasiTab

**Tanggal**
14 Juli 2026

**Status**
✅ Selesai

**Tujuan**
Memisahkan fitur transliterasi ke modul tersendiri.

**Perubahan**
- Membuat `tabs/transliterasi_tab.py`
- Memindahkan class `TransliterasiTab`
- Memindahkan `TRANSLITERATION_MAP` ke `aksara_jawa.py`
- Membersihkan import
- Program tetap berjalan tanpa perubahan perilaku

**Git Commit**
refactor: extract TransliterasiTab into tabs package