\# AD-TR-01 — Phase 2C — Tokenization \& Orthographic Resolution



> \*\*Status:\*\* LOCKED

>

> \*\*Milestone:\*\* AD-TR-01 — Transliterasi Subsystem

>

> \*\*Phase:\*\* Phase 2 — Core Transliteration Implementation

>

> \*\*Checkpoint:\*\* Phase 2C — Tokenization \& Orthographic Resolution

>

> \*\*Predecessor:\*\* Phase 2A — Implementation Reconnaissance  

> \*\*Predecessor:\*\* Phase 2B — Capability \& Diagnostic API

>

> \*\*Next Checkpoint:\*\* Phase 2D — Core Test Contract



\---



\# 1. Latar Belakang



Setelah Phase 2A dan Phase 2B selesai, kita belum langsung menulis implementasi transliterasi.



Keputusan ini disengaja.



Phase 2A telah melakukan reconnaissance terhadap kondisi implementasi yang ada dan mengidentifikasi fondasi yang dapat digunakan.



Phase 2B kemudian memperjelas \*\*capability boundary\*\* dan arah arsitektur transliterasi.



Namun masih terdapat sejumlah pertanyaan penting yang belum boleh dijawab dengan asumsi.



Di antaranya:



\- apa sebenarnya yang dimaksud dengan \*token\* dalam transliterasi Aksara Jawa;

\- bagaimana input Latin dipecah;

\- bagaimana menangani sequence seperti `ng`, `ny`, dan `kh`;

\- apakah tokenizer harus memahami suku kata;

\- kapan sebuah sequence dianggap sebagai satu token;

\- bagaimana context memengaruhi representasi ortografis;

\- bagaimana menghindari tokenizer berubah menjadi \*mini grammar engine\*.



Dari sinilah Phase 2C dimulai.



\---



\# 2. Pertanyaan Fundamental Phase 2C



Kita sengaja menahan diri untuk tidak langsung membuat algoritma.



Pertanyaan pertama yang harus dijawab adalah:



> \*\*Apa yang dimaksud dengan "token" dalam transliterasi Aksara Jawa?\*\*



Pertanyaan ini terlihat sederhana.



Namun setelah kita melihat contoh-contoh nyata, masalahnya segera menjadi jauh lebih kompleks.



Kasus yang perlu dipertimbangkan antara lain:



```text

ka

ki

ku

ke

ko



kh

gh

dz



ng

ny



kr

ky

kry



k

```



Pada titik ini, membuat rule sederhana seperti:



```python

if text.startswith("ng"):

&#x20;   ...

```



jelas belum cukup.



Sebelum menentukan algoritma, kita harus memahami \*\*unit apa yang sebenarnya sedang kita kenali\*\*.



\---



\# 3. Baseline dari Phase 2B



Phase 2B telah memberikan model konseptual:



```text

Latin Input

&#x20;   ↓

Tokenizer

&#x20;   ↓

Token Stream

&#x20;   ↓

Orthographic Resolver

&#x20;   ↓

Composer

```



Namun Phase 2B belum menyelesaikan seluruh detail internalnya.



Yang diwariskan kepada Phase 2C adalah pertanyaan-pertanyaan seperti:



\- token recognition untuk `ng` dan `ny`;

\- token matching;

\- prinsip longest valid token;

\- penggunaan lookahead;

\- orthographic role resolution;

\- syllable boundary;

\- ambiguous Latin sequences;

\- pembentukan struktur ortografis dari token stream.



Dengan kata lain, Phase 2B telah memberikan \*\*batas arsitektural\*\*, sedangkan Phase 2C harus mulai menyelidiki bagaimana proses di dalam batas tersebut dapat dipahami.



\---



\# 4. Workshop Dimulai: Token Taxonomy



Langkah pertama adalah mencoba mengidentifikasi kemungkinan kelas token.



Pada awal diskusi muncul sejumlah kandidat:



```text

A. Independent phonetic token

B. Base consonant

C. Vowel

D. Modifier

E. Consonant cluster

F. Orthographic boundary

```



Namun segera muncul peringatan penting.



Beberapa istilah tersebut mungkin merupakan konsep internal engine, tetapi belum tentu merupakan konsep yang secara eksplisit dimiliki oleh ScriptPack.



Karena itu kita tidak boleh terburu-buru menjadikan semua kategori tersebut sebagai kontrak final.



Workshop kemudian bergerak ke arah yang lebih konkret:



> Mari gunakan contoh nyata sebagai stress test.



