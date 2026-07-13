## Milestone 1.1 – Extract AksaraCard

**Tanggal**
2026-07-14

**Tujuan**
Memindahkan class `AksaraCard` dari `main.py` ke `ui/aksara_card.py` agar kode lebih modular.

**Perubahan**
- Membuat folder `ui`
- Membuat file `aksara_card.py`
- Memindahkan class `AksaraCard`
- Memperbarui import pada `main.py`
- Menghapus import yang tidak digunakan

**Git Commit**
refactor: extract AksaraCard and rename Javanese data module

**Catatan**
Refactoring selesai tanpa mengubah perilaku aplikasi.




## Milestone 1.2 – Extract FlashcardTab

**Tanggal**
2026-07-14

**Tujuan**
Memindahkan class `FlashcardTab` ke modul terpisah agar struktur proyek lebih modular.

**Perubahan**
- Membuat folder `tabs`
- Membuat `flashcard_tab.py`
- Memindahkan seluruh class `FlashcardTab`
- Memindahkan seluruh import yang diperlukan
- Memperbarui import di `main.py`
- Menghapus import yang tidak digunakan

**Git Commit**
refactor: extract FlashcardTab into tabs package

**Catatan**
Refactoring selesai tanpa mengubah perilaku aplikasi.