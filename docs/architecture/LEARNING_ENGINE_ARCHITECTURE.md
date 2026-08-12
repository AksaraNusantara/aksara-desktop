# Learning Engine Architecture

**Architecture Version:** 1.1
**Document Status:** Proposed
**Document Type:** Architecture Contract

---

> **Document Status Note**
>
> Dokumen ini mendefinisikan Architecture Contract Learning Engine Version 1.1.
>
> Status **Proposed** menunjukkan bahwa perubahan kontrak telah dirumuskan dan didokumentasikan, tetapi implementasi reference dan regression validation belum selesai. Setelah implementasi tervalidasi, dokumen dapat dikembalikan ke status **Stable**.
>
> Setelah dokumen dinyatakan Stable, perubahan terhadap Architecture Contract harus dilakukan secara terkontrol dan tidak boleh dilakukan hanya untuk menyesuaikan implementasi terhadap desain yang telah ditetapkan.

---

# 1. Introduction

> **Docstring**
>
> Bab ini menjelaskan tujuan, ruang lingkup, dan filosofi dasar Learning Engine. Bagian ini memberikan gambaran umum mengenai peran Learning Engine di dalam arsitektur AksaraNusantara tanpa membahas detail implementasi teknis.

## 1.1 Purpose

Learning Engine merupakan subsistem yang bertanggung jawab untuk mengelola seluruh data perkembangan belajar pengguna di dalam ekosistem AksaraNusantara. Setiap data aktivitas belajar yang menjadi bagian dari Learning Engine harus memiliki identitas learner yang jelas agar perkembangan belajar beberapa learner dalam satu instalasi aplikasi tetap terisolasi.

Learning Engine tidak berperan sebagai antarmuka pengguna (UI) maupun penyedia materi pembelajaran. Sebaliknya, komponen ini berfungsi sebagai pusat pengelolaan data belajar sehingga seluruh mode pembelajaran dapat menggunakan mekanisme pencatatan progres yang konsisten.

Arsitektur ini dirancang dengan prinsip **implementation-independent**, sehingga penambahan mode pembelajaran baru tidak memerlukan perubahan terhadap kontrak arsitektur yang telah ditetapkan.

---

## 1.2 Objectives

Learning Engine memiliki tujuan utama sebagai berikut:

* Menyediakan representasi tunggal terhadap perkembangan belajar pengguna.
* Menyediakan mekanisme penyimpanan progres yang konsisten.
* Menyediakan layanan statistik pembelajaran.
* Menjadi fondasi bagi seluruh mode pembelajaran di masa mendatang.
* Menjamin kompatibilitas terhadap pengembangan fitur tanpa mengubah kontrak arsitektur.

---

## 1.3 Design Philosophy

Learning Engine dikembangkan berdasarkan filosofi yang telah digunakan pada komponen Core Engine dan ScriptPack.

Prinsip utama yang digunakan adalah:

> **Architecture Contract First**

Kontrak arsitektur dirancang terlebih dahulu sebagai fondasi jangka panjang, sedangkan implementasi dilakukan secara bertahap sesuai kebutuhan setiap versi aplikasi.

Dengan pendekatan ini, perubahan implementasi tidak menyebabkan perubahan terhadap dokumen arsitektur, sehingga stabilitas sistem tetap terjaga.

---

## 1.4 Position in System Architecture

Secara konseptual, Learning Engine berada di antara antarmuka pengguna dan media penyimpanan data.

```text
           User Interface
                  │
                  ▼
         Learning Services
                  │
                  ▼
      Learning Repository
                  │
                  ▼
         Persistent Storage
```

Learning Engine tidak bergantung pada mode pembelajaran tertentu. Seluruh aktivitas belajar akan diproses melalui lapisan layanan (Service Layer) sebelum disimpan ke dalam media penyimpanan.

---

## 1.5 Current Implementation

Pada versi pertama implementasi Learning Engine, hanya mode **Quiz** yang terintegrasi dengan sistem.

Mode pembelajaran lain, seperti Flashcard, Writing Practice, Listening, maupun Recommendation Engine, belum diimplementasikan. Namun, arsitektur telah dirancang agar seluruh mode tersebut dapat ditambahkan pada versi mendatang tanpa memerlukan perubahan terhadap kontrak yang didefinisikan dalam dokumen ini.

Implementasi awal ini berfungsi sebagai validasi desain sebelum Learning Engine digunakan oleh seluruh ekosistem pembelajaran AksaraNusantara.

------------------

# 2. Scope

> **Docstring**
>
> Bab ini mendefinisikan ruang lingkup Learning Engine Architecture.
> Bagian ini menjelaskan tanggung jawab yang menjadi bagian dari Learning Engine serta batasan terhadap komponen yang berada di luar cakupan dokumen ini.
> Penetapan ruang lingkup bertujuan untuk menghindari tumpang tindih tanggung jawab antar subsistem dalam arsitektur AksaraNusantara.

## 2.1 Purpose

Learning Engine Architecture mendefinisikan struktur konseptual yang digunakan untuk mengelola perkembangan belajar pengguna di dalam aplikasi AksaraNusantara.

Dokumen ini berfungsi sebagai kontrak arsitektur yang menjadi acuan bagi seluruh implementasi Learning Engine, baik pada versi saat ini maupun pada pengembangan di masa mendatang.

---

## 2.2 In Scope

Learning Engine Architecture mencakup komponen-komponen berikut:

* Learning Profile
* Study Session
* Learning Activity
* Quiz Result
* Learning Statistics
* Learning Repository
* Learning Services
* Data Persistence
* Versioning
* Future Compatibility

Seluruh komponen tersebut merupakan bagian dari kontrak Learning Engine dan menjadi fondasi bagi sistem pencatatan serta pengelolaan perkembangan belajar pengguna.

---

## 2.3 Out of Scope

Dokumen ini tidak mendefinisikan implementasi maupun perilaku komponen berikut:

* Core Engine
* ScriptPack Architecture
* ScriptPack Interface
* User Interface (UI)
* Rendering Engine
* Audio Engine
* Theme Management
* Localization
* Application Bootstrap
* Platform-specific Implementation

Komponen-komponen tersebut memiliki dokumen arsitektur atau spesifikasi masing-masing dan berada di luar tanggung jawab Learning Engine.

---

## 2.4 Current Implementation Scope

Pada versi pertama Learning Engine, implementasi difokuskan pada integrasi dengan **Quiz Module**.

Ruang lingkup implementasi saat ini meliputi:

* Pencatatan hasil Quiz.
* Pembentukan Learning Profile.
* Penyimpanan Study Session bertipe Quiz.
* Perhitungan statistik dasar pembelajaran.
* Penyediaan data statistik bagi Home Dashboard.

Implementasi ini berfungsi sebagai validasi awal terhadap desain Learning Engine sebelum digunakan oleh mode pembelajaran lainnya.

---

## 2.5 Reserved for Future Implementation

Learning Engine telah dirancang agar mampu mendukung berbagai aktivitas pembelajaran selain Quiz.

Fitur-fitur berikut belum diimplementasikan pada versi saat ini, namun telah dipertimbangkan dalam desain arsitektur:

* Flashcard Learning
* Writing Practice
* Listening Practice
* Matching Exercise
* Transliteration Exercise
* Character Recognition Exercise
* Achievement System
* Learning Recommendation
* Adaptive Learning
* Cloud Synchronization

Penambahan fitur-fitur tersebut di masa mendatang diharapkan tidak memerlukan perubahan terhadap kontrak arsitektur yang didefinisikan dalam dokumen ini.

---

## 2.6 Scope Evolution

Learning Engine dirancang dengan prinsip **forward compatibility**, yaitu kemampuan untuk berkembang tanpa mengubah struktur konseptual yang telah ditetapkan.

Setiap implementasi baru diharapkan menjadi perluasan terhadap kontrak yang sudah ada. Apabila kebutuhan baru tidak dapat diakomodasi tanpa mengubah kontrak, perubahan tersebut harus melalui proses Architecture Decision dan versioning yang sesuai.

Dengan pendekatan ini, stabilitas dokumentasi dapat dipertahankan, sementara implementasi dapat terus berkembang mengikuti kebutuhan aplikasi dan ekosistem AksaraNusantara.

------------------

# 3. Terminology

> **Docstring**
>
> Bab ini mendefinisikan istilah-istilah yang digunakan di dalam Learning Engine Architecture.
> Seluruh istilah pada dokumen ini memiliki arti yang spesifik dan harus digunakan secara konsisten pada seluruh dokumentasi maupun implementasi Learning Engine.
> Definisi yang terdapat pada bab ini menjadi referensi utama apabila terjadi perbedaan penafsiran terhadap suatu istilah.

## 3.1 Learning Engine

Learning Engine adalah subsistem yang bertanggung jawab untuk mengelola seluruh data perkembangan belajar pengguna di dalam AksaraNusantara.

Learning Engine menyediakan mekanisme pencatatan aktivitas belajar, pengelolaan profil belajar, penyimpanan riwayat pembelajaran, serta penyediaan statistik yang digunakan oleh aplikasi.

Learning Engine bersifat independen terhadap jenis mode pembelajaran yang digunakan.

---

## 3.2 Learning Profile

Learning Profile merupakan representasi perkembangan belajar seorang learner.

Setiap Learning Profile dimiliki oleh tepat satu learner dan diidentifikasi secara unik melalui `learner_id`.

Learning Profile menyimpan informasi ringkasan yang menggambarkan kondisi belajar seorang learner secara keseluruhan dan menjadi sumber utama informasi progres pembelajaran.

Learning Profile tidak menyimpan detail setiap aktivitas belajar secara langsung, melainkan menyimpan hasil agregasi dari seluruh Study Session yang telah tercatat.

---

## 3.3 Study Session

Study Session merupakan satu aktivitas belajar yang telah selesai dan dimiliki oleh tepat satu learner.

Setiap Study Session memiliki `learner_id` yang mengidentifikasi learner pemilik aktivitas tersebut.

Satu Study Session dapat merepresentasikan berbagai jenis aktivitas pembelajaran, seperti Quiz, Flashcard, Writing Practice, maupun aktivitas lain yang didukung oleh Learning Engine.

Setiap Study Session memiliki awal, akhir, serta hasil yang dapat dicatat sebagai bagian dari riwayat pembelajaran.

Pada Reference Implementation versi pertama, hanya Study Session bertipe Quiz yang diimplementasikan. Setiap Study Session Quiz tetap memiliki ownership learner yang eksplisit.

---

## 3.4 Learner Identity

Learner Identity merupakan identitas unik yang digunakan Learning Engine untuk menentukan pemilik data perkembangan belajar. Identitas ini direpresentasikan oleh `learner_id`.

Setiap `StudySession` dan `LearningProfile` harus terkait dengan tepat satu `learner_id`. Learning Engine tidak bertanggung jawab terhadap mekanisme pemilihan, autentikasi, maupun pengelolaan antarmuka learner; Learning Engine menerima `learner_id` sebagai bagian dari konteks operasi pembelajaran.

---

## 3.5 Learning Activity

Learning Activity adalah jenis aktivitas pembelajaran yang dilakukan di dalam sebuah Study Session.

Learning Activity mendeskripsikan bentuk pembelajaran yang sedang dijalankan tanpa bergantung pada implementasi tertentu.

Contoh Learning Activity meliputi:

* Quiz
* Flashcard
* Writing Practice
* Listening Practice
* Matching Exercise

Reference Implementation saat ini hanya mengimplementasikan Quiz sebagai Learning Activity pertama.

---

## 3.6 Learning Statistics

Learning Statistics merupakan kumpulan informasi statistik yang dihasilkan berdasarkan Learning Profile dan Study Session.

Statistik ini digunakan untuk memberikan gambaran mengenai perkembangan belajar pengguna, seperti tingkat akurasi, jumlah sesi belajar, waktu belajar, maupun indikator perkembangan lainnya.

Learning Statistics bersifat turunan (*derived data*) dan dapat dihitung kembali dari data yang tersimpan.

---

## 3.7 Learning Repository

Learning Repository adalah komponen yang bertanggung jawab terhadap proses penyimpanan dan pengambilan data Learning Engine.

Repository tidak melakukan perhitungan statistik maupun logika bisnis.

Tanggung jawab Repository terbatas pada proses persistensi data.

---

## 3.8 Learning Service

Learning Service merupakan lapisan layanan yang mengoordinasikan interaksi antara User Interface, Repository, dan komponen lain di dalam Learning Engine.

Learning Service bertanggung jawab menjalankan logika bisnis pembelajaran tanpa bergantung pada mekanisme penyimpanan data.

---

## 3.9 Reference Implementation

Reference Implementation adalah implementasi pertama yang digunakan untuk membuktikan bahwa kontrak Learning Engine dapat diterapkan secara nyata.

Reference Implementation bukan merupakan batasan terhadap kemampuan Learning Engine, melainkan contoh implementasi yang mengikuti kontrak arsitektur.

Pada versi pertama dokumen ini, Quiz Module berperan sebagai Reference Implementation.

---

## 3.10 Future Implementation

Future Implementation adalah implementasi yang belum tersedia pada versi saat ini, tetapi telah diantisipasi oleh kontrak Learning Engine.

Penambahan Future Implementation tidak diharapkan mengubah struktur konseptual maupun kontrak arsitektur yang telah ditetapkan.

Contoh Future Implementation meliputi:

* Flashcard
* Writing Practice
* Listening Practice
* Recommendation Engine
* Adaptive Learning
* Achievement System

---

## 3.11 Architecture Contract

Architecture Contract adalah seperangkat aturan konseptual yang mendefinisikan struktur, tanggung jawab, hubungan antar komponen, serta prinsip-prinsip yang harus dipatuhi oleh seluruh implementasi Learning Engine.

Architecture Contract bersifat stabil dan dirancang untuk digunakan dalam jangka panjang. Perubahan terhadap kontrak hanya dilakukan melalui proses perubahan arsitektur yang terdokumentasi dan dapat ditelusuri.

Perubahan implementasi seharusnya tidak memerlukan perubahan terhadap Architecture Contract, kecuali apabila terjadi perubahan fundamental pada desain sistem.

------------------

# 4. Design Goals

> **Docstring**
>
> Bab ini menjelaskan tujuan utama yang menjadi dasar perancangan Learning Engine.
> Seluruh keputusan arsitektur yang didefinisikan dalam dokumen ini mengacu pada tujuan-tujuan desain yang dijelaskan pada bab ini.
> Design Goals berfungsi sebagai pedoman untuk mengevaluasi apakah suatu perubahan tetap selaras dengan visi jangka panjang Learning Engine.

## 4.1 Overview

Learning Engine dirancang sebagai fondasi sistem pembelajaran AksaraNusantara yang bersifat modular, mudah dikembangkan, dan tidak bergantung pada implementasi mode pembelajaran tertentu.

Arsitektur ini tidak hanya memenuhi kebutuhan Reference Implementation saat ini, tetapi juga dipersiapkan untuk mendukung perkembangan ekosistem pembelajaran pada versi-versi berikutnya.

---

## 4.2 Extensibility

Learning Engine harus memungkinkan penambahan mode pembelajaran baru tanpa memerlukan perubahan terhadap kontrak arsitektur.