\---



\# 5. Stress Test Pertama: `ng`



Sequence:



```text

ng

```



menjadi salah satu kasus paling penting dalam seluruh workshop.



Masalahnya adalah bahwa `ng` dapat berhubungan dengan beberapa representasi ortografis, antara lain:



```text

Nglegena

Panyigeg

Pasangan

```



Maka muncul pertanyaan:



> Apakah tokenizer harus langsung menentukan bahwa `ng` adalah Panyigeg?



Jawabannya: \*\*tidak boleh\*\*.



Token yang sama dapat memiliki interpretasi yang berbeda tergantung context.



Model yang lebih sehat adalah:



```text

TOKENIZER



"ng"

&#x20;↓



NG\_TOKEN

```



Kemudian:



```text

ORTHOGRAPHIC RESOLVER



NG\_TOKEN

&#x20;   ↓

context

&#x20;   ↓

role

```



Resolver dapat menentukan representasi berdasarkan context.



Secara konseptual:



```text

NG

&#x20;├── Nglegena

&#x20;├── Pasangan

&#x20;└── Panyigeg

```



Kasus `ng` kemudian menjadi salah satu alasan utama mengapa kita harus memisahkan \*\*pengenalan token\*\* dari \*\*interpretasi ortografis\*\*.



\---



\# 6. Stress Test Kedua: `kh`, `gh`, dan `dz`



Kasus berikutnya berbeda.



Untuk sequence:



```text

kh

gh

dz

```



terdapat dedicated Rekan representation.



Karena itu, tokenizer perlu mempertimbangkan:



```text

kh → KH\_TOKEN

gh → GH\_TOKEN

dz → DZ\_TOKEN

```



sebelum melakukan dekomposisi sederhana:



```text

kh → K + H

```



Kasus ini memperkenalkan konsep penting:



> \*\*Dedicated multi-character token dapat memiliki makna yang berbeda dari gabungan token yang lebih pendek.\*\*



Namun kita juga belum boleh menyederhanakannya menjadi:



> "Selalu pilih string yang paling panjang."



Yang lebih tepat adalah:



> \*\*Longest Valid Token\*\*



Bukan sekadar:



> \*\*Longest String Match\*\*



Perbedaan ini menjadi semakin penting ketika context dan ScriptPack vocabulary ikut berperan.



\---



\# 7. Stress Test Ketiga: `kya`



Kasus:



```text

kya

```



membantu kita melihat perbedaan antara sequence Latin dan struktur ortografis.



Secara konseptual:



```text

kya

&#x20;↓

K + Y + A

```



Kemudian:



```text

Resolver

&#x20;↓

BASE(K)

\+

PENGKAL(Y)

\+

INHERENT A

```



Dan akhirnya Composer menghasilkan representasi Aksara Jawa yang sesuai.



Poin penting dari kasus ini adalah:



> Tokenizer tidak perlu memiliki token `KYA`.



Membuat setiap kemungkinan kombinasi seperti:



```text

KYA

KRY

KRA

KANG

NYA

NYI

...

```



sebagai token akan menyebabkan ledakan kombinatorial.



Karena itu muncul prinsip:



> \*\*Tokenizer tidak boleh menjadi syllable generator.\*\*



\---



\# 8. Composite Orthography ≠ Composite Lexical Token



Dari kasus `kya` dan `kh`, muncul pembedaan yang sangat penting.



\### `kya`



Dapat dipahami sebagai:



```text

K + Y + A

```



Kemudian baru menghasilkan struktur ortografis tertentu.



\### `kh`



Dapat menjadi:



```text

KH

```



jika ScriptPack mendefinisikannya sebagai dedicated phonetic token.



Maka:



```text

Composite Orthography

&#x20;       ≠

Composite Lexical Token

```



Tidak semua sequence multi-character harus diperlakukan sebagai satu token.



Sebaliknya, tidak semua sequence multi-character boleh langsung dipecah menjadi token-token individual.



Keputusan tersebut harus bergantung pada identitas dan vocabulary token yang valid.



\---



\# 9. Tokenizer Bukan Mini Grammar Engine



Dari beberapa stress test, muncul risiko arsitektural yang jelas.



Kita tidak boleh membuat tokenizer seperti:



```text

tokenize("kya")

→ \["KYA"]



tokenize("kang")

→ \["KANG"]

```



Jika semua kemungkinan struktur ortografis dimasukkan ke tokenizer, maka tokenizer akan berubah menjadi:



> \*\*Mini grammar engine\*\*



Hal tersebut akan:



\- mencampurkan token recognition dengan grammar;

\- membuat testing lebih sulit;

\- meningkatkan jumlah kombinasi yang harus dikenali;

\- menyulitkan ScriptPack-driven design;

\- menyebabkan logic context-sensitive tersebar.



Model yang lebih sehat adalah:



```text

Tokenizer

&#x20;   ↓

Atomic meaningful units



Resolver

&#x20;   ↓

Orthographic interpretation



Composer

&#x20;   ↓

Javanese Unicode

```



\---



\# 10. Pertanyaan yang Belum Boleh Dijawab Sembarangan



Workshop kemudian mencapai kasus-kasus yang lebih kompleks:



```text

ngka

angka

krya

```



Di sinilah mulai muncul kebutuhan untuk mempertimbangkan:



\- syllable boundary;

\- previous context;

\- lookahead;

\- cluster;

\- pasangan;

\- modifier;

\- final consonant.



Kita menyadari bahwa rule sederhana:



```text

consonant + vowel = syllable

```



tidak cukup.



Struktur ortografi dapat melibatkan:



```text

base

\+

modifier

\+

pasangan

\+

final consonant

```



Karena itu Phase 2C tidak boleh diselesaikan dengan parser sederhana yang mengasumsikan setiap consonant-vowel pair sebagai satu suku kata.



\---



\# 11. Struktur Workshop Phase 2C



Untuk menjaga pembahasan tetap terarah, workshop secara konseptual dibagi menjadi tiga bagian:



```text

Phase 2C

│

├── 2C.1 Token Taxonomy

│       ↓

│   Apa saja atomic token?

│

├── 2C.2 Tokenization Rules

│       ↓

│   Bagaimana Latin dipecah?

│

└── 2C.3 Orthographic Resolution

&#x20;       ↓

&#x20;   Bagaimana token stream

&#x20;   diterjemahkan berdasarkan context?

```



Pada titik ini, `ng` dan `ny` tidak langsung diputuskan dengan rule final.



Sebaliknya, keduanya digunakan sebagai \*\*stress-test cases\*\*.



\---



\# 12. Candidate Token Classes



Dalam proses workshop muncul taxonomy sementara:



| Candidate Class | Contoh | Catatan |

|---|---|---|

| Base consonant | `k`, `r`, `m` | Dapat memperoleh role berbeda melalui resolution |

| Vowel | `a`, `i`, `u` | Dapat memiliki interpretasi ortografis berdasarkan context |

| Dedicated multi-character token | `kh`, `gh`, `dz` | Memiliki identitas token tersendiri |

| Context-sensitive sequence | `ng`, `ny` | Membutuhkan context untuk menentukan role |

| Punctuation | `,`, `.` | Structural token |

| Digit | `0–9` | Structural/special token |

| Whitespace | space, newline, tab | Boundary/structural information |

| Unknown | `@`, emoji, dan lainnya | Mengikuti unknown-handling contract |



Namun taxonomy ini tidak langsung di-lock seluruhnya.



Ada pertanyaan penting:



> Apakah `y`, `r`, `h`, atau `ng` harus memiliki token class ortografis tersendiri?



Masalahnya:



```text

Y\_TOKEN

```



tidak otomatis berarti:



```text

PENGKAL

```



Begitu juga token lain.



Sebuah token dapat memiliki identitas yang tetap, tetapi memperoleh role yang berbeda berdasarkan context.



Dari sinilah lahir salah satu prinsip terpenting Phase 2C.



\---



\# 13. 2C-DECISION-001 — Token Identity ≠ Orthographic Role



Keputusan pertama yang muncul dari workshop adalah:



> \*\*Token identity dan orthographic role harus dipisahkan.\*\*



Contoh:



```text

Input:

kya



Token Stream:

K + Y + A

```



Kemudian:



```text

Resolution:



K → BASE

Y → PENGKAL

A → inherent vowel

```



Baru kemudian Composer menghasilkan representasi Unicode yang sesuai.



Contoh lain:



```text

Input:

ng



Token Stream:

NG

```



Pada tahap tokenizer, kita tidak membuat:



```text

Token(

&#x20;   text="ng",

&#x20;   role="panyigeg"

)

```



Model tersebut akan mencampurkan recognition dengan contextual interpretation.



Model yang lebih tepat adalah:



```text

Token(

&#x20;   text="ng",

&#x20;   kind=NG

)

```



Kemudian:



```text

Resolver

&#x20;   ↓

OrthographicRole

```



Misalnya:



```text

OrthographicRole.PANYIGEG

```



jika context memang mengarah ke sana.



\### Status



```text

2C-DECISION-001

Token Identity

&#x20;       ≠

Orthographic Role



STATUS: LOCKED

```



\---



\# 14. Tiga Lapisan yang Semakin Jelas



Keputusan tersebut menghasilkan model mental yang lebih jelas:



```text

"What did the user type?"

&#x20;       ↓

&#x20;    TOKENIZER

&#x20;       ↓

"What does this token mean here?"

&#x20;       ↓

&#x20;    RESOLVER

&#x20;       ↓

"How is that represented?"

&#x20;       ↓

&#x20;    COMPOSER

```



Pemisahan ini memiliki keuntungan besar terhadap testing.



\### Tokenizer Test



```text

"kh"  → \[KH]

"ng"  → \[NG]

"kya" → \[K, Y, A]

```



Tokenizer tidak perlu mengetahui Unicode Aksara Jawa.



\### Resolver Test



```text

NG + context

&#x20;   ↓

orthographic role

```



Resolver tidak perlu mengetahui detail final glyph composition.



\### Composer Test



```text

BASE(K)

\+

PENGKAL

\+

A

&#x20;   ↓

final Unicode sequence

```



Composer tidak perlu melakukan token recognition.



Dengan demikian, setiap tahap dapat diuji secara terpisah.



\---



\# 15. Token Matching dan Longest Valid Token



Setelah prinsip pertama disepakati, workshop beralih ke masalah berikutnya.



Misalnya:



```text

kh

```



Terdapat candidate:



```text

K + H

KH

```



Jika `KH` merupakan dedicated token yang valid, maka `KH` harus dipilih.



Rule konseptual yang muncul adalah:



```text

1\. Cari candidate multi-character tokens.

2\. Pertimbangkan kandidat dari sequence yang lebih panjang.

3\. Gunakan kandidat yang valid menurut vocabulary/contract ScriptPack.

4\. Jika kandidat tidak dapat digunakan, fallback ke token yang lebih pendek.

5\. Unknown character mengikuti unknown-handling contract.

```



Prinsip ini disebut:



> \*\*Longest Valid Token\*\*



Yang penting:



```text

Longest Valid Token

&#x20;       ≠

Longest String Match

```



Tokenizer tidak boleh hanya menggunakan greedy string matching tanpa mempertimbangkan vocabulary yang benar.



\---



\# 16. Pertanyaan Baru: Valid Menurut Apa?



Ketika kita menggunakan istilah:



> "valid menurut ScriptPack"



muncul kebutuhan untuk memperjelas kata \*\*valid\*\*.



Contoh:



```text

KH

```



mungkin valid sebagai token.



Namun sequence:



```text

KH + Y + ...

```



belum tentu menghasilkan struktur ortografis yang valid.



Dari sini muncul pembedaan penting berikutnya:



```text

TOKEN VALIDITY

&#x20;       ≠

SEQUENCE VALIDITY

```



Token recognition dan orthographic validation bukan pekerjaan yang sama.



Secara konseptual:



```text

Tokenizer

&#x20;   ↓

Apakah token ini dapat dikenali?



Resolver

&#x20;   ↓

Apakah token-token ini membentuk

struktur ortografis yang dapat diterima?

```



Prinsip ini menjadi salah satu hasil penting dari workshop Phase 2C.



\---



\# 17. `ng` dan `ny` sebagai Stress Test



Kasus `ng` dan `ny` membantu menguji apakah pemisahan arsitektural yang kita buat benar-benar sehat.



Model:



```text

"ng"

&#x20;↓

NG\_TOKEN

&#x20;↓

Resolver

&#x20;↓

Role berdasarkan context

```



Dan:



```text

"ny"

&#x20;↓

NY\_TOKEN

&#x20;↓

Resolver

&#x20;↓

Role berdasarkan context

```



Yang penting, kita tidak membuat kombinasi seperti:



```text

NYA

NYI

NYU

NYE

NYO

```



sebagai token-token baru.



Vowel tetap dapat diperlakukan sebagai token terpisah.



Hal ini membantu menghindari ledakan jumlah token.



Namun detail algoritma context dan lookahead tidak dipaksakan untuk diselesaikan secara sembarangan pada tahap ini.



\---



\# 18. `kh` sebagai Stress Test Dedicated Token



Kasus `kh` membantu menguji prinsip yang berbeda.



