# AD-TR-01 — Phase 1C: Invalid, Ambiguous & Context Cases

> **Record type:** Decision/workshop summary  
> **Scope:** AD-TR-01, Javanese ScriptPack transliteration contract  
> **Implementation status:** No implementation is authorized by this record. This document captures the workshop decisions and proposals made so far.

## 1. Purpose

Phase 1B established how valid Javanese orthographic components compose. Phase 1C records the complementary contract question:

> What shall the transliteration engine do when input is Unicode-valid but orthographically incomplete, invalid, context-dependent, or ambiguous?

This phase defines semantic behavior and diagnostic intent. It does **not** prescribe classes, return types, exceptions, recovery APIs, source-code changes, or a language-aware spelling engine.

### 1.1 Scope boundary

AD-TR-01 remains a Level 1 character/orthographic transliteration contract:

```text
Latin phonetic representation  <->  Javanese orthographic form
```

It is not an Indonesian/Javanese natural-language spelling, lexical, or phonological-analysis system.

## 2. Decision status legend

| Status | Meaning |
|---|---|
| **Locked** | Decision is agreed for the current contract. |
| **Locked provisionally** | Semantic policy is agreed; the API/mechanism remains unspecified. |
| **Proposed** | Recommended decision awaiting final confirmation or data validation. |
| **Open** | Deliberately unresolved; no final behavior may be inferred. |

## 3. Classification model

```text
Input
 ├─ Known + valid + unambiguous         -> transliterate
 ├─ Unknown external character          -> preserve
 ├─ Known character + invalid context   -> diagnostic
 └─ Ambiguous input
     ├─ deterministic context available -> resolve and process
     └─ context insufficient             -> diagnostic; do not guess silently
```

### 3.1 `UNKNOWN`

An external character has no relevant mapping or semantic role in the ScriptPack (for example an unsupported symbol or emoji).

- Preserve the character unchanged.
- Treat preservation as non-error behavior.
- Do not discard it merely because it is outside the recognized transliteration vocabulary.

**Status: Locked.**

### 3.2 `INVALID_CONTEXT`

The character or sequence is known to the ScriptPack, but its placement or composition is orthographically invalid—for example a dependent vowel without a host.

- Emit a diagnostic.
- Do not silently reinterpret the character as an independent letter.
- Keep the problematic input identifiable; the recovery representation/API remains out of scope.

**Status: Locked provisionally.**

### 3.3 `AMBIGUOUS`

The input can carry more than one semantic role or interpretation. Ambiguity is not automatically an error.

- Resolve only when the applicable phonetic/orthographic context makes the result deterministic.
- Otherwise emit a diagnostic rather than guessing.

Examples include `ng` and `ny`, whose meaning differs between nglegena, pasangan, and—in the case of `ng`—panyigeg.

**Status: Proposed.**

## 4. Forward transliteration cases (Latin → Javanese)

| ID | Input | Expected orthographic output | Decision | Status |
|---|---|---|---|---|
| TR-1C-001 | `k` | `ꦏ꧀` | A bare consonant is KA with pangkon; pangkon removes the inherent vowel. | **Locked** |
| — | `ka` | `ꦏ` | The inherent vowel `a` needs no vowel modifier. Canonical forward output uses nglegena, not Murda. | **Locked** |
| — | `ki` | `ꦏꦶ` | `i` is composed through wulu, replacing the inherent vowel. | **Locked** |
| TR-1C-002 | `kh` | `ꦏ꦳` | `kh` is a registered Rekan phonetic token, not the sequence `k + h`; do not compose it as `ꦏ꧀ꦲ`. | **Locked** |
| — | `kr` | `ꦏꦿ` | `r` is the cakra medial; do not render it as `ꦏ꧀ꦫ`. | **Locked** |
| — | `kya` | `ꦏꦾ` | `y` is the pengkal medial; do not render it as `ꦏ꧀ꦪ`. | **Locked** |
| — | `kry` | No automatic `ꦏꦿꦾ` composition | The available data does not establish cakra + pengkal as one valid composition. It shall be treated as unsupported and diagnosed rather than guessed. | **Proposed** |

### 4.1 Context-sensitive phonetic tokens

`ng` and `ny` must not be implemented or conceptualized as a single global `latin -> glyph` mapping.

| Token | Possible semantic roles | Contract implication | Status |
|---|---|---|---|
| `ng` | nglegena `nga`; pasangan `ng`; panyigeg cecak `ng` | Interpret through role and surrounding orthographic context. | **Proposed / context-dependent** |
| `ny` | nglegena `nya`; pasangan `ny` | Interpret through role and surrounding orthographic context. | **Proposed / context-dependent** |

## 5. Reverse transliteration cases (Javanese → Latin)

| Input | Classification | Expected semantic result | Decision | Status |
|---|---|---|---|---|
| `ꦶ` | `INVALID_CONTEXT` | Diagnostic; no standalone `i` output | Wulu is a dependent vowel modifier and has no host. | **Locked provisionally** |
| `ꦏꦶ` | valid | `ki` | Base KA plus wulu replaces the inherent vowel. | **Locked** |
| `ꦏ꧀` | valid | `k` | Pangkon removes KA's inherent vowel. | **Locked** |
| `ꦏ꧀ꦩ` | valid structural cluster | `kma` | Interpret as `k + m`, not `ka + ma`. This is a component-level reading, not a recommendation for natural-language spelling. | **Locked (structural case)** |
| `ꦑ` | valid Murda | `k` | Follow the current ScriptPack data's Latin value. Do not silently substitute a linguistically preferred value such as `ka`. | **Locked to current data** |
| `ꦏ꦳` | valid Rekan construction | `kh` | Recognize the construction as one Rekan phonetic form. | **Locked** |
| `꧇` | known pada, no meaningful Latin mapping | TBD | It must not be silently converted to an empty string, whitespace, or unrelated punctuation. | **Open** |
| `꧋` | known pada, no meaningful Latin mapping | TBD | Same unresolved policy as above. | **Open** |
| `ꧏ` | known pada, no meaningful Latin mapping | TBD | Same unresolved policy as above. | **Open** |