Setiap mode pembelajaran baru diharapkan hanya menambahkan implementasi baru yang mematuhi kontrak Learning Engine.

Contoh implementasi yang diharapkan meliputi:

* Quiz
* Flashcard
* Writing Practice
* Listening Practice
* Matching Exercise

---

## 4.3 Modularity

Setiap komponen Learning Engine harus memiliki tanggung jawab yang jelas dan terpisah.

Pemisahan tanggung jawab ini bertujuan untuk:

* meningkatkan keterbacaan kode,
* mempermudah pemeliharaan,
* mempermudah pengujian,
* mengurangi ketergantungan antar komponen.

---

## 4.4 Maintainability

Learning Engine harus mudah dipelihara dalam jangka panjang.

Perubahan terhadap satu komponen diharapkan tidak memengaruhi komponen lain yang tidak memiliki keterkaitan langsung.

Pendekatan ini memungkinkan evolusi sistem dilakukan secara bertahap tanpa menyebabkan refactoring berskala besar.

---

## 4.5 Scalability

Arsitektur Learning Engine harus mampu berkembang mengikuti kebutuhan aplikasi.

Pertumbuhan jumlah pengguna, data pembelajaran, maupun mode pembelajaran tidak boleh mengharuskan perubahan terhadap struktur konseptual Learning Engine.

---

## 4.6 Implementation Independence

Kontrak Learning Engine tidak bergantung pada bahasa pemrograman, framework, maupun mekanisme penyimpanan data tertentu.

Implementasi Reference Implementation menggunakan Python dan JSON hanya merupakan salah satu bentuk penerapan kontrak.

Pada masa mendatang, Learning Engine dapat diimplementasikan menggunakan mekanisme penyimpanan atau platform lain selama tetap mematuhi kontrak arsitektur.

---

## 4.7 UI Independence

Learning Engine tidak memiliki ketergantungan terhadap User Interface.

Seluruh interaksi dengan antarmuka pengguna dilakukan melalui lapisan Service.

Dengan demikian, satu Learning Engine dapat digunakan oleh berbagai antarmuka, seperti:

* Desktop Application
* Mobile Application
* Web Application
* Command Line Interface (CLI)

tanpa memerlukan perubahan terhadap logika pembelajaran.

---

## 4.8 Stable Architecture Contract

Learning Engine dirancang berdasarkan prinsip bahwa kontrak arsitektur harus memiliki stabilitas jangka panjang.

Perubahan implementasi seharusnya dilakukan melalui penambahan komponen baru yang mematuhi kontrak, bukan melalui perubahan terhadap kontrak itu sendiri.

Kontrak hanya boleh direvisi apabila terjadi perubahan fundamental pada desain sistem.

---

## 4.9 Reference Implementation Philosophy

Reference Implementation berfungsi sebagai validasi bahwa kontrak Learning Engine dapat diimplementasikan secara nyata.

Reference Implementation tidak mendefinisikan batas kemampuan Learning Engine.

Seluruh keputusan desain pada dokumen ini harus mempertimbangkan kebutuhan jangka panjang, bukan hanya kebutuhan Reference Implementation saat ini.

---

## 4.10 Forward Compatibility

Learning Engine dirancang dengan mempertimbangkan kompatibilitas terhadap pengembangan di masa mendatang.

Setiap keputusan arsitektur diharapkan mampu mengakomodasi fitur baru tanpa memerlukan perubahan terhadap struktur konseptual yang telah ditetapkan.

Pendekatan ini memungkinkan evolusi Learning Engine berlangsung secara bertahap, konsisten, dan berkelanjutan.

------------------

# 5. Architecture Principles

> **Docstring**
>
> Bab ini mendefinisikan prinsip-prinsip arsitektur yang harus dipatuhi oleh seluruh implementasi Learning Engine.
> Prinsip-prinsip ini menjadi pedoman dalam proses perancangan, pengembangan, maupun evaluasi implementasi agar seluruh komponen tetap konsisten dengan kontrak arsitektur yang telah ditetapkan.
> Apabila terjadi konflik antara implementasi dan prinsip-prinsip pada bab ini, maka implementasi harus disesuaikan agar kembali mematuhi Architecture Contract.

## 5.1 Contract First

Learning Engine dikembangkan berdasarkan prinsip **Contract First**.

Kontrak arsitektur harus dirancang terlebih dahulu sebelum implementasi dimulai.

Seluruh implementasi merupakan realisasi dari kontrak yang telah ditetapkan, bukan sebaliknya.

> **Architecture Note**
>
> Kontrak arsitektur merupakan fondasi jangka panjang. Implementasi dapat berkembang dari waktu ke waktu, tetapi kontrak diharapkan tetap stabil.

---

## 5.2 Separation of Concerns

Setiap komponen Learning Engine harus memiliki tanggung jawab yang jelas.

Tidak diperkenankan menggabungkan beberapa tanggung jawab berbeda ke dalam satu komponen.

Contoh pemisahan tanggung jawab:

* User Interface bertanggung jawab terhadap presentasi.
* Service bertanggung jawab terhadap logika bisnis.
* Repository bertanggung jawab terhadap persistensi data.
* Model bertanggung jawab terhadap representasi data.

---

## 5.3 Single Responsibility

Setiap kelas maupun komponen sebaiknya memiliki satu tujuan utama.

Perubahan terhadap satu kebutuhan bisnis diharapkan hanya memengaruhi satu komponen yang relevan.

Prinsip ini bertujuan untuk meningkatkan keterbacaan, kemudahan pengujian, serta kemudahan pemeliharaan sistem.

---

## 5.4 Source of Truth

Learning Engine harus memiliki sumber data utama (*Source of Truth*) yang jelas.

**Study Session merupakan Primary Data dan authoritative source untuk learning activity history.**

Learning Profile merupakan **persisted derived aggregate** yang merepresentasikan keadaan agregat pembelajaran berdasarkan data aktivitas yang tersimpan dalam Study Session.

Learning Statistics merupakan **Derived Data** yang dihasilkan dari Primary Data dan/atau aggregated learning state.

Dengan demikian, klasifikasi data utama Learning Engine adalah:

```text
Study Session
    │
    └── Primary Data / Source of Truth

Learning Profile
    │
    └── Persisted Derived Aggregate

Learning Statistics
    │
    └── Derived Output
```

Learning Profile dapat disimpan secara permanen untuk efisiensi akses, tetapi tidak menjadi sumber kebenaran utama untuk riwayat aktivitas pembelajaran.

Learning Profile harus dapat direkonstruksi dari Study Session apabila diperlukan.

> **Architecture Note**
>
> Derived data dapat dihitung ulang dari Source of Truth.
>
> Persistensi terhadap derived aggregate diperbolehkan sebagai optimasi implementasi, tetapi tidak mengubah statusnya menjadi Primary Data.


---

## 5.5 Derived Data

Learning Statistics merupakan hasil perhitungan dari data pembelajaran yang telah tersimpan.

Derived data tidak boleh menjadi satu-satunya sumber informasi karena selalu dapat diregenerasi dari data utama apabila diperlukan.

Pendekatan ini menjaga konsistensi data serta mengurangi risiko inkonsistensi akibat duplikasi informasi.

---

## 5.6 Repository Isolation

Repository hanya bertanggung jawab terhadap proses penyimpanan dan pengambilan data.

Repository tidak boleh:

* menghitung statistik,
* menjalankan aturan bisnis,
* melakukan validasi tingkat aplikasi,
* mengambil keputusan pembelajaran.

Seluruh logika tersebut merupakan tanggung jawab Service Layer.

---

## 5.7 Service Oriented Processing

Seluruh proses bisnis Learning Engine harus melalui Service Layer.

User Interface tidak diperkenankan berinteraksi langsung dengan Repository.

Dengan pendekatan ini, seluruh logika bisnis terkonsentrasi pada satu lapisan yang dapat digunakan kembali oleh berbagai antarmuka aplikasi.

---

## 5.8 Implementation Independence

Kontrak Learning Engine tidak bergantung pada implementasi tertentu.

Perubahan bahasa pemrograman, framework, maupun mekanisme penyimpanan data tidak boleh memengaruhi struktur konseptual Learning Engine.

---

## 5.9 Forward Compatibility

Learning Engine harus dirancang untuk menerima perluasan fungsi tanpa mengubah Architecture Contract.

Penambahan mode pembelajaran baru diharapkan hanya memerlukan implementasi tambahan yang mengikuti kontrak yang telah ada.

---

## 5.10 Reference Implementation

Reference Implementation merupakan pembuktian bahwa Architecture Contract dapat diimplementasikan secara nyata.

Reference Implementation tidak boleh dianggap sebagai batas kemampuan Learning Engine maupun sebagai dasar untuk mengubah kontrak arsitektur.

> **Implementation Note**
>
> Reference Implementation pada versi pertama hanya mencakup integrasi dengan Quiz Module.

---

## 5.11 Documentation as Contract

Dokumen ini merupakan bagian dari kontrak resmi Learning Engine.

Seluruh implementasi diharapkan mengacu pada definisi, prinsip, dan struktur yang dijelaskan dalam dokumen ini.

Apabila implementasi tidak sesuai dengan dokumen, maka implementasi harus dievaluasi terlebih dahulu sebelum dilakukan perubahan terhadap Architecture Contract.

---

## 5.12 Long-Term Stability

Learning Engine dirancang untuk digunakan sebagai fondasi jangka panjang bagi seluruh ekosistem pembelajaran AksaraNusantara.

Setiap perubahan terhadap kontrak arsitektur harus dipertimbangkan secara menyeluruh karena dapat memengaruhi kompatibilitas implementasi yang telah ada.

Stabilitas kontrak merupakan prioritas utama dalam menjaga keberlanjutan pengembangan proyek.

------------------

# 6. System Architecture

> **Docstring**
>
> Bab ini memberikan gambaran umum mengenai struktur Learning Engine sebagai sebuah subsistem di dalam arsitektur AksaraNusantara.
> Fokus bab ini adalah hubungan antar lapisan (layers) dan aliran data secara konseptual, tanpa membahas implementasi teknis setiap komponen.
> Detail masing-masing komponen dijelaskan pada bab-bab berikutnya.

## 6.1 Architectural Overview

Learning Engine merupakan subsistem yang berada di antara User Interface dan mekanisme penyimpanan data.

Seluruh aktivitas pembelajaran diproses melalui Learning Engine sehingga antarmuka pengguna tidak berinteraksi langsung dengan media penyimpanan.

Pendekatan ini memastikan bahwa seluruh logika bisnis pembelajaran berada pada satu lokasi yang terpusat.

---

## 6.2 Layered Architecture

Learning Engine menggunakan pendekatan **Layered Architecture**.

Setiap lapisan memiliki tanggung jawab yang berbeda dan hanya berkomunikasi dengan lapisan yang berdekatan.

```text
+---------------------------+
|      User Interface       |
+---------------------------+
             │
             ▼
+---------------------------+
|     Learning Services     |
+---------------------------+
             │
             ▼
+---------------------------+
|   Learning Repository     |
+---------------------------+
             │
             ▼
+---------------------------+
|   Persistent Storage      |
+---------------------------+
```

> **Architecture Note**
>
> User Interface tidak diperkenankan mengakses Persistent Storage secara langsung. Seluruh akses data harus melalui Service Layer dan Repository.

---

## 6.3 Primary Data Flow

Aliran data utama di dalam Learning Engine mengikuti urutan berikut:

```text
Learning Activity
        │
        ▼
Learning Service
        │
        ▼
Learning Repository
        │
        ▼
Persistent Storage
        │
        ▼
Learning Statistics
        │
        ▼
User Interface
```

Data selalu bergerak melalui jalur yang telah ditentukan oleh Architecture Contract.

---

## 6.4 Responsibilities by Layer

### User Interface

Bertanggung jawab terhadap:

* interaksi pengguna,
* penyajian informasi,
* navigasi aplikasi.

User Interface tidak mengandung logika bisnis Learning Engine.

---

### Learning Services

Bertanggung jawab terhadap:

* logika bisnis,
* koordinasi antar komponen,
* pengelolaan proses pembelajaran.

Learning Services menjadi titik masuk utama seluruh operasi Learning Engine.

---

### Learning Repository

Bertanggung jawab terhadap:

* membaca data,
* menyimpan data,
* mengelola persistensi.

Repository tidak menjalankan aturan bisnis maupun perhitungan statistik.

---

### Persistent Storage

Bertanggung jawab menyimpan data secara permanen.

Jenis media penyimpanan tidak dibatasi oleh kontrak arsitektur.

Reference Implementation menggunakan berkas JSON lokal.

---

## 6.5 Dependency Direction

Ketergantungan antar lapisan bersifat satu arah.

```text
User Interface
        │
        ▼
Learning Services
        │
        ▼
Learning Repository
        │
        ▼
Persistent Storage
```

Lapisan bawah tidak boleh memiliki ketergantungan terhadap lapisan di atasnya.

Pendekatan ini menjaga independensi setiap komponen serta mempermudah pengujian.

---

## 6.6 Architecture Boundaries

Learning Engine hanya bertanggung jawab terhadap pengelolaan perkembangan belajar pengguna.

Komponen berikut berada di luar batas tanggung jawab Learning Engine:

* Core Engine
* ScriptPack
* Rendering System
* Audio System
* Theme Management
* Localization
* Application Bootstrap

Hubungan dengan subsistem tersebut dilakukan melalui antarmuka publik yang telah disediakan masing-masing.

---

## 6.7 Reference Implementation

Reference Implementation pertama mengikuti struktur arsitektur yang didefinisikan pada bab ini.

Saat ini hanya Quiz Module yang memanfaatkan Learning Engine secara penuh.

Mode pembelajaran lainnya akan mengikuti struktur yang sama ketika diimplementasikan pada versi berikutnya.

------------------

# 7. Core Components

> **Docstring**
>
> Bab ini memperkenalkan komponen-komponen utama yang membentuk Learning Engine.
> Setiap komponen memiliki tanggung jawab yang spesifik dan saling bekerja sama melalui Architecture Contract yang telah ditetapkan.
> Bab ini hanya memberikan gambaran konseptual. Detail masing-masing komponen dijelaskan pada bab-bab berikutnya.

## 7.1 Overview

Learning Engine terdiri atas sejumlah komponen inti yang bekerja sama untuk mengelola proses pembelajaran pengguna.

Setiap komponen dirancang mengikuti prinsip *Single Responsibility*, sehingga memiliki tujuan dan tanggung jawab yang jelas.

Hubungan antar komponen membentuk alur pemrosesan data pembelajaran yang konsisten, mudah dipelihara, dan mudah dikembangkan.

---

## 7.2 Component Relationship

Komponen-komponen utama Learning Engine dapat digambarkan sebagai berikut:

```text
                  Learning Engine
                         │
     ┌───────────────────┼───────────────────┐
     │                   │                   │
     ▼                   ▼                   ▼
Learning Profile   Study Session   Learning Statistics
         │
         ▼
Learning Repository
         │
         ▼
Learning Services
```

> **Architecture Note**
>
> Diagram ini menunjukkan hubungan konseptual antar komponen, bukan hubungan implementasi maupun dependency pada bahasa pemrograman tertentu.

---

## 7.3 Learning Profile

Learning Profile merupakan representasi utama perkembangan belajar seorang pengguna.