Jika ScriptPack mendefinisikan `kh` sebagai dedicated Rekan token:



```text

kh

&#x20;↓

KH\_TOKEN

```



maka tokenizer tidak boleh otomatis memecahnya menjadi:



```text

K + H

```



Tanpa alasan.



Ini memberikan prioritas konseptual:



```text

Dedicated valid token

&#x20;       ↓

preferred over

&#x20;       ↓

decomposition into shorter tokens

```



Namun kata \*\*valid\*\* tetap harus dipahami secara hati-hati.



Kita tidak ingin membuat algoritma yang menganggap setiap multi-character sequence otomatis lebih benar hanya karena lebih panjang.



\---



\# 19. Apa yang Berhasil Di-LOCK?



Setelah workshop Phase 2C, beberapa prinsip memiliki tingkat kepastian yang cukup untuk dikunci.



\## 19.1 Token Identity ≠ Orthographic Role



```text

STATUS: LOCKED

```



Tokenizer mengenali identitas token.



Resolver menentukan makna ortografis token berdasarkan context.



\---



\## 19.2 Tokenizer Tidak Boleh Menjadi Grammar Engine



```text

STATUS: LOCKED AS ARCHITECTURAL DIRECTION

```



Tokenizer tidak seharusnya menghasilkan seluruh kemungkinan kombinasi suku kata atau struktur ortografis.



Contoh:



```text

kya

```



tidak harus menjadi:



```text

\[KYA]

```



jika dapat dipahami sebagai:



```text

\[K] \[Y] \[A]

```



yang kemudian diinterpretasikan oleh Resolver.



\---



\## 19.3 Dedicated Multi-character Token Harus Dibedakan dari Orthographic Combination



```text

STATUS: LOCKED AS CONCEPTUAL PRINCIPLE

```



Tidak semua multi-character sequence adalah satu token.



Sebaliknya, beberapa sequence memang memiliki identitas token tersendiri.



```text

Composite Orthography

&#x20;       ≠

Composite Lexical Token

```



\---



\## 19.4 Longest Valid Token



```text

STATUS: LOCKED AS TOKEN-MATCHING PRINCIPLE

```



Token matching tidak menggunakan longest string match secara buta.



Candidate harus memiliki dasar validitas yang sesuai dengan vocabulary dan kontrak ScriptPack.



\---



\## 19.5 Token Validity ≠ Sequence Validity



```text

STATUS: LOCKED AS ARCHITECTURAL PRINCIPLE

```



Sebuah token dapat valid secara individual, tetapi sequence token tersebut belum tentu valid secara ortografis.



\---



\# 20. Apa yang Masih OPEN?



Phase 2C tidak bertujuan untuk menyelesaikan seluruh detail implementasi.



Beberapa hal masih sengaja dibiarkan terbuka.



\## 20.1 Exact Token Taxonomy



Candidate classes telah dibahas.



Namun detail class hierarchy final tidak boleh dianggap selesai hanya berdasarkan workshop konseptual.



\---



\## 20.2 Lookahead Strategy



Kita mengetahui bahwa beberapa kasus memerlukan context dan kemungkinan lookahead.



Namun:



\- berapa jumlah lookahead;

\- kapan digunakan;

\- bagaimana state dikelola;



belum perlu dipaksakan sebelum test contract.



\---



\## 20.3 Syllable Boundary Algorithm



Kasus:



```text

ngka

angka

krya

```



menunjukkan bahwa boundary detection tidak sesederhana:



```text

consonant + vowel

```



Algoritma konkret masih memerlukan contract dan test yang lebih jelas.



\---



\## 20.4 Exact Resolver Algorithm



Prinsip tanggung jawab Resolver telah semakin jelas.



Namun implementasi state machine atau algoritma konkret belum dipilih.



\---



\## 20.5 Final API dan Class Layout



Workshop ini bukan tempat untuk langsung menentukan:



```text

class Tokenizer:

&#x20;   ...

```



atau signature final setiap method.



Hal tersebut harus mengikuti keputusan arsitektur dan test contract.



\---



\# 21. Pelajaran Arsitektural dari Phase 2C



Phase 2C menghasilkan beberapa pelajaran penting.



\### Pertama



Masalah transliterasi tidak dapat diselesaikan hanya dengan:



```text

dictionary lookup

```



karena representasi dapat bergantung pada context.



\---



\### Kedua



Tidak semua complexity harus dimasukkan ke tokenizer.



