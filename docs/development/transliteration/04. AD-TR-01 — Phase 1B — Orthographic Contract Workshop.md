# AD-TR-01 — Phase 1B: Orthographic Contract Workshop

| Field | Value |
|---|---|
| Status | Proposed — selected foundational rules locked below |
| Date | 2026-08-29 |
| Intended repository location | `docs/decisions/04_AD_TR_01_PHASE_1B_ORTHOGRAPHIC_CONTRACT_WORKSHOP.md` |
| Preceded by | `03_AD_TR_01_PHASE_1_KOREKSI.md` |
| Next checkpoint | Phase 1C — Invalid, Ambiguous & Context Cases |

## Purpose

This workshop derives reusable orthographic contract rules from actual Javanese ScriptPack data. It is a test-design and contract artifact, not a claim of complete linguistic coverage or implemented behavior.

## Independent vowels

| Latin | Javanese |
|---|---|
| `a` | `ꦄ` |
| `i` | `ꦆ` |
| `u` | `ꦈ` |
| `e` | `ꦌ` |
| `o` | `ꦎ` |

**TR-SWARA-001 — Locked:** vowel-initial syllables use independent `swara`; canonical `a` is `ꦄ`.

## Inherent-vowel base and vowel modifiers

**TR-BASE-001 — Locked:** `nglegena` represents a consonant with inherent `a`; `ka → ꦏ`.

**TR-VOWEL-001 — Proposed:** a vowel modifier replaces the preceding base's inherent vowel.

| Base | Modifier | Latin result | Javanese |
|---|---|---|---|
| `ka` | — | `ka` | `ꦏ` |
| `ka` | wulu | `ki` | `ꦏꦶ` |
| `ka` | suku | `ku` | `ꦏꦸ` |
| `ka` | pepet | `keu` | `ꦏꦼ` |
| `ka` | taling | `ke` | `ꦏꦺ` |
| `ka` | taling-tarung | `ko` | `ꦏꦺꦴ` |

Data uses canonical `eu` for pepet; preserve `keu`, not an unrecorded `ə` substitution.

## Wyanjana modifiers

| Modifier | Evidenced effect | Example |
|---|---|---|
| cakra | adds medial `r` | `kra → ꦏꦿ` |
| pengkal | adds medial `y` | `kya → ꦏꦾ` |
| keret | adds `r`, replaces vowel with `eu` | `kreu → ꦏꦽ` |

**TR-MOD-001 — Locked:** a dependent character can have multiple effects; the engine MUST NOT assume it simply appends Latin text.

## Panyigeg and pangkon

| Latin | Javanese | Interpretation |
|---|---|---|
| `kah` | `ꦏꦃ` | wignyan adds final `h` |
| `kar` | `ꦏꦂ` | layar adds final `r` |
| `kang` | `ꦏꦁ` | cecak adds final `ng` |
| `k` | `ꦏ꧀` | pangkon suppresses inherent `a` |

**TR-PANGKON-001 — Proposed:** canonical final consonant is `k → ꦏ꧀`, with reverse `ꦏ꧀ → k`. Phase 1C must review contextual behavior first.

## Pasangan and segmentation

Pasangan represents a following consonant without an independent inherent vowel; it is not an independent syllable.

**TR-PASANGAN-001 — Proposed:** pasangan represents such a consonant after a preceding syllable.

**TR-PASANGAN-002 — Locked:** the engine MUST NOT apply “every consonant after a consonant is pasangan.” Latin-to-Javanese needs segmentation.

`kr` and `ky` can be medial clusters represented through `cakra` and `pengkal`. Do not generate undocumented combinations such as assumed simultaneous modifiers for `kry`.

## Rekan and murda

| Latin | Rekan glyph |
|---|---|
| `kh` | `ꦏ꦳` |
| `gh` | `ꦒ꦳` |
| `dz` | `ꦢ꦳` |
| `f` | `ꦥ꦳` |
| `v` | `ꦮ꦳` |
| `z` | `ꦗ꦳` |

**TR-TOKEN-001 — Proposed:** distinct rekan multi-character tokens have priority over shorter decompositions.

**TR-MURDA-001 — Proposed:** recognize murda in Script-to-Latin according to current data; do not select murda automatically for canonical Latin-to-Script generation. Current reverse transliteration is contextual: normal `ka` is `ka`, while pasangan and murda ka data use `k`.

## Digits, punctuation, and whitespace

**TR-NUM-001 — Proposed:** digits are independent tokens: `123 → ꧑꧒꧓` and reverse.

**TR-PUNCT-001 — Proposed:** map known pada `, → ꧈` and `. → ꧉`; preserve other punctuation until policy is locked.

**TR-IO-003 — Locked:** preserve whitespace exactly, including space, tab, and newline.

## Candidate golden corpus

| Family | Latin | Javanese |
|---|---|---|
| Base | `ha`, `na`, `ka`, `nga` | `ꦲ`, `ꦤ`, `ꦏ`, `ꦔ` |
| Vowel | `ki`, `ku`, `keu`, `ke`, `ko` | `ꦏꦶ`, `ꦏꦸ`, `ꦏꦼ`, `ꦏꦺ`, `ꦏꦺꦴ` |
| Wyanjana | `kra`, `kya`, `kreu` | `ꦏꦿ`, `ꦏꦾ`, `ꦏꦽ` |
| Final | `k`, `kah`, `kar`, `kang` | `ꦏ꧀`, `ꦏꦃ`, `ꦏꦂ`, `ꦏꦁ` |
| Rekan | `kh`, `gh`, `dz`, `f`, `v`, `z` | `ꦏ꦳`, `ꦒ꦳`, `ꦢ꦳`, `ꦥ꦳`, `ꦮ꦳`, `ꦗ꦳` |
| Swara | `a`, `i`, `u`, `e`, `o` | `ꦄ`, `ꦆ`, `ꦈ`, `ꦌ`, `ꦎ` |

## Phase 1C — required next checkpoint

Before implementation, record and decide invalid Javanese sequences; strict versus best-effort behavior and diagnostics; ambiguity/segmentation; pangkon interactions; final murda/rekan policy; digit/pada formatting scope; a defensible round-trip guarantee; and the capability boundary without unnecessary Foundation changes.

Use concrete sequence tables:

```text
Latin input
    ↓
Expected Javanese sequence
    ↓
Expected canonical Latin
    ↓
Underlying character roles
```