Komponen ini menyimpan informasi agregat mengenai aktivitas pembelajaran dan menjadi identitas utama perjalanan belajar pengguna.

Learning Profile tidak menyimpan detail setiap aktivitas belajar.

---

## 7.4 Study Session

Study Session merepresentasikan satu sesi pembelajaran yang dilakukan oleh pengguna.

Seluruh aktivitas belajar direpresentasikan sebagai sebuah Study Session, terlepas dari jenis mode pembelajaran yang digunakan.

Pada Reference Implementation, seluruh Study Session berasal dari Quiz Module.

---

## 7.5 Learning Activity

Learning Activity mendeskripsikan jenis aktivitas yang dilakukan di dalam sebuah Study Session.

Learning Activity memungkinkan Learning Engine mendukung berbagai bentuk pembelajaran tanpa mengubah Architecture Contract.

Reference Implementation hanya mengimplementasikan Quiz sebagai Learning Activity pertama.

---

## 7.6 Learning Statistics

Learning Statistics menyediakan informasi ringkasan mengenai perkembangan belajar pengguna.

Seluruh statistik dihasilkan dari data yang tersimpan pada Learning Profile dan Study Session.

Learning Statistics bukan merupakan sumber data utama (*source of truth*).

---

## 7.7 Learning Repository

Learning Repository menyediakan mekanisme persistensi data bagi Learning Engine.

Repository bertanggung jawab terhadap proses penyimpanan dan pengambilan data tanpa mengandung logika bisnis.

Repository menjadi satu-satunya komponen yang berinteraksi langsung dengan media penyimpanan.

---

## 7.8 Learning Services

Learning Services mengoordinasikan seluruh proses bisnis di dalam Learning Engine.

Service Layer menjadi titik masuk utama bagi User Interface maupun subsistem lain yang ingin menggunakan Learning Engine.

Seluruh validasi, koordinasi, dan pengelolaan proses pembelajaran dilakukan melalui komponen ini.

---

## 7.9 Component Collaboration

Komponen-komponen Learning Engine bekerja sama melalui alur berikut:

```text
Learning Activity
        │
        ▼
Learning Service
        │
        ▼
Learning Repository
        │
        ▼
Learning Profile
        │
        ▼
Learning Statistics
        │
        ▼
User Interface
```

Setiap komponen hanya bertanggung jawab terhadap perannya masing-masing dan tidak mengambil alih tanggung jawab komponen lain.

---

## 7.10 Reference Implementation

Reference Implementation pertama menggunakan seluruh komponen yang didefinisikan pada bab ini.

Walaupun implementasinya saat ini hanya mendukung Quiz Module, struktur konseptual Learning Engine telah dirancang untuk mengakomodasi mode pembelajaran lain tanpa memerlukan perubahan terhadap Architecture Contract.

> **Implementation Note**
>
> Reference Implementation berfungsi sebagai pembuktian bahwa seluruh komponen inti dapat bekerja sesuai kontrak arsitektur, bukan sebagai representasi lengkap seluruh kemampuan Learning Engine.

------------------

# 8. Learning Profile

> **Docstring**
>
> Bab ini mendefinisikan konsep *Learning Profile* sebagai representasi utama perkembangan belajar pengguna di dalam Learning Engine.
> Learning Profile berfungsi sebagai identitas pembelajaran yang merangkum progres pengguna berdasarkan seluruh aktivitas belajar yang telah tercatat.
> Bab ini membahas konsep arsitektur Learning Profile tanpa bergantung pada implementasi maupun mekanisme penyimpanan data tertentu.

## 8.1 Purpose

Learning Profile merupakan representasi agregat mengenai perkembangan belajar seorang pengguna.

Komponen ini menyediakan *aggregated learning state* yang dapat digunakan oleh berbagai komponen Learning Engine untuk memperoleh ringkasan kondisi pembelajaran pengguna.

Learning Profile tidak merepresentasikan seluruh aktivitas pembelajaran secara individual. Riwayat aktivitas pembelajaran secara authoritative direpresentasikan oleh kumpulan Study Session.

---

## 8.2 Responsibilities

Learning Profile memiliki tanggung jawab sebagai berikut:

* Merepresentasikan *aggregated learning state* seorang learner.
* Menyediakan ringkasan perkembangan pembelajaran.
* Menyediakan informasi agregat bagi Learning Services.
* Menyediakan informasi agregat yang dapat digunakan oleh Statistics Services.
* Menjadi persisted aggregate yang dapat digunakan untuk kebutuhan akses dan presentasi.

Learning Profile tidak bertanggung jawab terhadap pencatatan aktivitas pembelajaran individual.

Learning Profile juga tidak menjadi Source of Truth untuk learning activity history. Riwayat aktivitas pembelajaran secara authoritative direpresentasikan oleh Study Session.

---

## 8.3 Conceptual Model

Secara konseptual, Learning Profile berada di atas seluruh Study Session yang dimiliki oleh seorang pengguna.

```text
                 Learning Profile
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
Learning Statistics              Study Sessions
                                         │
                           ┌─────────────┼─────────────┐
                           ▼             ▼             ▼
                       Session A     Session B     Session C
```

Learning Profile tidak memiliki ketergantungan terhadap jenis aktivitas belajar tertentu.

Seluruh informasi yang disimpan merupakan representasi umum dari perkembangan belajar pengguna.

---

## 8.4 Lifecycle

Siklus hidup Learning Profile terdiri atas beberapa tahap:

1. Dibuat ketika pengguna pertama kali menggunakan Learning Engine.
2. Diperbarui setiap kali Study Session selesai.
3. Digunakan sebagai sumber informasi oleh komponen lain.
4. Disimpan secara permanen melalui Learning Repository.

Learning Profile tetap ada selama data pembelajaran pengguna masih tersedia.

---

## 8.5 Relationships

Learning Profile memiliki hubungan konseptual dengan beberapa komponen Learning Engine.

| Component           | Relationship                                                             |
| ------------------- | ------------------------------------------------------------------------ |
| Study Session       | Menjadi sumber data perkembangan belajar.                                |
| Learning Statistics | Menghasilkan informasi statistik berdasarkan profil dan riwayat belajar. |
| Learning Repository | Menyimpan dan mengambil Learning Profile.                                |
| Learning Services   | Mengelola perubahan terhadap Learning Profile.                           |
| User Interface      | Menggunakan informasi profil untuk ditampilkan kepada pengguna.          |

Learning Profile tidak berhubungan langsung dengan media penyimpanan maupun User Interface.

---

## 8.6 Design Considerations

Perancangan Learning Profile mengikuti beberapa prinsip berikut:

* Ringkas dan mudah dipelihara.
* Tidak bergantung pada mode pembelajaran tertentu.
* Tidak menyimpan activity-specific payload.
* Merepresentasikan aggregated learning state.
* Dapat dipersist untuk efisiensi akses.
* Dapat direkonstruksi dari Study Session.
* Tidak menjadi Source of Truth untuk learning activity history.
* Dapat digunakan oleh berbagai platform aplikasi.

> **Architecture Note**
>
> Learning Profile merupakan *persisted derived aggregate*.
>
> Walaupun Learning Profile dapat disimpan secara permanen untuk efisiensi akses, informasi tersebut tidak mengubah statusnya menjadi Primary Data.
>
> Apabila diperlukan, Learning Profile harus dapat direkonstruksi berdasarkan Study Session yang merupakan authoritative source untuk learning activity history.

---

## 8.7 Reference Implementation

Reference Implementation pertama menggunakan Learning Profile untuk mendukung Quiz Module.

Pada implementasi ini, Learning Profile diperbarui setelah setiap Quiz selesai dan digunakan sebagai sumber informasi bagi Home Dashboard.

Walaupun implementasinya masih terbatas pada Quiz, struktur konseptual Learning Profile tidak memiliki ketergantungan terhadap Quiz sebagai satu-satunya mode pembelajaran.

> **Implementation Note**
>
> Reference Implementation menggunakan penyimpanan berbasis JSON lokal sebagai media persistensi Learning Profile.

---

## 8.8 Future Extensions

Learning Profile dirancang agar dapat berkembang tanpa mengubah Architecture Contract.

Contoh pengembangan yang telah diantisipasi meliputi:

* Flashcard Learning
* Writing Practice
* Listening Practice
* Adaptive Learning
* Achievement System
* Learning Recommendation
* Cloud Synchronization

Penambahan fitur-fitur tersebut diharapkan hanya memerlukan perluasan implementasi tanpa mengubah konsep dasar Learning Profile.

------------------

# 9. Study Session

> **Docstring**
>
> Bab ini mendefinisikan konsep *Study Session* sebagai representasi satu aktivitas belajar yang dilakukan oleh pengguna.
> Study Session merupakan unit dasar pencatatan aktivitas di dalam Learning Engine dan menjadi sumber utama data perkembangan pembelajaran.
> Bab ini menjelaskan struktur konseptual Study Session tanpa bergantung pada implementasi mode pembelajaran tertentu.

## 9.1 Purpose

Study Session merepresentasikan satu aktivitas pembelajaran yang telah diselesaikan oleh pengguna.

Setiap aktivitas pembelajaran yang menghasilkan perubahan terhadap learning state pengguna direpresentasikan sebagai sebuah Study Session.

Study Session merupakan **Primary Data** dan **authoritative source** untuk learning activity history di dalam Learning Engine.

Study Session tidak menyimpan informasi agregat yang dapat dihitung dari kumpulan Study Session.

Setiap Study Session wajib memiliki `learner_id` dan tidak boleh menjadi milik lebih dari satu learner. `learner_id` merupakan bagian dari identitas ownership Study Session, bukan sekadar metadata presentation.

---

## 9.2 Responsibilities

Study Session memiliki tanggung jawab sebagai berikut:

* Merepresentasikan satu aktivitas belajar.
* Menyimpan informasi mengenai satu sesi pembelajaran.
* Menyimpan identitas learner pemilik aktivitas melalui `learner_id`.
* Menjadi sumber data bagi Learning Profile.
* Menjadi sumber data bagi Learning Statistics.
* Menyediakan dasar bagi analisis perkembangan belajar.

Study Session tidak bertanggung jawab terhadap penyimpanan permanen maupun perhitungan statistik.

---

## 9.3 Conceptual Model

Learning Engine memperlakukan setiap aktivitas belajar sebagai sebuah Study Session.

```text
                 Learner Identity
                         │
                         ▼
                  Study Sessions
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
  Session 1         Session 2         Session 3
```

Setiap Study Session berdiri sendiri dan merepresentasikan satu periode pembelajaran.

---

## 9.4 Lifecycle

Siklus hidup Study Session terdiri atas beberapa tahap:

1. Aktivitas pembelajaran berlangsung di dalam Learning Activity Module.
2. Aktivitas menghasilkan hasil pembelajaran (*Activity Result*).
3. Setelah aktivitas selesai, Learning Service membentuk Study Session.
4. Study Session diberi Activity Classification dan Payload.
5. Study Session dipersist melalui Learning Repository.
6. Study Session menjadi bagian dari authoritative learning activity history.

Study Session pada Reference Implementation merepresentasikan aktivitas pembelajaran yang telah selesai.

Aktivitas yang sedang berlangsung tidak dianggap sebagai Study Session yang telah tersimpan.

---

## 9.5 Relationships

Study Session memiliki hubungan konseptual dengan beberapa komponen Learning Engine.

| Component           | Relationship                                                              |
| ------------------- | ------------------------------------------------------------------------- |
| Learner Identity    | Menentukan learner pemilik Study Session.                                 |
| Learning Profile    | Menjadi sumber data perkembangan belajar.                                 |
| Learning Statistics | Menjadi sumber perhitungan statistik.                                     |
| Learning Repository | Menyimpan dan mengambil Study Session.                                    |
| Learning Services   | Mengelola proses pembentukan Study Session.                               |
| Learning Activity   | Mendefinisikan jenis aktivitas yang direpresentasikan oleh Study Session. |

Study Session tidak memiliki ketergantungan langsung terhadap User Interface.

---

## 9.6 Design Considerations

Perancangan Study Session mengikuti prinsip-prinsip berikut:

* Merepresentasikan satu aktivitas pembelajaran yang telah selesai.
* Bersifat independen terhadap jenis pembelajaran.
* Dapat digunakan oleh berbagai mode pembelajaran.
* Merupakan Primary Data.
* Menjadi authoritative source untuk learning activity history.
* Tidak menyimpan informasi agregat yang dapat dihitung ulang.
* Memiliki ownership eksplisit melalui `learner_id`.
* Tidak bergantung pada Learning Profile sebagai sumber data utama.
* Dapat dipersist melalui Learning Repository.

> **Architecture Note**
>
> Study Session merupakan sumber data utama untuk riwayat aktivitas pembelajaran.
>
> Learning Profile dan Statistics dapat dibentuk atau diperbarui berdasarkan Study Session, tetapi keduanya bukan pengganti Study Session sebagai authoritative learning activity history.

> **Architecture Decision — AD-LE-014**
>
> Setiap Study Session dimiliki tepat satu learner melalui `learner_id`. Learning Repository menyediakan pengambilan Study Session secara learner-scoped.
>
> **Rationale**
>
> Explicit ownership menjaga isolasi data antar learner dalam satu instalasi aplikasi dan mencegah History atau consumer lain melakukan filtering ownership di luar Persistence Boundary.

---

## 9.7 Reference Implementation

Reference Implementation pertama menggunakan Study Session untuk merepresentasikan hasil Quiz.

Setiap penyelesaian Quiz menghasilkan satu Study Session baru yang kemudian diproses oleh Learning Engine.

Tidak ada jenis Study Session lain yang diimplementasikan pada versi pertama.

> **Implementation Note**
>
> Payload dari Study Session pada Reference Implementation berupa Quiz Result.

---

## 9.8 Future Extensions

Study Session dirancang agar mampu merepresentasikan berbagai aktivitas pembelajaran.

Contoh implementasi yang telah diantisipasi antara lain:

* Flashcard Session
* Writing Practice Session
* Listening Practice Session
* Matching Exercise Session
* Character Recognition Session

Seluruh implementasi tersebut diharapkan menggunakan struktur konseptual Study Session yang sama sehingga tidak memerlukan perubahan terhadap Architecture Contract.

------------------

# 10. Activity Classification

> **Docstring**
>
> Bab ini mendefinisikan konsep *Activity Classification* sebagai mekanisme klasifikasi aktivitas pembelajaran di dalam Learning Engine.
> Activity Classification digunakan untuk mengidentifikasi jenis aktivitas yang direpresentasikan oleh sebuah Study Session tanpa mengubah struktur konseptual Learning Engine.
> Bab ini tidak mendefinisikan implementasi mode pembelajaran tertentu, melainkan kontrak klasifikasi yang digunakan oleh seluruh Reference Implementation maupun Future Implementation.

## 10.1 Purpose

Activity Classification digunakan untuk mengidentifikasi jenis aktivitas pembelajaran yang direpresentasikan oleh sebuah Study Session.

Klasifikasi ini memungkinkan Learning Engine mendukung berbagai mode pembelajaran menggunakan struktur Study Session yang sama.

Dengan pendekatan ini, penambahan mode pembelajaran baru tidak memerlukan perubahan terhadap struktur konseptual Learning Engine.

