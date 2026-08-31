# AD-TR-01 — Transliteration Contract
## Consolidated Contract Rules v0.1

> **Status:** Consolidated Draft  
> **Purpose:** Menetapkan seluruh contract rules TR-001 sampai TR-018 yang sebelumnya tersebar di Phase 1B, agar menjadi baseline implementasi AD-TR-01 tanpa perlu membahas setiap rule satu per satu di percakapan.

---

## 1. Contract Scope

AD-TR-01 menangani transliterasi antara representasi Latin dan bentuk ortografis Aksara Jawa.

```text
Latin phonetic representation
            ↕
Javanese orthographic form
```

AD-TR-01 tidak bertujuan menjadi engine language-aware untuk menerjemahkan bahasa Indonesia/Jawa atau melakukan analisis linguistik tingkat lanjut.

Scope utama:
- character transliteration
- orthographic composition
- orthographic decomposition
- ScriptPack-driven rules
- deterministic processing
- UI-independent implementation

Di luar scope:
- natural-language translation
- language-aware spelling correction
- automatic linguistic disambiguation yang membutuhkan semantic knowledge di luar ScriptPack
- redesign Flashcard, Quiz, Learning Engine, atau subsystem lain

---

# 2. TR-001 — Direction

Transliteration subsystem mendukung:

```text
LATIN → JAVANESE
JAVANESE → LATIN
```

Kedua arah merupakan operasi berbeda secara algoritmik.

### Latin → Javanese
```text
Latin
  ↓
Tokenization
  ↓
Orthographic interpretation
  ↓
Composition
  ↓
Javanese Unicode
```

### Javanese → Latin
```text
Javanese Unicode
  ↓
Character scanning
  ↓
Sequence parsing
  ↓
Orthographic interpretation
  ↓
Latin
```

**Status: LOCKED**

---

# 3. TR-002 — Base / Inherent Vowel

Nglegena merupakan base consonant dengan inherent vowel `a`.

Contoh:

```text
ha → ꦲ
na → ꦤ
ca → ꦕ
ra → ꦫ
ka → ꦏ
```

Tidak diperlukan sandhangan untuk merepresentasikan vowel `a`.

**Status: LOCKED**

---

# 4. TR-003 — Vowel Modifier

Sandhangan Swara menggantikan inherent vowel dari base consonant.

Dataset:

```text
wulu          → i
suku          → u
pepet         → eu
taling        → e
taling-tarung → o
```

Contoh:

```text
ka  → ꦏ
ki  → ꦏꦶ
ku  → ꦏꦸ
keu → ꦏꦼ
ke  → ꦏꦺ
ko  → ꦏꦺꦴ
```

Rule:

```text
BASE + vowel modifier
        ↓
replace inherent vowel
```

**Status: LOCKED**

---

# 5. TR-004 — Wyanjana

Sandhangan Wyanjana dapat menambahkan atau memodifikasi consonant pada syllable host.

Dataset:

```text
cakra    → r
pengkal  → y
keret    → reu
```

Contoh:

```text
kra  → ꦏꦿ
kya  → ꦏꦾ
kreu → ꦏꦽ
```

`keret` merupakan modifier khusus karena dapat sekaligus menambahkan consonant `r` dan mengubah vowel menjadi `reu`.

**Status: LOCKED**

---

# 6. TR-005 — Panyigeg

Sandhangan Panyigeg membentuk final consonant atau mengubah vowel state.

Dataset:

```text
wignyan → h
layar   → r
cecak   → ng
pangkon → ""
```

Contoh:

```text
kah  → ꦏꦃ
kar  → ꦏꦂ
kang → ꦏꦁ
```

**Status: LOCKED**

---

# 7. TR-006 — Pangkon

Pangkon menghilangkan inherent vowel dari base consonant.

```text
ka + pangkon
     ↓
k
```

Contoh:

```text
k → ꦏ꧀
ꦏ꧀ → k
```

Pangkon adalah state-changing modifier terhadap base sebelumnya, bukan sekadar character dengan Latin mapping kosong.

**Status: LOCKED**

---

# 8. TR-007 — Pasangan

Pasangan merepresentasikan following consonant tanpa independent inherent vowel.

Secara konseptual:

```text
BASE₁ + PASANGAN₂
```

merupakan consonant sequence/cluster, bukan dua independent syllables.

