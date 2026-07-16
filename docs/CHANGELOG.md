# Changelog

Semua perubahan penting pada proyek Aksara Nusantara didokumentasikan di sini.

---

## [0.1.0] - Unreleased

### Added

- Desktop application menggunakan Python & PySide6.
- Tampilan Aksara Lengkap.
- Flashcard.
- Quiz.
- Transliterasi Latin ? Aksara Jawa.
- Audio menggunakan Google Text-to-Speech.
- Theme system.
- Progress menggunakan JSON.
- Font Noto Sans Javanese.

### Changed

- Refactoring menuju arsitektur modular.
- `data_aksara.py` diubah menjadi `aksara_jawa.py`.
- `AksaraCard` dipindahkan ke folder `ui/`.
- `FlashcardTab` dipindahkan ke folder `tabs/`.
- `TransliterasiTab` dipindahkan ke folder `tabs/`.
- `TRANSLITERATION_MAP` dipindahkan ke `aksara_jawa.py`.
- Quiz diubah dari fungsi `create_quiz_tab()` menjadi class `QuizTab`.

### Development

- Git repository dibuat.
- Virtual Environment dibuat.
- Mulai menggunakan Git workflow.
- Menambahkan dokumentasi proyek.

### Known Issues

- Quiz masih berada di `main.py`.
- Progress Manager belum dipisahkan.
- Audio Manager belum dipisahkan.
- Theme Manager belum dipisahkan.
- Engine transliterasi masih sederhana.


## [0.1.1] - 2026-07-14

### Changed

- Quiz diubah menjadi class `QuizTab`.
- `QuizTab` dipindahkan ke `tabs/quiz_tab.py`.
- Struktur `MainWindow` disederhanakan dengan menghapus implementasi Quiz dari file utama.
- Seluruh tab utama kini menggunakan pendekatan modular.