---

## 10.2 Responsibilities

Activity Classification memiliki tanggung jawab sebagai berikut:

* Mengidentifikasi jenis aktivitas pembelajaran.
* Menentukan tipe payload yang berkaitan dengan sebuah Study Session.
* Menjadi dasar bagi Learning Services dalam memproses aktivitas pembelajaran.
* Menyediakan mekanisme klasifikasi yang konsisten bagi seluruh mode pembelajaran.

Activity Classification tidak bertanggung jawab terhadap penyimpanan data, logika bisnis, maupun representasi User Interface.

---

## 10.3 Conceptual Model

Setiap Study Session memiliki satu Activity Classification.

```text
              Study Session
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
 Activity Classification      Payload
```

Activity Classification mendeskripsikan **jenis** aktivitas, sedangkan payload menyimpan **hasil** aktivitas tersebut.

> **Architecture Decision — AD-LE-004**
>
> Activity Classification direpresentasikan sebagai atribut konseptual dari Study Session, bukan sebagai komponen arsitektur yang berdiri sendiri.
>
> **Rationale**
>
> Pendekatan ini menjaga struktur Learning Engine tetap sederhana, mengurangi jumlah model yang harus dipelajari, serta memungkinkan seluruh mode pembelajaran menggunakan struktur Study Session yang sama.

---

## 10.4 Classification Contract

Architecture Contract menetapkan bahwa setiap Study Session harus memiliki tepat satu Activity Classification.

Setiap Activity Classification SHALL memiliki Payload yang kompatibel dengan klasifikasi tersebut.

Activity Classification digunakan untuk menentukan jenis aktivitas pembelajaran yang direpresentasikan oleh Study Session, sedangkan Payload menyimpan hasil spesifik dari aktivitas tersebut.

Dokumen ini tidak membatasi jumlah maupun jenis Activity Classification yang dapat digunakan oleh implementasi.

Reference Implementation maupun Future Implementation dapat menambahkan klasifikasi baru selama tetap mematuhi kontrak Learning Engine.

> **Architecture Rule**
>
> Activity Classification SHALL be compatible with the Payload associated with the Study Session.
>
> Sebuah Study Session tidak boleh memiliki kombinasi Activity Classification dan Payload yang tidak sesuai.

---

## 10.5 Relationships

Activity Classification memiliki hubungan konseptual dengan komponen berikut.

| Component           | Relationship                                                        |
| ------------------- | ------------------------------------------------------------------- |
| Study Session       | Mengidentifikasi jenis aktivitas yang direpresentasikan.            |
| Payload             | Menentukan struktur hasil aktivitas yang terkait.                   |
| Learning Services   | Digunakan untuk menentukan alur pemrosesan aktivitas.               |
| Learning Statistics | Dapat digunakan sebagai dasar pengelompokan statistik pembelajaran. |

---

## 10.6 Design Considerations

Perancangan Activity Classification mengikuti prinsip berikut:

* Tidak bergantung pada implementasi tertentu.
* Dapat diperluas tanpa mengubah Architecture Contract.
* Tidak memengaruhi struktur Study Session.
* Tidak mengubah mekanisme Learning Repository.
* Tidak memengaruhi Learning Profile maupun Learning Statistics.

Dengan pendekatan ini, seluruh perluasan sistem dilakukan melalui penambahan klasifikasi dan payload baru, bukan melalui perubahan struktur inti Learning Engine.

---

## 10.7 Reference Implementation

Reference Implementation pertama hanya mendefinisikan satu Activity Classification.

```text
QUIZ
```

Activity Classification tersebut digunakan oleh seluruh Study Session yang dihasilkan oleh Quiz Module.

> **Implementation Note**
>
> Walaupun hanya terdapat satu Activity Classification pada Reference Implementation, kontrak arsitektur telah dirancang untuk mendukung penambahan klasifikasi lain tanpa perubahan terhadap struktur konseptual Learning Engine.

---

## 10.8 Future Extensions

Contoh Activity Classification yang telah diantisipasi antara lain:

```text
FLASHCARD

WRITING

LISTENING

MATCHING

TRANSLITERATION

CHARACTER_RECOGNITION
```

Setiap klasifikasi baru diharapkan memiliki payload yang sesuai dengan kebutuhan mode pembelajaran masing-masing.

Penambahan Activity Classification tidak memerlukan perubahan terhadap Learning Profile, Study Session, Learning Repository, maupun Learning Statistics selama tetap mengikuti Architecture Contract.

------------------

# 11. Payload Model

> **Docstring**
>
> Bab ini mendefinisikan konsep *Payload Model* sebagai mekanisme untuk membawa hasil spesifik dari sebuah aktivitas pembelajaran di dalam Study Session.
> Payload Model memungkinkan Learning Engine tetap bersifat umum (*activity-agnostic*), sementara setiap mode pembelajaran dapat memiliki struktur data hasil yang berbeda.
> Bab ini mendefinisikan kontrak konseptual Payload tanpa bergantung pada implementasi Python maupun jenis aktivitas pembelajaran tertentu.

## 11.1 Purpose

Payload merupakan representasi hasil dari sebuah aktivitas pembelajaran.

Setiap Study Session memiliki tepat satu Payload yang menyimpan data spesifik sesuai Activity Classification yang dimiliki oleh Study Session tersebut.

Payload memungkinkan Learning Engine mengelola berbagai mode pembelajaran tanpa harus mengetahui struktur internal masing-masing mode.

---

## 11.2 Responsibilities

Payload memiliki tanggung jawab sebagai berikut:

* Menyimpan hasil spesifik dari satu aktivitas pembelajaran.
* Menjadi representasi data yang diproses oleh Learning Services.
* Menjadi sumber informasi detail bagi Study Session.
* Menyediakan informasi yang diperlukan untuk membangun Learning Profile dan Learning Statistics.

Payload tidak bertanggung jawab terhadap:

* persistensi data,
* logika bisnis,
* statistik,
* identitas pengguna.

---

## 11.3 Conceptual Model

Secara konseptual, Payload merupakan bagian dari sebuah Study Session.

```text
                 Study Session
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
 Activity Classification         Payload
```

Study Session bertanggung jawab terhadap identitas sesi pembelajaran.

Payload bertanggung jawab terhadap hasil aktivitas pembelajaran.

---

## 11.4 Payload Contract

Architecture Contract menetapkan aturan berikut:

* Setiap Study Session memiliki tepat satu Payload.
* Payload harus sesuai dengan Activity Classification.
* Payload harus merepresentasikan hasil dari aktivitas yang diklasifikasikan oleh Activity Classification tersebut.
* Payload tidak boleh digunakan di luar konteks Study Session.
* Learning Engine tidak bergantung pada struktur internal Payload.

Hubungan konseptual antara Activity Classification dan Payload adalah:

```text
Activity Classification
          │
          │ determines
          ▼
     Payload Type
```

Contoh:

```text
QUIZ
  └── QuizResult

FLASHCARD
  └── FlashcardResult

WRITING
  └── WritingResult
```

> **Architecture Note**
>
> Activity Classification dan Payload merupakan pasangan konseptual di dalam Study Session. Classification menjelaskan **jenis aktivitas**, sedangkan Payload menjelaskan **hasil aktivitas**.

---

## 11.5 Relationships

Payload memiliki hubungan konseptual dengan komponen berikut.

| Component               | Relationship                                              |
| ----------------------- | --------------------------------------------------------- |
| Study Session           | Dimiliki oleh satu Study Session.                         |
| Activity Classification | Menentukan jenis Payload yang digunakan.                  |
| Learning Services       | Memproses Payload sesuai kebutuhan bisnis.                |
| Learning Statistics     | Menggunakan informasi Payload untuk menghitung statistik. |

Payload tidak memiliki hubungan langsung dengan User Interface maupun Persistent Storage.

---

## 11.6 Design Considerations

Perancangan Payload mengikuti prinsip berikut:

* Activity-specific.
* Extensible.
* Independent.
* Serializable.
* Self-contained.

Learning Engine hanya mengetahui keberadaan Payload, tetapi tidak bergantung pada struktur internalnya.

---

## 11.7 Reference Implementation

Reference Implementation pertama hanya menggunakan satu jenis Payload.

```text
QuizResult
```

Seluruh Study Session pada versi pertama menggunakan QuizResult sebagai Payload.

> **Implementation Note**
>
> Struktur QuizResult dijelaskan pada dokumentasi implementasi dan bukan merupakan bagian dari Architecture Contract.

---

## 11.8 Future Extensions

Contoh Payload yang telah diantisipasi antara lain:

```text
QuizResult
FlashcardResult
WritingResult
ListeningResult
MatchingResult
RecognitionResult
```

Setiap Payload baru harus memiliki Activity Classification yang sesuai.

Contoh:

```text
FLASHCARD → FlashcardResult
WRITING   → WritingResult
LISTENING → ListeningResult
```

Penambahan Payload baru tidak memerlukan perubahan terhadap:

* Learning Profile
* Study Session
* Learning Repository
* Learning Services
* Statistics Services

selama Payload dan Activity Classification tetap memenuhi Architecture Contract.

---

## 11.9 Summary

Payload merupakan mekanisme yang memungkinkan Learning Engine tetap bersifat generik sementara setiap mode pembelajaran bebas memiliki struktur data hasil yang sesuai dengan kebutuhannya.

Dengan pendekatan ini, kontrak arsitektur tetap stabil walaupun jumlah mode pembelajaran terus bertambah.

------------------

# 12. Learning Repository

> **Docstring**
>
> Bab ini mendefinisikan konsep *Learning Repository* sebagai lapisan persistensi (*Persistence Layer*) di dalam Learning Engine.
> Learning Repository bertanggung jawab terhadap penyimpanan dan pengambilan data pembelajaran tanpa mengandung logika bisnis maupun logika presentasi.
> Bab ini mendefinisikan kontrak konseptual Repository dan tidak bergantung pada mekanisme penyimpanan data tertentu.

## 12.1 Purpose

Learning Repository menyediakan mekanisme persistensi bagi seluruh data yang dikelola oleh Learning Engine.

Repository menjadi satu-satunya komponen yang diperbolehkan berinteraksi langsung dengan media penyimpanan.

Dengan pendekatan ini, perubahan mekanisme penyimpanan tidak memengaruhi komponen lain di dalam Learning Engine.

---

## 12.2 Responsibilities

Learning Repository memiliki tanggung jawab sebagai berikut:

* Menyimpan Learning Profile.
* Mengambil Learning Profile.
* Menyimpan Study Session.
* Mengambil Study Session.
* Menyediakan mekanisme persistensi yang konsisten.
* Menyembunyikan detail implementasi media penyimpanan.

Learning Repository tidak bertanggung jawab terhadap:

* logika bisnis,
* validasi pembelajaran,
* perhitungan statistik,
* pembentukan User Interface.

---

## 12.3 Conceptual Model

Repository berada di antara Service Layer dan Persistent Storage.

```text
               Learning Services
                      │
                      ▼
            Learning Repository
                      │
                      ▼
             Persistent Storage
```

Repository bertindak sebagai batas (*boundary*) antara domain Learning Engine dan media penyimpanan.

---

## 12.4 Repository Contract

Learning Repository harus menyediakan kemampuan konseptual berikut:

* Menyimpan Learning Profile.
* Mengambil Learning Profile.
* Menyimpan Study Session.
* Mengambil Study Session untuk learner tertentu.
* Menyediakan operasi pembaruan data secara konsisten.

Pengambilan Study Session secara learner-scoped merupakan tanggung jawab Repository. Consumer tidak boleh mengambil seluruh collection lalu melakukan filtering ownership sendiri.

Dokumen ini tidak mendefinisikan nama metode, struktur kelas, maupun bahasa pemrograman yang digunakan.

> **Architecture Decision — AD-LE-006**
>
> Seluruh operasi persistensi Learning Engine harus dilakukan melalui Learning Repository.
>
> **Rationale**
>
> Repository menjadi satu-satunya batas terhadap media penyimpanan sehingga perubahan implementasi storage tidak memengaruhi Service Layer maupun komponen lainnya.

---

## 12.5 Relationships

Learning Repository memiliki hubungan konseptual dengan:

| Component          | Relationship                                              |
| ------------------ | --------------------------------------------------------- |
| Learning Services  | Menggunakan Repository untuk seluruh operasi persistensi. |
| Learning Profile   | Disimpan dan diambil melalui Repository.                  |
| Study Session      | Disimpan dan diambil melalui Repository dengan learner ownership. |
| Persistent Storage | Menjadi media penyimpanan yang digunakan Repository.      |

Repository tidak memiliki hubungan langsung dengan User Interface.

Repository SHALL menyediakan learner-scoped retrieval untuk Study Session. Consumer meminta data berdasarkan `learner_id` dan tidak melakukan filtering ownership sendiri.

---

## 12.6 Design Considerations

Learning Repository dirancang berdasarkan prinsip berikut:

* Single Responsibility.
* Storage-independent.
* Replaceable.
* Testable.
* Consistent.

Repository hanya mengetahui bagaimana data disimpan dan diambil.

Repository tidak mengetahui bagaimana data digunakan.

---

## 12.7 Reference Implementation

Reference Implementation menggunakan penyimpanan berbasis berkas JSON lokal.

Seluruh operasi penyimpanan dan pengambilan data dilakukan melalui implementasi Repository yang mematuhi kontrak pada dokumen ini.

> **Implementation Note**
>
> Penggunaan JSON merupakan keputusan implementasi dan bukan bagian dari Architecture Contract.

---

## 12.8 Future Extensions

Kontrak Repository telah dirancang agar dapat mendukung berbagai mekanisme penyimpanan, antara lain:

* SQLite
* PostgreSQL
* Cloud Storage
* REST API
* Remote Synchronization

Selama implementasi memenuhi kontrak Repository, perubahan media penyimpanan tidak memerlukan perubahan terhadap komponen lain di dalam Learning Engine.

---

## 12.9 Summary

Learning Repository merupakan satu-satunya komponen yang bertanggung jawab terhadap persistensi data.

Seluruh komponen lain harus mengakses media penyimpanan melalui Repository sesuai dengan kontrak arsitektur yang telah ditetapkan.

------------------

# 13. Learning Services

> **Docstring**
>
> Bab ini mendefinisikan konsep *Learning Services* sebagai lapisan logika bisnis (*Business Logic Layer*) di dalam Learning Engine.
> Learning Services bertanggung jawab mengoordinasikan seluruh proses pembelajaran, mengelola interaksi antar komponen, serta memastikan seluruh operasi mengikuti Architecture Contract.
> Bab ini mendefinisikan tanggung jawab konseptual Service Layer dan tidak bergantung pada implementasi bahasa pemrograman maupun framework tertentu.

## 13.1 Purpose

Learning Services merupakan titik masuk utama (*Entry Point*) bagi seluruh operasi Learning Engine.

Seluruh aktivitas pembelajaran diproses melalui Service Layer sebelum disimpan maupun digunakan oleh komponen lain.

Dengan pendekatan ini, seluruh logika bisnis berada pada satu lapisan yang konsisten dan dapat digunakan kembali oleh berbagai antarmuka aplikasi.

---

## 13.2 Responsibilities

Learning Services memiliki tanggung jawab sebagai berikut:

* Mengelola alur pembelajaran.
* Membuat Study Session.
* Memproses Payload.
* Memperbarui Learning Profile.
* Memanggil Learning Repository.
* Menyediakan layanan bagi User Interface.

Learning Services tidak bertanggung jawab terhadap:

* penyimpanan data,
* representasi User Interface,
* implementasi media penyimpanan.

---

## 13.3 Conceptual Model

Learning Services menghubungkan seluruh komponen Learning Engine.

```text
             User Interface
                    │
                    ▼
          Learning Services
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
Study Session  Learning Profile  Repository
```

Seluruh operasi pembelajaran melewati Learning Services.

---

## 13.4 Service Contract

Architecture Contract menetapkan bahwa:

* User Interface tidak boleh mengakses Repository secara langsung.
* User Interface tidak boleh memodifikasi Learning Profile secara langsung.
* User Interface tidak boleh membuat maupun menyimpan Study Session secara langsung.

Seluruh operasi tersebut harus dilakukan melalui Learning Services.

> **Architecture Decision — AD-LE-007**
>
> Learning Services merupakan satu-satunya pintu masuk terhadap logika bisnis Learning Engine.
>
> **Rationale**
>
> Pemusatan logika bisnis menjaga konsistensi proses pembelajaran, mempermudah pengujian, dan menghindari duplikasi logika pada berbagai antarmuka aplikasi.

---

## 13.5 Relationships

Learning Services memiliki hubungan konseptual dengan:

| Component           | Relationship                                             |
| ------------------- | -------------------------------------------------------- |
| User Interface      | Menggunakan Service sebagai titik masuk seluruh operasi. |
| Study Session       | Dibentuk dan diproses melalui Service.                   |
| Payload             | Diproses sesuai Activity Classification.                 |
| Learning Profile    | Diperbarui berdasarkan hasil Study Session.              |
| Learning Repository | Digunakan untuk seluruh operasi persistensi.             |
| Learning Statistics | Menggunakan data yang telah diproses oleh Service.       |

---

## 13.6 Processing Flow

Secara konseptual, alur pemrosesan Learning Engine adalah sebagai berikut:

```text
User Interface
        │
        ▼
Learning Services
        │
        ▼
Create Study Session
        │
        ▼
Process Payload
        │
        ▼
Update Learning Profile
        │
        ▼
Save using Repository
        │
        ▼
Return Updated State
```

Service Layer mengoordinasikan seluruh tahapan tersebut tanpa mengetahui detail implementasi media penyimpanan.

---

## 13.7 Design Considerations

Learning Services dirancang berdasarkan prinsip berikut:

* Business Logic Only.
* Repository Independent.
* UI Independent.
* Activity-Agnostic.
* Extensible.
* Testable.

Learning Services tidak bergantung pada jenis Activity Classification tertentu.

---

## 13.8 Reference Implementation

Reference Implementation pertama menggunakan Learning Services untuk memproses hasil Quiz.

Setelah pengguna menyelesaikan Quiz, Learning Services:

1. Membentuk Study Session.
2. Mengaitkan Activity Classification.
3. Menyimpan Payload.
4. Memperbarui Learning Profile.
5. Menyimpan perubahan melalui Learning Repository.

> **Implementation Note**
>
> Pada Reference Implementation, seluruh operasi Learning Engine berasal dari Quiz Module.

---

## 13.9 Future Extensions

Learning Services dirancang untuk mendukung penambahan layanan baru tanpa mengubah Architecture Contract.

Contoh perluasan implementasi:

* Flashcard Service
* Writing Service
* Listening Service
* Recommendation Service
* Achievement Service
* Synchronization Service

Seluruh layanan tersebut diharapkan menjadi implementasi tambahan yang mengikuti kontrak Service Layer yang sama.

---

## 13.10 Summary

Learning Services merupakan pusat logika bisnis Learning Engine.

Seluruh aktivitas pembelajaran diproses melalui Service Layer sehingga komponen lain tetap memiliki tanggung jawab yang jelas sesuai Architecture Contract.

------------------

# 14. Statistics Services

> **Docstring**
>
> Bab ini mendefinisikan konsep *Statistics Services* sebagai layanan yang menghasilkan informasi statistik berdasarkan data pembelajaran yang dikelola oleh Learning Engine.
> Statistics Services tidak menyimpan data maupun menjadi sumber kebenaran (*Source of Truth*), melainkan menghasilkan informasi turunan (*Derived Data*) yang digunakan oleh komponen lain.
> Bab ini mendefinisikan kontrak konseptual Statistics Services tanpa bergantung pada algoritma perhitungan maupun implementasi tertentu.

## 14.1 Purpose

Statistics Services menyediakan informasi statistik mengenai perkembangan belajar pengguna.

Seluruh statistik dihasilkan berdasarkan data yang terdapat pada Learning Profile dan Study Session.

Statistics Services tidak memiliki penyimpanan data sendiri.

---

## 14.2 Responsibilities

Statistics Services memiliki tanggung jawab sebagai berikut:

* Menghasilkan statistik pembelajaran.
* Menghitung indikator perkembangan belajar.
* Menyediakan ringkasan pembelajaran.
* Menyediakan informasi bagi User Interface.
* Menyediakan informasi bagi layanan lain yang memerlukan analisis pembelajaran.

Statistics Services tidak bertanggung jawab terhadap:

* penyimpanan data,
* pembentukan Study Session,
* perubahan Learning Profile.

---

## 14.3 Conceptual Model

Statistics Services menghasilkan informasi berdasarkan data yang telah tersedia.

```text
              Study Session
                     │
                     ▼
            Learning Profile
                     │
                     ▼
          Statistics Services
                     │
                     ▼
          Statistics Information
```

Statistics merupakan hasil pemrosesan, bukan data utama yang disimpan.

> **Architecture Decision — AD-LE-008**
>
> Statistics merupakan *Derived Data* yang dihasilkan berdasarkan Source of Truth.
>
> **Rationale**
>
> Dengan tidak menyimpan statistik sebagai data permanen, risiko inkonsistensi dapat dihindari dan seluruh informasi statistik selalu dapat dihitung ulang.

---

## 14.4 Statistics Contract

Statistics Services bertanggung jawab menghasilkan informasi statistik tanpa mengubah data pembelajaran.

Architecture Contract hanya menetapkan bahwa statistik harus dapat dihasilkan dari Source of Truth.

Kontrak ini tidak menentukan rumus maupun algoritma yang digunakan.

---

## 14.5 Relationships

Statistics Services memiliki hubungan konseptual dengan:

| Component         | Relationship                                     |
| ----------------- | ------------------------------------------------ |
| Study Session     | Menjadi sumber utama data statistik.             |
| Learning Profile  | Menyediakan informasi agregat yang diperlukan.   |
| Learning Services | Memanggil Statistics Services ketika diperlukan. |
| User Interface    | Menampilkan informasi statistik kepada pengguna. |

Statistics Services tidak memiliki hubungan langsung dengan Persistent Storage.

---

## 14.6 Design Considerations

Statistics Services mengikuti prinsip-prinsip berikut:

* Stateless.
* Read-only.
* Deterministic.
* Derived Data Only.
* Independent.
* Testable.

Statistics Services tidak boleh menghasilkan perubahan terhadap Source of Truth.

---

## 14.7 Reference Implementation

Reference Implementation menghasilkan statistik dasar yang digunakan oleh Home Dashboard.

Contoh statistik yang dapat disediakan:

* Total Quiz.
* Total Questions.
* Correct Answers.
* Incorrect Answers.
* Overall Accuracy.
* Last Study Date.

Daftar tersebut merupakan implementasi awal dan bukan bagian dari Architecture Contract.

> **Implementation Note**
>
> Reference Implementation hanya menghitung statistik yang diperlukan oleh Quiz Module dan Home Dashboard.

---

## 14.8 Future Extensions

Statistics Services dirancang agar dapat mendukung berbagai analisis pembelajaran tambahan, antara lain:

* Study Streak.
* Learning Trend.
* Weak Characters.
* Mastery Analysis.
* Learning Distribution.
* Recommendation Metrics.
* Achievement Metrics.

Seluruh perluasan tersebut diharapkan menjadi implementasi baru tanpa mengubah Architecture Contract.

---

## 14.9 Summary

Statistics Services merupakan layanan analisis yang menghasilkan informasi berdasarkan Source of Truth.

Statistics bukan bagian dari model data Learning Engine dan tidak disimpan sebagai data permanen.

Dengan pendekatan ini, konsistensi data tetap terjaga sementara kemampuan analisis dapat terus berkembang tanpa mengubah struktur inti Learning Engine.

------------------

# 15. Data Storage

> **Docstring**
>
> Bab ini mendefinisikan kontrak konseptual penyimpanan data (*Data Storage*) yang digunakan oleh Learning Engine.
> Data Storage menyediakan media persistensi bagi seluruh data pembelajaran tanpa membatasi teknologi, format, maupun lokasi penyimpanan.
> Bab ini hanya mendefinisikan kebutuhan arsitektur terhadap mekanisme penyimpanan data dan tidak membahas implementasi tertentu.

## 15.1 Purpose

Data Storage menyediakan media penyimpanan permanen bagi seluruh informasi yang dikelola oleh Learning Engine.

Learning Engine tidak memiliki ketergantungan terhadap jenis media penyimpanan tertentu.

Seluruh interaksi dengan Data Storage dilakukan melalui Learning Repository.

---

## 15.2 Responsibilities

Data Storage memiliki tanggung jawab sebagai berikut:

* Menyediakan media persistensi.
* Menjamin keberlangsungan data antar sesi aplikasi.
* Menyediakan mekanisme penyimpanan yang konsisten.
* Menyimpan data sebagaimana diminta oleh Learning Repository.

Data Storage tidak bertanggung jawab terhadap:

* logika bisnis,
* statistik,
* validasi,
* representasi User Interface.

---

## 15.3 Conceptual Model

Secara konseptual, Data Storage berada di bawah Learning Repository dan diakses melalui Storage Adapter.

```text
Learning Services
        │
        ▼
Learning Repository
        │
        ▼
Storage Adapter
        │
        ▼
Persistent Storage
```

Learning Repository menyediakan abstraksi persistensi kepada Learning Engine, sedangkan Storage Adapter memisahkan Repository dari teknologi penyimpanan tertentu.

Persistent Storage merupakan media penyimpanan aktual yang digunakan oleh implementasi.

---

## 15.4 Storage Contract

Architecture Contract menetapkan bahwa Data Storage harus mampu menyimpan informasi berikut:

* Learning Profile
* Study Session Collection dengan learner ownership eksplisit

Kontrak ini tidak menentukan:

* struktur berkas,
* nama berkas,
* format serialisasi,
* jenis basis data,
* lokasi penyimpanan.

> **Architecture Decision — AD-LE-009**
>
> Learning Engine tidak bergantung pada teknologi penyimpanan tertentu.
>
> **Rationale**
>
> Pemisahan antara kontrak dan implementasi memungkinkan perubahan media penyimpanan tanpa memengaruhi Domain Model maupun Business Logic.

---

## 15.5 Relationships

| Component           | Relationship                                                          |
| ------------------- | --------------------------------------------------------------------- |
| Learning Repository | Menggunakan Storage Adapter untuk mengakses media penyimpanan.        |
| Storage Adapter     | Menyediakan abstraksi terhadap teknologi Persistent Storage.          |
| Learning Profile    | Disimpan melalui Learning Repository.                                 |
| Study Session       | Disimpan melalui Learning Repository.                                 |
| Persistent Storage  | Menjadi media penyimpanan aktual yang digunakan oleh Storage Adapter. |

Data Storage tidak memiliki hubungan langsung dengan:

* User Interface
* Learning Services
* Statistics Services

---

## 15.6 Design Considerations

Perancangan Data Storage mengikuti prinsip-prinsip berikut:

* Storage Independent.
* Replaceable.
* Persistent.
* Consistent.
* Serializable.
* Technology Independent.

Pemisahan antara Repository, Storage Adapter, dan Persistent Storage memungkinkan setiap lapisan memiliki tanggung jawab yang jelas:

```text
Learning Repository
    Persistence abstraction

Storage Adapter
    Storage technology abstraction

Persistent Storage
    Actual persistence mechanism
```

Perubahan teknologi penyimpanan tidak boleh memengaruhi Domain Model maupun Business Logic.

---

## 15.7 Reference Implementation

Reference Implementation pertama menggunakan penyimpanan berbasis berkas JSON lokal.

Struktur konseptualnya adalah:

```text
Learning Repository
        │
        ▼
Storage Adapter
        │
        ▼
JSON Storage
```

Penggunaan JSON merupakan keputusan implementasi dan tidak menjadi bagian dari Architecture Contract.

> **Implementation Note**
>
> Implementasi Storage Adapter dapat diganti dengan adapter untuk SQLite, PostgreSQL, cloud storage, maupun mekanisme penyimpanan lainnya tanpa mengubah Domain Model maupun Business Logic.

---

## 15.8 Future Extensions

Kontrak Data Storage telah dirancang untuk mendukung berbagai mekanisme penyimpanan, termasuk namun tidak terbatas pada:

* SQLite
* Relational Database
* NoSQL Database
* Cloud Storage
* Remote Synchronization
* Hybrid Storage

Perubahan mekanisme penyimpanan tidak diharapkan memerlukan perubahan terhadap Architecture Contract.

---

## 15.9 Summary

Data Storage merupakan media persistensi konseptual bagi Learning Engine.

Kontrak arsitektur hanya mendefinisikan kebutuhan penyimpanan data, sedangkan teknologi penyimpanan ditentukan sepenuhnya oleh implementasi yang dipilih.

------------------

# 16. Domain Model

> **Docstring**
>
> Bab ini mendefinisikan Domain Model konseptual yang digunakan oleh Learning Engine.
> Domain Model menggambarkan objek-objek utama yang menjadi bagian dari Architecture Contract beserta hubungan konseptual di antaranya.
> Bab ini tidak mendefinisikan implementasi kelas, struktur berkas, maupun bahasa pemrograman tertentu.

## 16.1 Purpose

Domain Model menyediakan representasi konseptual terhadap objek-objek utama yang dikelola oleh Learning Engine.

Model ini menjadi acuan bagi seluruh implementasi sehingga setiap implementasi memiliki pemahaman yang sama mengenai struktur domain pembelajaran.

Domain Model tidak mendefinisikan implementasi teknis maupun struktur kode.

---

## 16.2 Domain Overview

Learning Engine terdiri atas dua kelompok utama:

* **Primary Domain**
* **Supporting Domain**

Primary Domain merupakan sumber utama informasi pembelajaran.

Supporting Domain menyediakan layanan yang mendukung pengelolaan Primary Domain.

---

## 16.3 Primary Domain

Primary Domain terdiri atas objek-objek berikut.

```text
Learner Identity

Learning Profile

Study Session

Activity Classification

Payload
```

Objek-objek tersebut membentuk inti Domain Model Learning Engine.

> **Architecture Note**
>
> Primary Domain merupakan bagian dari Architecture Contract dan menjadi fondasi seluruh mode pembelajaran.

---

## 16.4 Supporting Domain

Supporting Domain terdiri atas komponen berikut.