Contoh structural case:

```text
ꦏ꧀ꦩ
```

ditafsirkan pada component level sebagai:

```text
k + m
```

bukan:

```text
ka + ma
```

Pasangan diproses berdasarkan context dan tidak boleh direduksi menjadi global `latin → glyph` lookup.

**Status: LOCKED — STRUCTURAL RULE**

---

# 9. TR-008 — Swara / Independent Vowels

Independent vowels menggunakan karakter `swara`.

Dataset:

```text
a → ꦄ
i → ꦆ
u → ꦈ
e → ꦌ
o → ꦎ
```

Rule:

> Vowel-initial syllables menggunakan `swara`, bukan base consonant + sandhangan.

**Status: LOCKED**

---

# 10. TR-009 — Rekan

Rekan merupakan canonical representation untuk dedicated phonetic tokens yang tidak memiliki equivalent normal Nglegena.

Dataset:

```text
kh → ꦏ꦳
gh → ꦒ꦳
dz → ꦢ꦳
f  → ꦥ꦳
v  → ꦮ꦳
z  → ꦗ꦳
```

Dedicated tokens harus dikenali sebelum dipecah menjadi consonant individual.

Contoh:

```text
kh
```

tidak boleh secara default ditafsirkan sebagai `k + h`.

**Status: LOCKED**

---

# 11. TR-010 — Murda

Murda dikenali pada reverse transliteration.

Murda tidak dipilih otomatis pada canonical Latin → Javanese apabila Latin input tidak memberikan informasi yang cukup untuk menentukan bahwa bentuk Murda diinginkan.

Contoh:

```text
ka → ꦏ
```

bukan:

```text
ka → ꦑ
```

Sebaliknya, bentuk Murda yang ditemukan pada Javanese input tetap harus dikenali sesuai data ScriptPack.

Catatan: jika dataset saat ini memberikan nilai Latin yang tampak tidak intuitif, engine mengikuti data ScriptPack yang berlaku dan tidak mengoreksi data secara diam-diam.

**Status: LOCKED TO CURRENT SCRIPT DATA**

---

# 12. TR-011 — Digits

Angka merupakan independent token.

```text
0 → ꧐
1 → ꧑
2 → ꧒
3 → ꧓
4 → ꧔
5 → ꧕
6 → ꧖
7 → ꧗
8 → ꧘
9 → ꧙
```

Contoh:

```text
123 → ꧑꧒꧓
```

Reverse:

```text
꧑꧒꧓ → 123
```

Aturan formatting angka yang lebih luas belum menjadi bagian contract ini.

**Status: LOCKED FOR DIGIT TRANSLITERATION**

---

# 13. TR-012 — Punctuation

Punctuation yang memiliki mapping di ScriptPack ditransliterasikan.

Contoh:

```text
, → ꧈
. → ꧉
```

Punctuation umum tanpa mapping ScriptPack dipertahankan:

```text
? → ?
! → !
: → :
; → ;
```

**Status: LOCKED**

---

# 14. TR-013 — Whitespace

Whitespace harus dipertahankan.

```text
space
tab
newline
```

tidak boleh dinormalisasi otomatis oleh transliteration engine.

Engine tidak boleh melakukan `.strip()` sebagai bagian dari transliteration contract.

**Status: LOCKED**

---

# 15. TR-014 — Unknown Characters

Karakter eksternal yang tidak dikenal ScriptPack tidak otomatis dianggap error.

Contoh:

```text
@
#
$
emoji
```

Jika tidak mempunyai mapping, karakter dipertahankan.

```text
unknown external character
        ↓
preserve
```

Hal ini berbeda dari karakter ScriptPack yang dikenal tetapi digunakan dalam context invalid.

**Status: LOCKED**

---

# 16. TR-015 — Determinism

Untuk:

```text
input yang sama
+
direction yang sama
+
ScriptPack yang sama
```

engine harus menghasilkan output yang sama.

Tidak boleh ada hasil acak atau behavior yang bergantung pada UI state.

**Status: LOCKED**

---

# 17. TR-016 — No UI Dependency

Transliteration engine tidak boleh bergantung pada:

- PySide6 widget
- `TransliterasiTab`
- UI state
- signal/slot
- clipboard
- visual rendering
- user interaction

UI hanya menjadi presentation/boundary layer.

Target architecture:

```text
UI
 ↓
Application Boundary
 ↓
ScriptPack / Transliteration Capability
 ↓
Transliteration Engine
```

**Status: LOCKED**

---

# 18. TR-017 — No Persistence

Transliteration engine tidak boleh:

- membaca database
- menulis database
- membaca learner data
- menulis learning history
- bergantung pada JSONAdapter
- menyimpan state transliteration ke storage

Engine harus dapat dipanggil sebagai operasi deterministic tanpa persistence.

**Status: LOCKED**

---

# 19. TR-018 — ScriptPack Ownership

Aturan transliterasi yang bersifat writing-system-specific menjadi tanggung jawab ScriptPack.

Core Engine menyediakan infrastructure/capability boundary, tetapi tidak mengimplementasikan linguistic rules Aksara Jawa.

```text
Core Engine
    │
    └── infrastructure / capability access
                 │
                 ▼
             ScriptPack
                 │
                 └── transliteration rules
```

Core Engine tidak boleh menjadi tempat hard-coded rules seperti:

```text
ka → ꦏ
ki → ꦏꦶ
kh → ꦏ꦳
...
```

Aturan tersebut merupakan tanggung jawab implementation ScriptPack.

**Status: LOCKED**

---

# 20. Cross-Cutting Principles

## 20.1 Character Repository ≠ Grammar

Character Repository menyediakan vocabulary/character definitions.

Transliteration engine menyediakan:

```text
grammar
+
context
+
composition
+
decomposition
```

`latin` field merupakan representation/component data, bukan keseluruhan grammar transliterasi.

## 20.2 Context Matters

`latin` tidak selalu globally unique.

Contoh:

```text
nga → Nglegena
ng  → Pasangan / Panyigeg
nya → Nglegena
ny  → Pasangan
```

Karena itu global dictionary sederhana:

```python
latin_to_glyph[latin]
```

tidak boleh menjadi mekanisme utama.

## 20.3 Longest Valid Token

Untuk Latin → Javanese:

> **Longest valid token match within the applicable phonetic/orthographic class.**

Yang dipilih bukan sekadar string terpanjang, tetapi token valid menurut ScriptPack.

## 20.4 Canonical Generation vs Recognition

Forward:

```text
Latin → Javanese
```

menghasilkan canonical/default representation.

Reverse:

```text
Javanese → Latin
```

mengenali valid representations yang diberikan ScriptPack.

---

# 21. Round-Trip Policy

AD-TR-01 tidak menjamin textual identity untuk:

```text
Latin → Javanese → Latin
```

atau:

```text
Javanese → Latin → Javanese
```

Karena beberapa representasi memiliki context, Murda memiliki ambiguity terhadap default consonants, dan transliteration dapat melakukan canonicalization.

Yang dijamin:

> **canonical semantic/orthographic interpretation sesuai contract dan data ScriptPack.**

Karena itu golden tests menggunakan expected canonical output, bukan selalu:

```python
assert reverse(forward(x)) == x
```

---

# 22. Error / Diagnostic Foundation

Contract membedakan:

## UNKNOWN

Karakter eksternal tidak dikenal.

```text
→ preserve
→ bukan error
```

## INVALID_CONTEXT

Character dikenal tetapi penggunaannya invalid.

Contoh:

```text
ꦶ
```

Sandhangan berdiri tanpa host.

```text
→ diagnostic
```

## UNSUPPORTED / INVALID ORTHOGRAPHIC SEQUENCE

Sequence tidak dapat dibentuk atau ditafsirkan menurut aturan ScriptPack.

Contoh candidate:

```text
kry
```

```text
→ diagnostic
```

Engine tidak boleh diam-diam mengubahnya menjadi orthography lain.

---

# 23. Partial Processing Principle

Error pada satu bagian input tidak otomatis membuang seluruh input.

Secara konseptual:

```text
valid segment
    → process

unknown external character
    → preserve

invalid segment
    → diagnostic
```

Valid segments yang tidak berkaitan tetap dapat diproses.

Detail API/result object belum dikunci di tahap contract ini.

---

# 24. Golden Test Seed

Initial golden cases:

```text
ka   → ꦏ
ki   → ꦏꦶ
ku   → ꦏꦸ
keu  → ꦏꦼ
ke   → ꦏꦺ
ko   → ꦏꦺꦴ

k    → ꦏ꧀
kah  → ꦏꦃ
kar  → ꦏꦂ
kang → ꦏꦁ

kra  → ꦏꦿ
kya  → ꦏꦾ
kreu → ꦏꦽ

kh   → ꦏ꦳
gh   → ꦒ꦳
dz   → ꦢ꦳
f    → ꦥ꦳
v    → ꦮ꦳
z    → ꦗ꦳

a    → ꦄ
i    → ꦆ
u    → ꦈ
e    → ꦌ
o    → ꦎ

123  → ꧑꧒꧓

,    → ꧈
.    → ꧉
```

Reverse cases:

```text
ꦏ     → ka
ꦏꦶ    → ki
ꦏ꧀    → k
ꦏꦃ    → kah
ꦏꦂ    → kar
ꦏꦁ    → kang
ꦏꦿ    → kra
ꦏꦾ    → kya
ꦏ꦳    → kh
ꦑ     → k       # mengikuti current ScriptPack data
꧑꧒꧓ → 123
```

---

# 25. Known Edge Cases

```text
ꦶ       → invalid context / diagnostic
ꦏꦶ     → valid
ꦏ꧀     → valid
ꦏ꧀ꦩ   → structural consonant sequence
ꦑ       → Murda recognition
ꦏ꦳     → Rekan recognition
꧇       → open
꧋       → open
ꧏ       → open
kry     → unsupported candidate / diagnostic
ng      → context-dependent
ny      → context-dependent
```

---

# 26. Contract Status Summary

| Rule | Subject | Status |
|---|---|---|
| TR-001 | Direction | LOCKED |
| TR-002 | Base / inherent vowel | LOCKED |
| TR-003 | Vowel modifier | LOCKED |
| TR-004 | Wyanjana | LOCKED |
| TR-005 | Panyigeg | LOCKED |
| TR-006 | Pangkon | LOCKED |
| TR-007 | Pasangan | LOCKED — structural |
| TR-008 | Swara | LOCKED |
| TR-009 | Rekan | LOCKED |
| TR-010 | Murda | LOCKED — current data |
| TR-011 | Digits | LOCKED |
| TR-012 | Punctuation | LOCKED |
| TR-013 | Whitespace | LOCKED |
| TR-014 | Unknown | LOCKED |
| TR-015 | Determinism | LOCKED |
| TR-016 | UI independence | LOCKED |
| TR-017 | Persistence independence | LOCKED |
| TR-018 | ScriptPack ownership | LOCKED |

---

# 27. Open Items Before Phase 2

Detail berikut belum menjadi implementation contract final:

1. Exact diagnostic/result API.
2. Exact recovery strategy untuk invalid segments.
3. Final handling untuk `꧇`, `꧋`, dan `ꧏ`.
4. Detailed composition rules untuk pasangan + modifier combinations.
5. Final tokenizer behavior untuk seluruh ambiguous Latin sequences.
6. Orthographic combinations yang belum tersedia di ScriptPack.

Open items tidak boleh menjadi alasan untuk mengarang behavior baru. Jika implementasi membutuhkan keputusan yang belum tercantum, keputusan tersebut harus dicatat sebagai contract amendment terlebih dahulu.

---

# 28. Implementation Boundary

Phase 2 dapat mengimplementasikan:

```text
Transliteration Capability
        │
        ├── Latin → Javanese
        │      ├── tokenizer
        │      └── composer
        │
        └── Javanese → Latin
               ├── scanner
               └── parser
```

Engine harus:

- deterministic
- testable
- ScriptPack-driven
- UI-independent
- persistence-independent
- context-aware
- tidak menggunakan hard-coded Javanese mapping di UI

`TransliterasiTab` menjadi integration/presentation layer setelah core transliteration behavior stabil.

---

# 29. Next Step

Setelah consolidated contract ini diterima sebagai baseline:

```text
Contract
   ↓
Unit Tests / Golden Tests
   ↓
Implementation
   ↓
Core Integration
   ↓
TransliterasiTab Integration
   ↓
Integration Tests
   ↓
Regression Suite
   ↓
Manual Smoke Test
```

**Tidak perlu membahas TR-001 sampai TR-018 satu per satu lagi di chat**, kecuali implementasi menemukan conflict, ambiguity, atau evidence baru yang benar-benar memerlukan amendment terhadap contract.
