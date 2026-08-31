# AD-TR-01 — Phase 1: Koreksi

| Field | Value |
|---|---|
| Status | Locked — correction to the initial Phase 1 model |
| Date | 2026-08-29 |
| Intended repository location | `docs/decisions/03_AD_TR_01_PHASE_1_KOREKSI.md` |
| Corrects | `02_AD_TR_01_PHASE_1_AWAL_DRAFT.md` |
| Continued by | `04_AD_TR_01_PHASE_1B_ORTHOGRAPHIC_CONTRACT_WORKSHOP.md` |

## Reason for correction

Real ScriptPack data shows distinct behavior classes:

```text
Independent / base: nglegena, swara, murda, rekan
Dependent / modifier: pasangan, sandhangan_swara,
                      sandhangan_wyanjana, sandhangan_panyigeg
Non-letter: angka, pada
```

Examples: `nglegena/ka` (`ꦏ`, `ka`) has inherent `a`; `wulu` (`ꦶ`, `i`) changes a preceding base vowel; `pangkon` has empty Latin and suppresses the preceding inherent vowel. Thus global `latin → glyph` or `glyph → latin` replacement cannot express composition/decomposition.

## Corrected decisions

| ID | Decision | Status | Reason / corrected assumption |
|---|---|---|---|
| TR-CORR-001 | Derive roles from existing category, `id`, `latin`, and `description`; do not add `role` to JSON now. | Locked | Character Model v1.0 and interface are stable; current data is sufficient for contract discovery. |
| TR-CORR-002 | Use context-aware character-sequence composition/decomposition. | Locked | Supersedes character/global-string replacement. |
| TR-CORR-003 | Longest-match is a tokenizer tool but cannot decide syllable boundaries or pasangan. | Locked | Corrects over-reliance on lexical matching. |
| TR-CORR-004 | `latin` is canonical character representation, not a complete bidirectional grammar. | Locked | Reverse output can depend on category and context. |
| TR-CORR-005 | Do not invent undocumented combinations. | Locked | Unsupported sequences need explicit later policy. |

## Resulting model

```text
Latin text
  → tokenize and segment where the contract permits
  → interpret an orthographic unit
  → compose a ScriptPack character sequence

Javanese text
  → read character sequence and roles
  → decompose an orthographic unit
  → emit canonical Latin representation
```

This correction selects no implementation API and does not change Foundation v1.0.
