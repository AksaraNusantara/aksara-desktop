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
- `AksaraCard` dipindahkan ke `ui/`.
- `FlashcardTab` dipindahkan ke `tabs/`.
- `TransliterasiTab` dipindahkan ke `tabs/`.
- `TRANSLITERATION_MAP` dipindahkan ke `aksara_jawa.py`.

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