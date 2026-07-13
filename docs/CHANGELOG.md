# Changelog

Semua perubahan penting pada proyek **Aksara Nusantara** akan didokumentasikan di file ini.

Format changelog ini mengikuti prinsip *Keep a Changelog* dan menggunakan *Semantic Versioning*.

---

## [0.1.0] - Unreleased

### Added
- Aplikasi desktop berbasis Python dan PySide6.
- Halaman Aksara Lengkap untuk menampilkan 20 aksara dasar Honocoroko.
- Fitur Flashcard untuk membantu menghafal aksara.
- Fitur Quiz pilihan ganda.
- Fitur Transliterasi Latin ? Aksara Jawa (versi awal).
- Dukungan font Noto Sans Javanese.
- Sistem tema aplikasi (Default, Krem, Klasik Jawa, High Contrast).
- Penyimpanan progress belajar menggunakan file JSON.
- Pengucapan aksara menggunakan Google Text-to-Speech (gTTS).

### Changed
- Struktur proyek mulai dimodularisasi.
- `data_aksara.py` diubah menjadi `aksara_jawa.py` sebagai persiapan dukungan berbagai aksara Nusantara.
- Class `AksaraCard` dipindahkan ke modul `ui/aksara_card.py`.
- Class `FlashcardTab` dipindahkan ke modul `tabs/flashcard_tab.py`.

### Documentation
- Menambahkan `README.md`.
- Menambahkan `PROJECT_LOG.md`.
- Menambahkan `ROADMAP.md`.
- Menambahkan `TODO.md`.

### Development
- Inisialisasi Git repository.
- Menambahkan `.gitignore`.
- Menyiapkan Virtual Environment (`.venv`).
- Memulai penggunaan Git commit yang terstruktur.

### Known Issues
- Transliterasi Aksara Jawa ? Latin masih berupa placeholder.
- Engine transliterasi Latin ? Aksara Jawa masih sederhana dan belum mendukung sandhangan, pasangan, maupun aturan penulisan lengkap.
- Audio masih menggunakan implementasi langsung pada masing-masing tab dan belum dipusatkan ke Audio Manager.