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

---

## Milestone 1.4 – Refactor QuizTab

**Tanggal**
14 Juli 2026

**Status**
✅ Selesai

**Tujuan**
Mengubah implementasi Quiz dari fungsi `create_quiz_tab()` menjadi class `QuizTab` agar konsisten dengan arsitektur aplikasi dan lebih mudah dipelihara.

**Perubahan**
- Membuat class `QuizTab(QWidget)`.
- Memindahkan seluruh UI Quiz ke dalam class.
- Memindahkan state Quiz (`current_score`, `current_total`, `current_answer`, `current_nama`, dan `current_level`) menjadi atribut class.
- Memindahkan seluruh method Quiz ke dalam class.
- Menghapus fungsi `create_quiz_tab()`.
- MainWindow sekarang menggunakan objek `QuizTab` secara langsung.

**Hasil**
- Perilaku aplikasi tetap sama.
- Struktur kode menjadi lebih modular.
- Quiz siap dipindahkan ke folder `tabs/` pada milestone berikutnya.

**Git Commit**
refactor: convert create_quiz_tab into QuizTab class

**Lessons Learned**

- Perubahan dari fungsi menjadi class dapat dilakukan tanpa mengubah perilaku aplikasi.
- Memisahkan tanggung jawab antar class membuat proses refactoring berikutnya menjadi lebih mudah.
- Refactoring bertahap lebih aman dibanding melakukan banyak perubahan sekaligus.

---

## Milestone 1.5 – Extract QuizTab

**Tanggal**
14 Juli 2026

**Status**
✅ Selesai

**Tujuan**
Memindahkan implementasi `QuizTab` ke modul terpisah agar setiap tab memiliki file sendiri dan `MainWindow` hanya bertanggung jawab mengelola aplikasi.

**Perubahan**
- Membuat file `tabs/quiz_tab.py`.
- Memindahkan class `QuizTab` dari `main.py`.
- Menyesuaikan seluruh import yang diperlukan.
- Mengubah `MainWindow` agar menggunakan `QuizTab` dari package `tabs`.
- Memastikan seluruh fitur Quiz tetap berjalan dengan baik setelah pemindahan.

**Hasil**
- Semua tab utama kini memiliki implementasi yang terpisah.
- Struktur proyek menjadi lebih modular dan mudah dipelihara.
- `main.py` menjadi lebih ringkas.

**Lessons Learned**
- Refactoring bertahap membuat proses pemindahan file menjadi sederhana.
- Setelah sebuah komponen menjadi class mandiri, proses modularisasi hampir tidak memerlukan perubahan logika.

**Git Commit**
refactor: move QuizTab into tabs package

---

## 2026-07-23

### Milestone

Core Runtime Specification Frozen

### Completed

- BaseScriptPack Interface
- Script Registry
- Script Loader
- Script Validator
- Core Engine API
- Specification Traceability Workflow
- Traceability Matrix

### Architecture Decisions

- BaseScriptPack no longer exposes `get_manifest()`.
- Registry is the single source of truth for manifest metadata.
- Core Engine is the only public entry point for applications.
- Every implementation must reference its originating specification.

### Next Phase

Begin implementation of the Core Engine.

---

Temporary Repository Decision

During the initial Core Engine implementation,
the repository may keep Python packages at the repository root.

Migration to the final src/ package layout will occur
after the public package namespace has been finalized.

---

2026-07-23

Architecture Decision

Introduce core/exceptions.py before validator.py.

Reason:
Provide a unified exception hierarchy for the Core Engine and
avoid duplicated exception definitions across modules.

---