```text
Learning Services

Statistics Services

Learning Repository

Data Storage
```

Supporting Domain menyediakan layanan yang mengelola Primary Domain, tetapi bukan merupakan bagian dari data pembelajaran itu sendiri.

---

## 16.5 Domain Relationships

Hubungan konseptual antar Domain Model digambarkan sebagai berikut.

```text
                    Learner Identity
                           │
                           ▼
                    Study Session *
                           │
                     derived into
                           ▼
                    Learning Profile
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
Activity Classification              Payload
```

Keterangan:

* Satu Learning Profile merepresentasikan perkembangan belajar seorang learner.
* Setiap Study Session dimiliki tepat satu learner melalui `learner_id`.
* Satu Learning Profile dibentuk dari banyak Study Session milik learner yang sama.
* Setiap Study Session memiliki tepat satu Activity Classification.
* Setiap Study Session memiliki tepat satu Payload.

---

## 16.6 Domain Boundaries

Learning Engine hanya mengelola Domain Model yang didefinisikan pada dokumen ini.

Komponen berikut berada di luar Domain Model Learning Engine:

* User Interface
* Core Engine
* ScriptPack
* Rendering System
* Audio System

Interaksi dengan komponen tersebut dilakukan melalui Service Layer.

---

## 16.7 Domain Rules

Architecture Contract menetapkan aturan berikut.

* Learning Profile merupakan representasi agregat seorang learner.
* Study Session merupakan Source of Truth dan memiliki ownership eksplisit melalui `learner_id`.
* Activity Classification mengidentifikasi jenis aktivitas.
* Payload menyimpan hasil spesifik aktivitas.
* Repository tidak mengandung logika bisnis.
* Statistics merupakan Derived Data.

> **Architecture Decision — AD-LE-010**
>
> Domain Model Learning Engine dipisahkan secara tegas dari Service Layer dan Persistence Layer.
>
> **Rationale**
>
> Pemisahan ini menjaga independensi Domain Model sehingga perubahan pada implementasi layanan maupun media penyimpanan tidak memengaruhi struktur konseptual domain.

---

## 16.8 Domain Evolution

Domain Model dirancang agar dapat berkembang melalui penambahan Activity Classification maupun Payload baru.

Perluasan tersebut tidak diharapkan mengubah struktur konseptual Domain Model.

Dengan demikian, Learning Engine dapat mendukung mode pembelajaran baru tanpa melakukan perubahan terhadap Architecture Contract.

---

## 16.9 Reference Implementation

Reference Implementation pertama menggunakan Domain Model berikut.

```text
Learning Profile

Study Session

Activity Classification
    └── QUIZ

Payload
    └── QuizResult
```

Reference Implementation hanya merealisasikan sebagian kemampuan Domain Model yang didefinisikan oleh dokumen ini.

> **Implementation Note**
>
> Flashcard, Writing Practice, Listening Practice, dan mode pembelajaran lainnya akan menjadi implementasi tambahan pada versi mendatang tanpa mengubah Domain Model.

---

## 16.10 Summary

Domain Model merupakan representasi konseptual dari objek-objek utama Learning Engine.

Seluruh implementasi diharapkan mematuhi hubungan, tanggung jawab, dan batasan yang telah didefinisikan pada bab ini sehingga Architecture Contract tetap konsisten sepanjang evolusi proyek.

------------------

# 17. Versioning

> **Docstring**
>
> Bab ini mendefinisikan mekanisme versioning yang digunakan oleh Learning Engine Architecture.
> Versioning bertujuan menjaga kompatibilitas antar implementasi serta menyediakan mekanisme evolusi kontrak arsitektur tanpa mengorbankan implementasi yang telah ada.
> Bab ini mendefinisikan prinsip versioning secara konseptual dan tidak bergantung pada implementasi tertentu.

## 17.1 Purpose

Versioning menyediakan mekanisme untuk mengelola evolusi Learning Engine secara terstruktur.

Dengan adanya versioning, perubahan terhadap implementasi dapat dilakukan secara bertahap tanpa mengganggu kompatibilitas antar versi.

Versioning juga menjadi acuan ketika dilakukan migrasi data maupun penambahan kemampuan baru pada Learning Engine.

---

## 17.2 Architecture Version

Architecture Version merepresentasikan versi Architecture Contract.

Perubahan terhadap Architecture Version hanya dilakukan apabila terjadi perubahan terhadap Architecture Contract.

Perubahan implementasi yang tetap mematuhi kontrak tidak memerlukan perubahan Architecture Version.

---

## 17.3 Reference Implementation Version

Reference Implementation Version merepresentasikan versi implementasi yang merealisasikan Architecture Contract.

Reference Implementation Version dapat berkembang secara independen selama implementasi tetap mematuhi Architecture Contract.

---

## 17.4 Storage Version

Storage Version merepresentasikan versi format atau struktur data pada Persistent Storage.

Storage Version dapat berubah secara independen dari Architecture Version maupun Reference Implementation Version.

---

## 17.5 Compatibility Rules

Learning Engine mengikuti aturan kompatibilitas berikut:

* Architecture Contract bersifat stabil.
* Reference Implementation dapat berkembang secara bertahap.
* Storage dapat berubah tanpa mengubah Domain Model.
* Penambahan Activity Classification tidak mengubah kontrak.
* Penambahan Payload baru tidak mengubah kontrak.
* Perubahan yang mengubah ownership atau struktur inti Domain Model merupakan perubahan Architecture Contract dan harus melalui controlled architecture change.

> **Architecture Decision — AD-LE-011**
>
> Architecture Version, Reference Implementation Version, dan Storage Version merupakan konsep yang terpisah.
>
> **Rationale**
>
> Pemisahan versioning memungkinkan evolusi implementasi dan media penyimpanan dilakukan secara independen tanpa memengaruhi kontrak arsitektur.

---

## 17.6 Version Evolution

Perubahan yang bersifat implementatif, seperti:

* penambahan Activity Classification,
* penambahan Payload,
* penambahan Statistics Services,

dianggap sebagai evolusi implementasi.

Perubahan tersebut tidak memerlukan revisi terhadap Architecture Contract.

---

## 17.7 Breaking Changes

Breaking Change hanya terjadi apabila perubahan mengharuskan implementasi yang telah ada untuk menyesuaikan diri terhadap Architecture Contract.

Contoh Breaking Change antara lain:

* perubahan ownership atau hubungan antar Domain Model,
* perubahan kontrak Repository yang memerlukan penyesuaian implementasi yang telah ada,
* perubahan tanggung jawab komponen inti,
* penghapusan kontrak yang telah dipublikasikan.

Perubahan seperti ini harus disertai dengan peningkatan Architecture Version.

---

## 17.8 Reference Implementation

Reference Implementation pertama menggunakan:

* Architecture Version 1.x
* Reference Implementation Version 1.x
* Storage Version 1.x

Ketiga versi tersebut dapat berkembang secara independen sesuai kebutuhan proyek.

---

## 17.9 Future Compatibility

Versioning dirancang agar Learning Engine dapat berkembang tanpa mengorbankan kompatibilitas implementasi yang telah ada.

Perubahan di masa mendatang diharapkan lebih banyak terjadi pada implementasi daripada pada Architecture Contract.

---

## 17.10 Summary

Versioning menyediakan fondasi evolusi Learning Engine yang terstruktur.

Dengan memisahkan Architecture Version, Reference Implementation Version, dan Storage Version, Learning Engine dapat berkembang secara berkelanjutan sambil mempertahankan stabilitas kontrak arsitektur.

------------------

# 18. Reference Implementation

> **Docstring**
>
> Bab ini menjelaskan bagaimana Architecture Contract direalisasikan melalui Reference Implementation pertama Learning Engine.
> Reference Implementation berfungsi sebagai validasi bahwa kontrak arsitektur dapat diimplementasikan secara nyata, tanpa membatasi evolusi implementasi di masa mendatang.
> Bab ini bersifat informatif dan bukan merupakan bagian normatif dari Architecture Contract.

## 18.1 Purpose

Reference Implementation merupakan implementasi pertama yang digunakan untuk memvalidasi Architecture Contract.

Implementasi ini dipilih berdasarkan ruang lingkup pengembangan pada Sprint AD-7 dan tidak dimaksudkan sebagai representasi lengkap seluruh kemampuan Learning Engine.

Seluruh implementasi berikutnya diharapkan mengikuti kontrak yang sama.

---

## 18.2 Implementation Scope

Reference Implementation hanya mencakup mode pembelajaran berikut:

```text
Quiz Module
```

Seluruh komponen Learning Engine pada versi pertama dibangun untuk mendukung integrasi dengan Quiz Module.

Mode pembelajaran lain belum diimplementasikan.

---

## 18.3 Architecture Mapping

Hubungan antara Architecture Contract dan Reference Implementation ditunjukkan pada tabel berikut.

| Architecture Contract   | Reference Implementation |
| ----------------------- | ------------------------ |
| Learning Profile        | `LearningProfile`        |
| Study Session           | `StudySession`           |
| Activity Classification | `QUIZ`                   |
| Payload                 | `QuizResult`             |
| Learning Repository     | `LearningRepository`     |
| Learning Services       | `LearningService`        |
| Statistics Services     | `StatisticsService`      |
| Data Storage            | JSON Local Storage       |

Tabel ini hanya menunjukkan implementasi pertama dan bukan membatasi implementasi berikutnya.

---

## 18.4 Processing Flow

Reference Implementation mengikuti alur pemrosesan berikut.

```text
Quiz Module
      │
      ▼
Learning Service
      │
      ▼
Create Study Session
      │
      ▼
Attach Activity Classification
      │
      ▼
Attach QuizResult Payload
      │
      ▼
Update Learning Profile
      │
      ▼
Save using Repository
      │
      ▼
Generate Statistics
      │
      ▼
Return Result to User Interface
```

Seluruh logika bisnis berada di dalam Learning Service.

---

## 18.5 Repository Mapping

Reference Implementation menggunakan satu implementasi Repository.

Repository bertanggung jawab terhadap:

* penyimpanan Learning Profile,
* penyimpanan Study Session,
* pengambilan data pembelajaran.

Media penyimpanan menggunakan JSON lokal.

Repository tidak mengandung logika bisnis.

---

## 18.6 Statistics Mapping

Statistics Services menghasilkan informasi yang digunakan oleh Home Dashboard.

Contoh informasi yang dapat dihasilkan:

* Total Quiz
* Total Questions
* Correct Answers
* Incorrect Answers
* Overall Accuracy
* Last Study Date

Daftar tersebut merupakan implementasi awal dan dapat berkembang tanpa mengubah Architecture Contract.

---

## 18.7 Design Validation

Reference Implementation digunakan untuk memvalidasi keputusan-keputusan arsitektur yang telah ditetapkan.

Validasi tersebut meliputi:

* Study Session sebagai Source of Truth.
* Learning Profile sebagai agregasi.
* Repository sebagai Persistence Layer.
* Service Layer sebagai pusat logika bisnis.
* Statistics sebagai Derived Data.

> **Architecture Decision — AD-LE-012**
>
> Reference Implementation digunakan sebagai validasi Architecture Contract, bukan sebagai definisi kemampuan maksimum Learning Engine.
>
> **Rationale**
>
> Ruang lingkup implementasi dapat berkembang dari waktu ke waktu, sedangkan kontrak arsitektur tetap menjadi acuan utama.

---

## 18.8 Limitations

Reference Implementation belum mencakup:

* Flashcard
* Writing Practice
* Listening Practice
* Matching Exercise
* Recommendation Engine
* Achievement System
* Cloud Synchronization

Keterbatasan tersebut merupakan keputusan ruang lingkup implementasi dan bukan keterbatasan Architecture Contract.

---

## 18.9 Evolution Path

Implementasi berikutnya diharapkan memperluas Learning Engine melalui:

* Activity Classification baru.
* Payload baru.
* Statistics Services tambahan.
* Learning Services tambahan.

Perluasan tersebut dilakukan tanpa mengubah Domain Model maupun Architecture Contract.

---

## 18.10 Summary

Reference Implementation merupakan realisasi pertama dari Learning Engine Architecture.

Implementasi ini membuktikan bahwa seluruh komponen inti dapat bekerja sesuai kontrak, sekaligus menyediakan fondasi yang stabil untuk pengembangan mode pembelajaran lainnya pada versi mendatang.

------------------

# 19. Evolution Strategy

> **Docstring**
>
> Bab ini mendefinisikan strategi evolusi Learning Engine setelah Architecture Contract ditetapkan.
> Evolution Strategy bertujuan memastikan bahwa Learning Engine dapat berkembang secara bertahap tanpa mengorbankan stabilitas Architecture Contract maupun kompatibilitas implementasi yang telah ada.
> Bab ini menjadi pedoman bagi seluruh pengembangan Learning Engine pada versi-versi berikutnya.

## 19.1 Purpose

Learning Engine dirancang sebagai fondasi jangka panjang bagi seluruh sistem pembelajaran AksaraNusantara.

Oleh karena itu, evolusi Learning Engine harus dilakukan melalui perluasan implementasi, bukan melalui perubahan terhadap Architecture Contract.

Bab ini menjelaskan prinsip-prinsip yang harus diikuti selama proses pengembangan berlangsung.

---

## 19.2 Evolution Principles

Learning Engine mengikuti prinsip-prinsip evolusi berikut:

* Architecture Contract bersifat stabil.
* Reference Implementation berkembang secara bertahap.
* Domain Model dipertahankan.
* Service Layer dapat diperluas.
* Repository dapat diganti.
* Storage dapat berubah.
* Activity Classification dapat bertambah.
* Payload dapat bertambah.

Perubahan implementasi tidak boleh menyebabkan perubahan terhadap struktur konseptual Learning Engine.

---

## 19.3 Extension Points

Learning Engine menyediakan beberapa titik perluasan (*Extension Points*) yang dapat digunakan oleh implementasi baru.

Extension Points meliputi:

* Activity Classification
* Payload
* Learning Services
* Statistics Services
* Repository Implementation
* Storage Implementation

Penambahan implementasi pada Extension Points tidak memerlukan perubahan terhadap Architecture Contract.

---

## 19.4 Future Learning Activities

Architecture Contract telah dipersiapkan untuk mendukung berbagai mode pembelajaran, termasuk namun tidak terbatas pada:

* Flashcard
* Writing Practice
* Listening Practice
* Matching Exercise
* Transliteration Exercise
* Character Recognition
* Daily Practice
* Adaptive Learning

Seluruh mode pembelajaran tersebut diharapkan menggunakan Domain Model yang sama.

---

## 19.5 Backward Compatibility

Learning Engine harus mempertahankan kompatibilitas terhadap implementasi yang telah mematuhi Architecture Contract.

Perubahan implementasi tidak boleh menyebabkan implementasi sebelumnya menjadi tidak valid tanpa alasan arsitektural yang kuat.

Untuk Study Session yang telah dipersist sebelum learner ownership diperkenalkan, sistem tidak boleh menetapkan `learner_id` secara diam-diam berdasarkan tebakan, urutan profile, timestamp, session identifier, atau informasi tidak authoritative lainnya. Legacy records tanpa ownership yang dapat diverifikasi harus diperlakukan sebagai legacy/unassigned data sampai migration strategy yang eksplisit diterapkan.