Jika tokenizer terlalu pintar, ia berubah menjadi grammar engine.



\---



\### Ketiga



Identity dan role adalah dua konsep berbeda.



```text

What is this token?

&#x20;       ≠

What does this token mean here?

```



\---



\### Keempat



Tokenization dan orthographic validation merupakan dua level validasi yang berbeda.



```text

Valid token

&#x20;       ≠

Valid sequence

```



\---



\### Kelima



Stress test sederhana seperti:



```text

ng

ny

kh

kya

```



lebih berguna daripada langsung merancang algoritma abstrak.



Kasus-kasus tersebut memaksa arsitektur menjawab pertanyaan nyata.



\---



\# 22. Posisi Phase 2C dalam Perjalanan AD-TR-01



Perjalanan kita sampai titik ini dapat digambarkan sebagai berikut:



```text

Phase 0

Repository Reconnaissance

&#x20;       ↓

Phase 1

Contract Exploration

&#x20;       ↓

Phase 1B

Orthographic Contract Workshop

&#x20;       ↓

Phase 1C

Invalid, Ambiguous \& Context Cases

&#x20;       ↓

Consolidated Contract Rules v0.1

&#x20;       ↓

Phase 2A

Implementation Reconnaissance

&#x20;       ↓

Phase 2B

Capability Boundary \& Diagnostic API

&#x20;       ↓

Phase 2C

Tokenization \& Orthographic Resolution

&#x20;       ↓

Phase 2D

Core Test Contract

```



Phase 2C bukan sekadar "menentukan tokenizer".



Phase ini menjadi jembatan antara:



```text

High-level Contract

&#x20;       ↓

Actual Token Stream

&#x20;       ↓

Context-sensitive Orthography

```



\---



\# 23. Transisi ke Phase 2D



Setelah Phase 2C, kita belum langsung menulis production code.



Langkah berikutnya adalah:



> \*\*AD-TR-01 — Phase 2D — Core Test Contract\*\*



Tujuan Phase 2D adalah menerjemahkan hasil perjalanan sebelumnya menjadi behavior yang dapat diuji.



Fokus berikutnya:



```text

Contract

&#x20;   ↓

Test Matrix

&#x20;   ↓

Executable Tests

&#x20;   ↓

Implementation

```



Dengan demikian, implementasi nanti tidak dimulai dari intuisi.



Ia harus mengikuti:



\- contract yang telah dibangun;

\- architecture boundary yang telah disepakati;

\- keputusan Phase 2C;

\- test contract yang dapat diverifikasi.



\---



\# 24. Final Status



```text

AD-TR-01 — Phase 2C

Tokenization \& Orthographic Resolution



Architecture Workshop: COMPLETED

Key Principles: LOCKED

Implementation Algorithm: NOT YET IMPLEMENTED

Production Code: NOT YET CHANGED



NEXT:

AD-TR-01 — Phase 2D

Core Test Contract

```



\---



\# 25. Documentation Trace



Dokumen ini merupakan bagian dari catatan perjalanan AD-TR-01.



```text

01 — Phase 0 Reconnaissance



02 — Phase 1 — Transliteration Contract



03 — Phase 1 — Contract Deep Dive



04 — Phase 1B — Orthographic Contract Workshop



05 — Phase 1C — Invalid, Ambiguous \& Context Cases



06 — Transliteration Contract Rules v0.1



07 — Phase 2A — Implementation Reconnaissance



08 — Phase 2B — Capability \& Diagnostic API



09 — Phase 2C — Tokenization \& Orthographic Resolution

```



\---



\# Penutup



Phase 2C mengajarkan kita bahwa pertanyaan:



> \*\*"Bagaimana cara memecah input Latin?"\*\*



ternyata tidak dapat dijawab tanpa terlebih dahulu memisahkan tiga pertanyaan yang berbeda:



```text

What did the user type?

&#x20;       ↓

Tokenization



What does it mean here?

&#x20;       ↓

Orthographic Resolution



How should it be represented?

&#x20;       ↓

Composition

```



Pemisahan inilah yang menjadi hasil paling penting dari workshop Phase 2C.



Bukan karena kita telah menemukan seluruh algoritma transliterasi.



Justru sebaliknya.



Kita berhasil mengidentifikasi \*\*di mana setiap jenis complexity seharusnya hidup\*\*, sebelum complexity tersebut berubah menjadi kode.



> \*\*That is the purpose of the workshop.\*\*

>

> \*\*Understand the problem before implementing the solution.\*\*