### 5.1 Murda recognition versus canonical generation

Forward canonical generation and reverse recognition deliberately differ:

```text
Latin `ka` -> ꦏ       (canonical nglegena generation)
Javanese ꦑ -> `k`     (recognize valid Murda according to current data)
```

Lossless recognition does not require automatic reconstruction of Murda from plain Latin input.

**Status: Locked.**

## 6. Tokenizer policy

Latin-to-Javanese processing is conceptually split into:

```text
Latin input -> tokenizer -> phonetic tokens -> orthographic composer -> Javanese Unicode
```

The tokenizer must recognize applicable valid token classes before composing glyphs. Indicative priority is:

1. Dedicated phonetic tokens, such as `kh`, `gh`, and `dz`.
2. Supported consonant-medial compositions, such as `kr` and `ky`.
3. Ordinary syllable forms, such as `ka`, `ki`, and `ku`.
4. A single consonant, such as `k`.

### 6.1 Refined longest-valid-token rule

The earlier shorthand “longest match” is refined as follows:

> Select the **longest valid token match within the applicable phonetic/orthographic class**.

String length alone is not sufficient. For example, `kh` wins over `k` because it is a registered Rekan phonetic token, not merely because it contains more characters. A longer candidate that has no valid composition—such as the proposed-invalid `kry` case—must not be accepted or guessed.

**Status: Proposed.**

## 7. Diagnostic philosophy

The contract distinguishes semantic outcomes rather than prescribing an implementation mechanism:

```text
SUCCESS
SUCCESS_WITH_DIAGNOSTICS
INVALID_INPUT
```

Recommended semantic policy:

| Condition | Behavior | Status |
|---|---|---|
| Unknown external character | Preserve; not an error. | **Locked** |
| Known Javanese character in invalid context | Diagnose; do not silently reinterpret. | **Locked provisionally** |
| Unsupported orthographic sequence | Diagnose; do not invent a composed meaning. | **Proposed** |
| Ambiguous input with deterministic context | Resolve and process. | **Proposed** |
| Ambiguous input without deterministic context | Diagnose; do not guess silently. | **Proposed** |

The record intentionally does not lock whether diagnostics are exposed through a result object, exception with partial output, callback, or another API design.

## 8. Partial processing and preservation

### 8.1 Partial processing proposal

An invalid or unsupported segment should not erase unrelated valid segments.

Example, conceptually:

```text
Input:  ka @ kry!
        ka  -> ꦏ
        @   -> @          (preserved unknown)
        kry -> diagnostic (unsupported composition)
        !   -> !          (preserved)
```

Proposed invariant:

> Transliteration shall process independent valid segments whenever possible and shall not discard unrelated valid input solely because another segment is invalid or unsupported.

**Status: Proposed (TR-1C-003).**

### 8.2 Preservation rules

- Preserve unknown external characters unchanged.
- Preserve whitespace according to the Phase 1B contract.
- Do not silently normalize unsupported input into a different orthographic meaning.
- Do not silently drop known input merely because its Latin mapping is empty or unresolved.
- For diagnostic segments, the exact output/recovery carrier remains an API and implementation decision.

## 9. Core interpretation rule

For reverse transliteration, semantic role precedes Latin rendering:

```text
glyph sequence -> semantic role -> Latin output
```

It must not be reduced to a global per-glyph dictionary:

```text
glyph -> Latin
```

This is necessary because the same Latin fragment may denote a base, pasangan, or final consonant function depending on context.

**Status: Locked as a contract principle.**

## 10. Phase 1C status

| Area | Status |
|---|---|
| `k`, `ka`, `ki`, `kh`, `kr`, `kya` | **Locked** |
| `kry` unsupported composition | **Proposed** |
| Standalone dependent vowel `ꦶ` | **Locked provisionally** |
| `ꦏꦶ`, `ꦏ꧀`, `ꦏ꧀ꦩ`, `ꦑ`, `ꦏ꦳` | **Locked** |
| Pada `꧇`, `꧋`, `ꧏ` | **Open** |
| Unknown-character policy | **Locked** |
| Invalid-context policy | **Locked provisionally** |
| Ambiguity and tokenizer policies | **Proposed** |
| Partial processing | **Proposed** |
| Diagnostic API/object model | **Open / explicitly out of scope** |

Phase 1C is **in progress**, not complete.

## 11. Next checkpoint: contextual sequences

Before finalizing the Phase 1C error/diagnostic contract, test contextual parser boundaries and modifier attachment with concrete sequences such as:

```text
ꦏꦶ      ꦏ꧀ꦩ      ꦏꦶꦩ      ꦏ꧀ꦩꦶ
ꦏꦿ      ꦏꦾ      ꦏꦽ      ꦏꦁ
ꦏꦂ      ꦏꦃ
```

The checkpoint question is:

> Does each modifier attach to the intended nearest host, and how are boundaries determined when pasangan, sandhangan, wyanjana, and panyigeg occur in one sequence?

Resolving those contextual sequences will support the eventual AD-TR-01 Transliteration Contract v1.0, Golden Test Corpus, Error/Diagnostic Policy, and a clear Phase 2 implementation boundary.