Backward Compatibility merupakan salah satu prioritas utama dalam evolusi Learning Engine.

---

## 19.6 Architecture Stability

Architecture Contract dianggap sebagai fondasi Learning Engine.

Perubahan terhadap kontrak hanya diperbolehkan apabila:

* ditemukan kesalahan fundamental pada desain,
* terdapat kebutuhan arsitektural yang tidak dapat diakomodasi,
* perubahan tersebut memberikan manfaat jangka panjang yang signifikan.

Seluruh perubahan terhadap Architecture Contract harus melalui evaluasi menyeluruh.

> **Architecture Decision — AD-LE-013**
>
> Evolusi Learning Engine dilakukan terutama melalui perluasan implementasi tanpa mengubah Architecture Contract. Perubahan terhadap Architecture Contract hanya dilakukan apabila terdapat kebutuhan arsitektural yang tidak dapat diakomodasi oleh kontrak yang ada dan telah melalui proses keputusan arsitektur yang terdokumentasi.
>
> **Rationale**
>
> Stabilitas kontrak tetap menjadi prioritas, tetapi arsitektur harus dapat dikoreksi apabila ditemukan gap fundamental yang memengaruhi integrity, ownership, compatibility, atau long-term viability sistem.

---

## 19.7 Reference Implementation Evolution

Reference Implementation pertama hanya merealisasikan sebagian kemampuan Learning Engine.

Implementasi berikutnya diharapkan memperluas kemampuan tersebut melalui penambahan:

* Activity Classification baru.
* Payload baru.
* Learning Services baru.
* Statistics Services baru.

Perluasan tersebut dilakukan tanpa mengubah struktur Domain Model.

---

## 19.8 Long-Term Vision

Learning Engine diproyeksikan menjadi fondasi seluruh aktivitas pembelajaran di dalam ekosistem AksaraNusantara.

Seluruh mode pembelajaran diharapkan berbagi Domain Model, Service Layer, Repository, dan mekanisme statistik yang sama sehingga perjalanan belajar pengguna dapat direpresentasikan secara konsisten.

Implementasi dapat berkembang sesuai kebutuhan aplikasi tanpa mengorbankan stabilitas Architecture Contract.

---

## 19.9 Closing Statement

Learning Engine Architecture merupakan kontrak konseptual yang mendefinisikan struktur, tanggung jawab, serta hubungan antar komponen utama dalam sistem pembelajaran AksaraNusantara.

Dokumen ini disusun dengan prinsip **Contract First**, sehingga Architecture Contract menjadi fondasi yang stabil bagi seluruh implementasi saat ini maupun di masa mendatang.

Reference Implementation pertama membuktikan bahwa kontrak ini dapat direalisasikan melalui Quiz Module, sementara evolusi berikutnya diharapkan memperluas implementasi tanpa mengubah prinsip-prinsip dasar yang telah ditetapkan.

Dengan demikian, Learning Engine dapat berkembang secara berkelanjutan sebagai fondasi pembelajaran yang konsisten, modular, dan mudah dipelihara sepanjang siklus hidup proyek AksaraNusantara.

------------------

# Appendix A — Conceptual Directory Layout

> **Docstring**
>
> Appendix ini memberikan contoh struktur direktori konseptual yang dapat digunakan untuk mengimplementasikan Learning Engine.
> Struktur yang ditampilkan bersifat informatif dan tidak merupakan bagian dari Architecture Contract.
> Implementasi diperbolehkan menggunakan struktur direktori yang berbeda selama tetap mematuhi kontrak arsitektur yang didefinisikan pada dokumen ini.

## A.1 Purpose

Conceptual Directory Layout memberikan gambaran mengenai pemisahan komponen Learning Engine ke dalam beberapa kelompok sesuai tanggung jawab arsitekturalnya.

Struktur ini dimaksudkan sebagai referensi implementasi dan bukan sebagai persyaratan wajib.

---

## A.2 Example Directory Layout

```text
core/

└── learning/

    ├── models/
    │
    │   ├── learning_profile.py
    │   ├── study_session.py
    │   └── payload.py
    │
    ├── services/
    │
    │   ├── learning_service.py
    │   └── statistics_service.py
    │
    ├── repositories/
    │
    │   └── learning_repository.py
    │
    ├── storage/
    │
    │   ├── storage_adapter.py
    |   └── json_storage.py
    │
    └── __init__.py
```

---

## A.3 Notes

Directory Layout pada appendix ini hanya merupakan contoh implementasi.

Architecture Contract tidak mewajibkan struktur direktori tertentu maupun nama modul tertentu.

Implementasi lain diperbolehkan menggunakan struktur yang berbeda selama hubungan konseptual antar komponen tetap dipertahankan.

------------------

# Appendix B — Domain Relationship Diagram

> **Docstring**
>
> Appendix ini menyediakan representasi visual hubungan antar komponen utama Learning Engine.
> Diagram digunakan sebagai referensi cepat untuk memahami struktur Domain Model, Service Layer, dan Persistence Layer tanpa menggantikan definisi normatif pada bab-bab utama.
> Diagram bersifat informatif dan dapat diperluas selama tetap mematuhi Architecture Contract.

## B.1 Purpose

Domain Relationship Diagram memberikan gambaran menyeluruh mengenai hubungan antar komponen Learning Engine.

Diagram ini memperlihatkan:

* Domain Model.
* Service Layer.
* Persistence Layer.
* Aliran ketergantungan antar lapisan.
* Hubungan antara Primary Data dan Derived Data.

---

## B.2 Layered Domain Model

```text
┌──────────────────────────────────────────────────────────────┐
│                       DOMAIN MODEL                           │
│                                                              │
│  ┌─────────────────┐                                         │
│  │ Learning Profile│◄───────────────┐                        │
│  └─────────────────┘                │                        │
│          ▲                           │ derived from           │
│          │                           │                        │
│          │                    ┌──────┴───────┐                │
│          │                    │ Study Session│                │
│          │                    └──────┬───────┘                │
│          │                           │                        │
│          │              ┌────────────┴────────────┐           │
│          │              │                         │           │
│          │              ▼                         ▼           │
│          │    Activity Classification         Payload        │
│          │                                                   │
└──────────┼───────────────────────────────────────────────────┘
           │
           │ processed by
           ▼
┌──────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                       │
│                                                              │
│  ┌─────────────────────┐     ┌──────────────────────────┐    │
│  │  Learning Service   │     │   Statistics Service     │    │
│  └──────────┬──────────┘     └────────────▲─────────────┘    │
│             │                             │                  │
└─────────────┼─────────────────────────────┼──────────────────┘
              │                             │
              │ persistence                 │ reads
              ▼                             │
┌───────────────────────────────────────────┼──────────────────┐
│                 INFRASTRUCTURE LAYER       │                  │
│                                           │                  │
│  ┌─────────────────────────┐              │                  │
│  │   Learning Repository   │◄─────────────┘                  │
│  └────────────┬────────────┘                                 │
│               │                                               │
│               ▼                                               │
│  ┌─────────────────────────┐                                  │
│  │     Storage Adapter     │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                               │
│  ┌─────────────────────────┐                                  │
│  │    Persistent Storage   │                                  │
│  └─────────────────────────┘                                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## B.3 Domain Relationships

Hubungan utama Domain Model adalah:

```text
Learner Identity
       │
       ▼
Study Session *
       │
       │ derived into
       ▼
Learning Profile
       │
       ├───────────────┐
       │               │
       ▼               ▼
Activity             Payload
Classification
```

Interpretasi diagram:

* Satu Learning Profile merepresentasikan satu learner.
* Setiap Study Session dimiliki tepat satu learner melalui `learner_id`.
* Satu Learning Profile dapat memiliki banyak Study Session milik learner yang sama.
* Setiap Study Session memiliki tepat satu Activity Classification.
* Setiap Study Session memiliki tepat satu Payload.
* Study Session merupakan Primary Data.
* Learning Profile merupakan Derived Aggregate.

---

## B.4 Layer Relationships

Ketergantungan antar lapisan mengikuti arah berikut:

```text
User Interface
      │
      ▼
Learning Services
      │
      ▼
Learning Repository
      │
      ▼
Storage Adapter
      │
      ▼
Persistent Storage
```

Statistics Service memperoleh informasi dari Domain Model dan tidak menjadi bagian dari Persistence Layer.

---

## B.5 Data Classification

Data Learning Engine dapat diklasifikasikan sebagai berikut:

```text
PRIMARY DATA
    │
    └── Study Session
          │
          ├── Activity Classification
          └── Payload


DERIVED DATA
    │
    ├── Learning Profile
    └── Statistics


PRESENTATION DATA
    │
    └── Dashboard / History / Reports
```

> **Architecture Note**
>
> Presentation Data bukan bagian dari Domain Model. Dashboard, History, dan laporan merupakan representasi data yang dihasilkan untuk kebutuhan User Interface.

---

## B.6 Reference Implementation

Pada Reference Implementation, hubungan Domain Model menjadi:

```text
Learning Profile
       ▲
       │
Study Session
       │
       ├── Activity Classification
       │        └── QUIZ
       │
       └── Payload
                └── QuizResult
```

Service dan Persistence Layer:

```text
Quiz Module
     │
     ▼
Learning Service
     │
     ├──────────────► Statistics Service
     │
     ▼
Learning Repository
     │
     ▼
Storage Adapter
     │
     ▼
JSON Storage
```

Diagram ini hanya menggambarkan Reference Implementation dan tidak membatasi Future Implementation.

---

## B.7 Future Extension Model

Ketika mode pembelajaran baru ditambahkan, struktur inti tetap dipertahankan.

Contoh:

```text
Study Session
     │
     ├── QUIZ
     │     └── QuizResult
     │
     ├── FLASHCARD
     │     └── FlashcardResult
     │
     ├── WRITING
     │     └── WritingResult
     │
     └── LISTENING
           └── ListeningResult
```

Tidak diperlukan perubahan terhadap struktur:

```text
Learning Profile
Learning Repository
Storage Adapter
```

selama implementasi baru tetap mematuhi Architecture Contract.

---

## B.8 Summary

Domain Relationship Diagram memberikan representasi ringkas terhadap struktur Learning Engine.

Struktur utama dapat diringkas sebagai:

```text
Study Session
     │
     ├── Classification
     └── Payload
     │
     ▼
Learning Profile
     │
     ▼
Statistics Service
```

dengan persistensi melalui:

```text
Learning Service
     │
     ▼
Learning Repository
     │
     ▼
Storage Adapter
     │
     ▼
Persistent Storage
```

Diagram ini merupakan referensi visual terhadap Architecture Contract yang telah didefinisikan pada bab-bab utama.

------------------

# Appendix C — Processing Flow

> **Docstring**
>
> Appendix ini mendokumentasikan alur pemrosesan data di dalam Learning Engine, dengan Quiz Module sebagai Reference Implementation.
> Diagram dan uraian pada appendix ini menunjukkan bagaimana data bergerak dari aktivitas pembelajaran menuju Domain Model, Persistence Layer, dan informasi yang dikonsumsi oleh User Interface.
> Bagian ini bersifat informatif dan tidak menggantikan aturan normatif yang telah ditetapkan pada bab-bab utama.

## C.1 Purpose

Processing Flow memberikan gambaran menyeluruh mengenai siklus sebuah aktivitas pembelajaran sejak dimulai hingga hasilnya tersedia bagi User Interface.

Reference Implementation menggunakan Quiz sebagai aktivitas pembelajaran pertama.

---

## C.2 High-Level Flow

Alur utama Learning Engine adalah:

```text
Active Learner Context
 │
 ▼
Quiz Module
 │
 │ Quiz Completed
 ▼
Learning Service
 │
 ├── Create Study Session
 │
 ├── Set Activity Classification
 │
 ├── Attach Payload
 │
 ├── Update Learning Profile
 │
 └── Persist Data
       │
       ▼
 Learning Repository
       │
       ▼
 Storage Adapter
       │
       ▼
 Persistent Storage
       │
       ▼
 Statistics Service
       │
       ▼
 Dashboard
```

---

## C.3 Quiz Completion Flow

Ketika pengguna menyelesaikan Quiz, Quiz Module menghasilkan informasi hasil pembelajaran.

```text
Quiz Module
     │
     ▼
Quiz Completed
     │
     ▼
QuizResult
```

`QuizResult` kemudian diserahkan kepada Learning Service untuk diproses.

Quiz Module tidak menyimpan hasil pembelajaran secara langsung ke Persistent Storage.

---

## C.4 Study Session Creation

Learning Service membuat Study Session berdasarkan hasil aktivitas.

```text
QuizResult
    │
    ▼
Study Session
    │
    ├── learner_id = Active Learner
    ├── Activity Classification = QUIZ
    │
    └── Payload = QuizResult
```

Study Session menjadi representasi permanen dari aktivitas pembelajaran tersebut.

---

## C.5 Learning Profile Update

Setelah Study Session terbentuk, Learning Service memperbarui Learning Profile.

```text
Existing Learning Profile
          │
          │ + Study Session
          ▼
Updated Learning Profile
```

Informasi agregat dapat mencakup:

* jumlah sesi,
* jumlah soal,
* jumlah jawaban benar,
* jumlah jawaban salah,
* akurasi keseluruhan,
* tanggal aktivitas terakhir.

Daftar tersebut merupakan contoh Reference Implementation dan bukan batasan Architecture Contract.

---

## C.6 Persistence Flow

Learning Service tidak berinteraksi langsung dengan media penyimpanan.

Alur persistensi:

```text
Learning Service
       │
       ▼
Learning Repository
       │
       ▼
Storage Adapter
       │
       ▼
Persistent Storage
```

Repository menyembunyikan detail mekanisme penyimpanan dari Service Layer.

Reference Implementation menggunakan JSON sebagai Persistent Storage.

---

## C.7 Statistics Flow

Statistics Service membaca data pembelajaran yang telah tersimpan atau tersedia melalui Domain Model.

```text
Study Sessions
      │
      ▼
Learning Profile
      │
      ▼
Statistics Service
      │
      ▼
Statistics Information
```

Statistics Service tidak mengubah Study Session maupun Learning Profile.

---

## C.8 Dashboard Flow

Home Dashboard menggunakan informasi yang dihasilkan oleh Learning Services dan Statistics Services.

```text
Statistics Service
       │
       ▼
Statistics Information
       │
       ▼
Home Dashboard
       │
       ▼
User
```

User Interface hanya menampilkan informasi yang diberikan oleh Service Layer.

---

## C.9 Complete Reference Flow

Keseluruhan Reference Implementation dapat digambarkan sebagai berikut:

```text
┌─────────────────┐
│      User       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Quiz Module   │
└────────┬────────┘
         │
         │ QuizResult
         ▼
┌─────────────────────────┐
│    Learning Service     │
│                         │
│ Create Study Session    │
│ Set Classification      │
│ Attach Payload          │
│ Update Profile          │
└───────────┬─────────────┘
            │
            ├──────────────────────┐
            │                      │
            ▼                      ▼
┌─────────────────────┐   ┌─────────────────────┐
│ Learning Repository │   │ Statistics Service  │
└──────────┬──────────┘   └──────────┬──────────┘
           │                         │
           ▼                         │
