# AD-TR-01 — Phase 1: Awal / Draft

| Field | Value |
|---|---|
| Status | Superseded in part — retained as design history |
| Date | 2026-08-29 |
| Intended repository location | `docs/decisions/02_AD_TR_01_PHASE_1_AWAL_DRAFT.md` |
| Preceded by | `01_AD_TR_01_PHASE_0_RECONNAISSANCE.md` |
| Superseded in part by | `03_AD_TR_01_PHASE_1_KOREKSI.md` |

## Purpose

The initial Phase 1 draft established the service boundary and identified questions to answer before code is written. It did not treat dictionary mapping as a complete orthographic solution.

## Draft direction model

```text
Latin input       → Javanese composition
Javanese input    → Latin decomposition

string input → normalization / analysis → transliteration → string output
```

## Contract register

| ID | Draft contract | Status |
|---|---|---|
| TR-IO-001 | Input and output are strings. | Proposed |
| TR-IO-002 | Empty input produces empty output. | Proposed |
| TR-IO-003 | Preserve spaces, tabs, and line breaks exactly; do not normalize whitespace automatically. | Locked |
| TR-IO-004 | Preserve general unknown characters rather than silently discard them. | Proposed |
| TR-IO-005 | Processing is deterministic, with no UI or persistence dependency. | Locked |
| TR-ARCH-006 | Character repository supplies data; ScriptPack owns linguistic behavior. | Locked |

## Initial tokenizer observation

Multi-character Latin units such as `ng`, `ny`, `dh`, and `th` require longest-match recognition before shorter components. This is a **proposed tokenizer technique**, not a final rule for syllable segmentation, pasangan, or complete Javanese orthography.

## Open decisions retained for later phases

1. Invalid Javanese sequences.
2. Strict versus best-effort Latin-to-Javanese processing.
3. Ambiguous Latin units and syllable boundaries.
4. Murda and rekan generation/recognition policy.
5. Number formatting beyond digit substitution.
6. Pangkon and consonant-cluster behavior.
7. `swara` versus `nglegena + sandhangan` for vowel-initial input.
8. The precise scope of a round-trip guarantee.

## Why this draft was corrected

The direction and boundary remain useful, but later review of ScriptPack data established that `latin` values alone do not define character composition. The correction is retained in the next document rather than rewriting this draft out of history.
