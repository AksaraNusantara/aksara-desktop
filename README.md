# Aksara Nusantara

> Belajar, melestarikan, dan mengembangkan aksara tradisional Nusantara melalui teknologi.

![Status](https://img.shields.io/badge/status-in%20development-orange)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Qt](https://img.shields.io/badge/PySide6-6.x-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Tentang Proyek

**Aksara Nusantara** adalah aplikasi desktop berbasis Python yang bertujuan membantu pengguna mempelajari berbagai aksara tradisional Indonesia secara interaktif.

Pengembangan dimulai dari **Aksara Jawa (Honocoroko)** dan dirancang agar di masa depan dapat mendukung aksara tradisional lainnya seperti:

- Aksara Bali
- Aksara Sunda
- Aksara Batak
- Aksara Lontara
- Aksara Kaganga
- dan aksara Nusantara lainnya.

Proyek ini juga menjadi sarana belajar pengembangan perangkat lunak modern menggunakan Python, Git, dan praktik pengembangan open source.

---

# Fitur Saat Ini

- Menampilkan 20 aksara dasar Honocoroko
- Flashcard interaktif
- Quiz pilihan ganda
- Transliterasi Latin ? Aksara Jawa (versi awal)
- Pengucapan menggunakan Google Text-to-Speech
- Tema aplikasi
- Penyimpanan progress belajar

---

# Screenshot

*(akan ditambahkan setelah tampilan aplikasi lebih stabil)*

---

# Teknologi

- Python 3
- PySide6 (Qt for Python)
- gTTS
- playsound3
- JSON
- Git

---

# Struktur Proyek

```
AksaraNusantara/

+-- docs/
¦   +-- CHANGELOG.md
¦   +-- PROJECT_LOG.md
¦   +-- ROADMAP.md
¦   +-- TODO.md
¦
+-- fonts/
¦
+-- tabs/
¦
+-- ui/
¦
+-- main.py
+-- aksara_jawa.py
+-- requirements.txt
+-- README.md
```

---

# Instalasi

Clone repository:

```bash
git clone <repository-url>
```

Masuk ke folder proyek:

```bash
cd AksaraNusantara
```

Buat Virtual Environment:

```bash
python -m venv .venv
```

Aktifkan Virtual Environment:

Windows

```bash
.venv\Scripts\activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan aplikasi:

```bash
python main.py
```

---

# Roadmap

## Milestone 1
- Refactoring
- Modularisasi kode
- Dokumentasi

## Milestone 2
- Sandhangan
- Pasangan
- Murda
- Rekan

## Milestone 3
- Gamification

## Milestone 4
- Dukungan Multi Aksara

## Milestone 5
- Android

## Milestone 6
- Web Application

Lihat detail pada **ROADMAP.md**

---

# Kontribusi

Kontribusi selalu diterima.

Silakan membuat Issue atau Pull Request apabila ingin membantu pengembangan proyek ini.

---

# Lisensi

Proyek ini akan menggunakan lisensi **MIT License**.

---

# Tujuan

Proyek ini dibuat dengan harapan dapat membantu melestarikan aksara tradisional Indonesia melalui media pembelajaran yang modern, mudah digunakan, dan dapat diakses oleh siapa saja.

> "Melestarikan warisan budaya bukan hanya dengan mengenangnya, tetapi juga dengan menggunakannya."