┌─────────────────────┐              │
│  Storage Adapter    │              │
└──────────┬──────────┘              │
           │                         │
           ▼                         │
┌─────────────────────┐              │
│ Persistent Storage  │              │
└─────────────────────┘              │
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │    Home Dashboard   │
                           └──────────┬──────────┘
                                      │
                                      ▼
                                   User
```

---

## C.10 Failure Boundary

Setiap lapisan memiliki batas tanggung jawab terhadap kegagalan.

```text
Quiz Module
    │
    ├── Invalid Result
    │
    ▼
Learning Service
    │
    ├── Business Validation Error
    │
    ▼
Learning Repository
    │
    ├── Persistence Error
    │
    ▼
Storage Adapter
    │
    └── Storage Error
```

Error yang terjadi pada satu lapisan tidak boleh menyebabkan lapisan lain mengambil alih tanggung jawab yang bukan miliknya.

---

## C.11 Future Activity Flow

Ketika aktivitas baru ditambahkan, alur inti tetap sama.

Contoh Flashcard:

```text
Flashcard Module
      │
      ▼
FlashcardResult
      │
      ▼
Learning Service
      │
      ▼
Study Session
      │
      ├── Classification = FLASHCARD
      └── Payload = FlashcardResult
      │
      ▼
Learning Profile
      │
      ▼
Statistics Service
```

Perubahan hanya terjadi pada sumber aktivitas, Activity Classification, dan Payload.

Struktur Learning Engine lainnya tetap dipertahankan.

---

## C.12 Processing Principles

Processing Flow mengikuti prinsip berikut:

1. Aktivitas pembelajaran menghasilkan Payload.
2. Learning Service membentuk Study Session.
3. Study Session menjadi Primary Data.
4. Learning Profile diperbarui berdasarkan Study Session.
5. Repository menangani persistensi.
6. Statistics Service menghasilkan Derived Data.
7. User Interface hanya mengonsumsi hasil Service Layer.

Prinsip tersebut berlaku untuk Reference Implementation maupun Future Implementation.

---

## C.13 Summary

Processing Flow menunjukkan bahwa Learning Engine memisahkan aktivitas pembelajaran, Domain Model, Business Logic, Persistence, dan Presentation.

Reference Implementation menggunakan Quiz sebagai titik masuk, tetapi alur tersebut dirancang agar dapat digunakan kembali oleh seluruh aktivitas pembelajaran yang akan ditambahkan pada masa mendatang.

------------------

# Appendix D — Architecture Decision Index

> **Docstring**
>
> Appendix ini menyediakan indeks seluruh Architecture Decision yang didefinisikan dalam Learning Engine Architecture.
> Indeks ini memungkinkan implementer dan maintainer menemukan keputusan arsitektur secara cepat tanpa harus menelusuri seluruh dokumen.
> Detail setiap keputusan tetap berada pada bab tempat keputusan tersebut didefinisikan.

## D.1 Purpose

Architecture Decision Index berfungsi sebagai referensi cepat terhadap keputusan arsitektur yang telah ditetapkan selama perancangan Learning Engine.

Setiap keputusan memiliki identifier unik dengan format:

```text
AD-LE-NNN
```

dengan:

* `AD` — Architecture Decision
* `LE` — Learning Engine
* `NNN` — Nomor keputusan

Identifier bersifat stabil dan tidak boleh digunakan kembali untuk keputusan yang berbeda.

---

## D.2 Decision Index

| ID            | Decision                                                                                                                                  | Reference                |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| **AD-LE-001** | Learning Profile merepresentasikan aggregated learning state dan tidak menyimpan activity-specific payload.                               | Learning Profile         |
| **AD-LE-002** | Study Session merupakan unit dasar pencatatan aktivitas pembelajaran yang telah selesai.                                                  | Study Session            |
| **AD-LE-003** | History merupakan presentation view dari kumpulan Study Session dan bukan Domain Model.                                                   | Study Session            |
| **AD-LE-004** | Activity Classification mengidentifikasi jenis aktivitas pembelajaran yang direpresentasikan oleh Study Session.                          | Activity Classification  |
| **AD-LE-005** | Payload merepresentasikan hasil spesifik aktivitas yang terkait dengan Study Session dan harus kompatibel dengan Activity Classification. | Payload Model            |
| **AD-LE-006** | Seluruh operasi persistensi dilakukan melalui Learning Repository.                                                                        | Learning Repository      |
| **AD-LE-007** | Learning Services merupakan entry point utama terhadap Business Logic Learning Engine.                                                    | Learning Services        |
| **AD-LE-008** | Statistics merupakan Derived Data dan bukan Primary Data yang disimpan sebagai sumber kebenaran.                                          | Statistics Services      |
| **AD-LE-009** | Learning Engine tidak bergantung pada teknologi penyimpanan tertentu.                                                                     | Data Storage             |
| **AD-LE-010** | Domain Model dipisahkan dari Service Layer dan Persistence Layer.                                                                         | Domain Model             |
| **AD-LE-011** | Architecture Version, Reference Implementation Version, dan Storage Version dikelola secara independen.                                   | Versioning               |
| **AD-LE-012** | Reference Implementation digunakan untuk memvalidasi Architecture Contract dan bukan sebagai batas kemampuan Learning Engine.             | Reference Implementation |
| **AD-LE-013** | Evolusi Learning Engine dilakukan terutama melalui perluasan implementasi; perubahan kontrak hanya melalui controlled architecture change.     | Evolution Strategy       |
| **AD-LE-014** | Setiap Study Session dimiliki tepat satu learner melalui `learner_id`, dan Repository menyediakan learner-scoped retrieval.               | Learner Ownership        |

---

## D.3 Decision Categories

Architecture Decisions dapat dikelompokkan menjadi beberapa kategori.

### Domain Model

```text
AD-LE-001
AD-LE-002
AD-LE-003
AD-LE-004
AD-LE-005
AD-LE-010
AD-LE-014
```

### Application Layer

```text
AD-LE-007
AD-LE-008
```

### Persistence Layer

```text
AD-LE-006
AD-LE-009
AD-LE-014
```

### Versioning and Evolution

```text
AD-LE-011
AD-LE-012
AD-LE-013
```

---

## D.4 Decision Stability

Architecture Decision yang tercantum dalam appendix ini dianggap sebagai bagian dari Architecture Contract selama dokumen berada pada Architecture Version yang sesuai.

Decision Identifier tidak boleh digunakan kembali untuk keputusan yang berbeda.

Apabila suatu keputusan dibatalkan atau digantikan, keputusan lama harus tetap dipertahankan sebagai bagian dari architectural history dan keputusan baru harus memperoleh identifier baru.

Contoh:

```text
AD-LE-006  → Original Decision
AD-LE-014  → Replacement Decision
```

Keputusan lama tidak dihapus dari history.

---

## D.5 Decision Traceability

Architecture Decision dapat digunakan sebagai penghubung antara:

```text
Architecture Contract
        │
        ▼
Architecture Decision
        │
        ▼
Implementation
        │
        ▼
Test
```

Reference Implementation dapat mencantumkan Architecture Decision yang direalisasikan oleh suatu komponen.

Contoh:

```python
"""
Architecture Decisions:

AD-LE-006
AD-LE-007
"""
```

Unit test juga dapat menggunakan identifier yang sama untuk menunjukkan kontrak yang sedang divalidasi.

---

## D.6 Future Decisions

Architecture Decision baru harus memperoleh identifier berikutnya yang tersedia.

Contoh:

```text
AD-LE-014
AD-LE-015
AD-LE-016
```

Identifier baru tidak boleh menggantikan identifier lama.

Keputusan baru yang memodifikasi atau menggantikan keputusan sebelumnya harus secara eksplisit mencantumkan hubungan dengan decision yang terdahulu.

---

## D.7 Summary

Architecture Decision Index menyediakan daftar terpusat seluruh keputusan arsitektur Learning Engine.

Index ini mendukung traceability, maintainability, dan historical integrity tanpa menduplikasi isi keputusan yang telah dijelaskan pada bab utama.

------------------

# Appendix E — Glossary

> **Docstring**
>
> Appendix ini mendefinisikan istilah-istilah utama yang digunakan dalam Learning Engine Architecture.
> Glossary berfungsi sebagai referensi terminologi resmi untuk menjaga konsistensi pemahaman antar developer, dokumentasi, dan implementasi.
> Apabila istilah digunakan dalam konteks Learning Engine, definisi pada glossary ini menjadi definisi referensi.

## E.1 Activity Classification

Mekanisme untuk mengidentifikasi jenis aktivitas pembelajaran yang direpresentasikan oleh sebuah Study Session.

Contoh:

```text id="3p1x6f"
QUIZ
FLASHCARD
WRITING
LISTENING
```

Activity Classification bukan merupakan Domain Model terpisah.

---

## E.2 Architecture Contract

Kumpulan aturan, struktur, tanggung jawab, dan hubungan konseptual yang harus dipatuhi oleh implementasi Learning Engine.

Architecture Contract merupakan dasar evaluasi kesesuaian implementasi terhadap arsitektur.

---

## E.3 Architecture Decision

Keputusan desain arsitektur yang telah ditetapkan dan didokumentasikan beserta alasan (*rationale*) yang mendasarinya.

Architecture Decision memiliki identifier unik dengan format:

```text id="7ymr9s"
AD-LE-NNN
```

---

## E.4 Architecture Version

Versi yang merepresentasikan evolusi Architecture Contract.

Perubahan implementasi yang tidak mengubah kontrak tidak memerlukan perubahan Architecture Version.

---

## E.5 Business Logic

Aturan dan proses yang menentukan bagaimana Learning Engine memproses aktivitas pembelajaran dan memperbarui keadaan pembelajaran pengguna.

Business Logic berada pada Service Layer.

---

## E.6 Core Domain

Bagian utama Domain Model yang merepresentasikan konsep inti pembelajaran.

Learning Engine Core Domain terdiri atas:

```text id="y7c4e3"
Learning Profile
Study Session
Activity Classification
Payload
```

---

## E.7 Data Storage

Media persistensi yang digunakan untuk menyimpan data Learning Engine.

Data Storage tidak mengandung Business Logic.

---

## E.8 Derived Data

Informasi yang dihasilkan melalui pemrosesan Primary Data dan dapat dihitung ulang.

Contoh:

```text id="y8g2gz"
Learning Profile
Statistics
```

---

## E.9 Domain Model

Representasi konseptual objek dan hubungan yang menjadi inti Learning Engine.

Domain Model tidak bergantung pada User Interface maupun teknologi penyimpanan.

---

## E.10 Evolution Strategy

Sekumpulan prinsip yang mengatur bagaimana Learning Engine berkembang tanpa mengorbankan Architecture Contract.

---

## E.11 Future Implementation

Implementasi mode pembelajaran atau layanan yang belum menjadi bagian dari Reference Implementation saat ini.

Contoh:

```text id="g7x9s0"
Flashcard
Writing Practice
Listening Practice
```

---

## E.12 Learning Engine

Subsistem yang bertanggung jawab mengelola data, proses, dan perkembangan aktivitas pembelajaran pengguna.

Learning Engine merupakan bagian dari arsitektur AksaraNusantara.

---

## E.13 Learning Profile

Representasi agregat mengenai keadaan perkembangan belajar seorang pengguna.

Learning Profile bukan riwayat aktivitas individual.

---

## E.14 Learning Repository

Komponen Persistence Layer yang bertanggung jawab terhadap penyimpanan dan pengambilan data Learning Engine.

Repository tidak mengandung Business Logic.

---

## E.15 Learning Service

Komponen Application Layer yang mengoordinasikan Business Logic Learning Engine.

Learning Service merupakan entry point utama untuk operasi pembelajaran.

---

## E.16 Payload

Data spesifik yang merepresentasikan hasil dari sebuah aktivitas pembelajaran.

Setiap Study Session memiliki tepat satu Payload.

Struktur Payload bergantung pada Activity Classification.

---

## E.17 Persistence Layer

Lapisan yang bertanggung jawab terhadap persistensi data.

Dalam Learning Engine, Persistence Layer terdiri atas:

```text id="yw9t4d"
Learning Repository
Storage Adapter
Data Storage
```

---

## E.18 Primary Data

Data utama yang menjadi Source of Truth dan tidak bergantung pada data turunan.

Dalam Learning Engine, Study Session merupakan Primary Data.

---

## E.19 Reference Implementation

Implementasi pertama yang digunakan untuk memvalidasi Architecture Contract.

Reference Implementation tidak mendefinisikan batas kemampuan Learning Engine.

---

## E.20 Service Layer

Lapisan Application Layer yang menjalankan Business Logic dan mengoordinasikan Domain Model dengan Persistence Layer.

---

## E.21 Source of Truth

Data utama yang menjadi dasar bagi pembentukan seluruh Derived Data.

Dalam Learning Engine, Study Session merupakan Source of Truth untuk aktivitas pembelajaran.

---

## E.22 Statistics

Informasi analitis yang dihasilkan berdasarkan Primary Data maupun Derived Data.

Statistics merupakan Derived Data dan bukan Primary Data.

---

## E.23 Statistics Service

Service yang menghasilkan informasi statistik tanpa menjadi sumber penyimpanan data utama.

Statistics Service bersifat read-only terhadap Source of Truth.

---

## E.24 Storage Adapter

Lapisan abstraksi yang memisahkan Learning Repository dari teknologi penyimpanan tertentu.

Storage Adapter memungkinkan implementasi storage diganti tanpa mengubah Domain Model maupun Business Logic.

---

## E.25 Storage Version

Versi yang merepresentasikan format atau struktur data pada Persistent Storage.

Storage Version dapat berubah secara independen dari Architecture Version.

---

## E.26 Learner Identity

Identitas unik yang digunakan Learning Engine untuk menentukan learner pemilik Learning Profile dan Study Session. Learner Identity direpresentasikan oleh `learner_id`.

---

## E.27 Study Session

Representasi satu aktivitas pembelajaran yang dilakukan oleh seorang learner.

Study Session merupakan unit dasar pencatatan aktivitas dan Primary Data Learning Engine.

Setiap Study Session memiliki:

```text id="o6p4o5"
learner_id
Activity Classification
Payload
```

Setiap Study Session dimiliki tepat satu learner.

---

## E.28 User Interface

Lapisan aplikasi yang bertanggung jawab terhadap interaksi dan presentasi kepada pengguna.

User Interface tidak boleh mengakses Persistence Layer secara langsung.

---

## E.29 History

Representasi visual dari kumpulan Study Session.

History bukan merupakan Domain Model maupun sumber data terpisah.

---

## E.30 Quiz Result

Payload yang digunakan oleh Reference Implementation untuk merepresentasikan hasil Quiz.

QuizResult merupakan implementasi spesifik dan bukan bagian dari Architecture Contract generik.

---

## E.31 Reference Implementation Scope

Batas kemampuan yang direalisasikan oleh Reference Implementation pada versi tertentu.

Reference Implementation Scope tidak boleh dianggap sebagai batas Architecture Contract.

---

## E.32 Summary

Glossary menetapkan terminologi resmi Learning Engine Architecture.

Penggunaan istilah yang konsisten diperlukan untuk menjaga keselarasan antara Architecture Contract, Reference Implementation, Source Code, Unit Test, dan dokumentasi proyek.
