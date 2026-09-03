# AD-TR-01 — Phase 2A — Implementation Reconnaissance

> **Status:** Completed — Reconnaissance only  
> **Phase:** AD-TR-01 — Phase 2 — Core Transliteration Implementation  
> **Checkpoint:** 2A — Implementation Reconnaissance  
> **Rule:** No production implementation or architectural refactor is performed in this checkpoint.

---

## 1. Purpose

Phase 2A establishes the implementation baseline before coding.

The repository snapshot is treated as the source of truth for:

- existing Core Engine APIs;
- ScriptPack implementation;
- Javanese character datasets;
- legacy `TransliterasiTab`;
- application/UI wiring;
- existing tests;
- architecture and standards documentation.

The consolidated contract in:

```text
06_AD_TR_01_TRANSLITERATION_CONTRACT_RULES_v0_1.md
```

is the behavioral baseline.

---

# 2. Repository Findings

## 2.1 Legacy TransliterasiTab

Existing file:

```text
ui/tabs/transliterasi_tab.py
```

Current implementation is a legacy UI-bound prototype.

Important findings:

- imports `TRANSLITERATION_MAP` from `data.aksara_jawa`;
- performs direct string replacement;
- lowercases and strips input;
- splits input with `str.split()`;
- iterates over a global translation map;
- implements no contextual orthographic parsing;
- reverse direction is only a placeholder message.

Current forward algorithm is therefore **not suitable for AD-TR-01**.

The contract requires this legacy mapping approach to be retired rather than extended.

The repository snapshot does not contain:

```text
data/aksara_jawa.py
```

so the legacy `TRANSLITERATION_MAP` is not part of the current ScriptPack-based architecture.

---

# 3. Core Engine

Existing file:

```text
core/engine.py
```

Current Core Engine responsibilities include:

- ScriptPack discovery;
- validation;
- loading;
- registry;
- activation;
- access to active ScriptPack;
- access to active characters;
- dataset selection;
- asset/path access.

Relevant existing API:

```python
engine.get_active_scriptpack()
engine.get_active_characters()
engine.get_available_datasets()
engine.set_current_dataset(...)
engine.get_current_dataset()
```

The Core Engine does **not** currently expose a transliteration API.

This is consistent with the existing ScriptPack specification:

> Transliteration is writing-system specific and remains the responsibility of the ScriptPack.

Therefore Phase 2 should **not** put Javanese transliteration rules into `core.engine`.

---

# 4. BaseScriptPack

Existing file:

```text
core/scriptpack.py
```

`BaseScriptPack` currently provides:

- character access;
- dataset access;
- metadata;
- asset paths;
- generated paths;
- ScriptPack lifecycle-related interface.

There is currently **no standardized transliteration method/interface** in `BaseScriptPack`.

The existing standard explicitly states that future versions may define a standardized transliteration interface.

Therefore the current implementation must avoid inventing an unnecessary Core Engine abstraction merely to satisfy the UI.

A ScriptPack-specific capability is the likely implementation boundary.

---

# 5. Javanese ScriptPack

Existing file:

```text
scriptpacks/javanese/script.py
```

`JavaneseScriptPack` currently:

- inherits `BaseScriptPack`;
- loads character JSON datasets;
- exposes available datasets;
- switches the current dataset;
- registers fonts.

Available datasets:

```text
nglegena
sandhangan_swara
sandhangan_panyigeg
sandhangan_wyanjana
pasangan
murda
rekan
swara
angka
pada
```

This is highly relevant to AD-TR-01 because the required transliteration vocabulary already exists in the ScriptPack.

---

# 6. Javanese Character Data

Directory:

```text
scriptpacks/javanese/assets/characters/
```

Contains:

```text
angka.json
murda.json
nglegena.json
pada.json
pasangan.json
rekan.json
sandhangan_panyigeg.json
sandhangan_swara.json
sandhangan_wyanjana.json
swara.json
```

Current dataset sizes:

```text
nglegena                20
sandhangan_swara         5
sandhangan_panyigeg      4
sandhangan_wyanjana      3
pasangan                20
murda                    8
rekan                    6
swara                     5
angka                    10
pada                      5
```

The character model uses:

```text
id
glyph
latin
unicode
description
```

where applicable.

This confirms the Phase 1 principle:

> Character Repository provides vocabulary; Transliteration Engine provides grammar, context, composition, and decomposition.

---

# 7. Important Data Semantics

The reconnaissance confirms that `latin` is **not globally unique**.

Examples:

```text
nglegena:
nga → ꦔ

pasangan:
ng → pasangan nga

panyigeg:
ng → ꦁ
```

Likewise:

```text
nglegena:
nya

pasangan:
ny
```

Other examples:

```text
murda:
k → ꦑ

nglegena:
ka → ꦏ
```

Therefore a simple:

```python
latin_to_glyph = {...}
```

cannot be the primary transliteration algorithm.

Context and orthographic role are required.

---

# 8. Application Layer

Existing:

```text
application/application.py
```

The Application owns the shared `CoreEngine`.

The current startup sequence:

```text
Application
    ↓
CoreEngine.initialize()
    ↓
ScriptPack discovery/loading
    ↓
ScriptPack asset registration
```

This is already suitable for a transliteration feature because the active ScriptPack is available at runtime.

No persistence dependency is required for transliteration.

---

# 9. UI Layer

Existing:

```text
ui/central_workspace.py
ui/main_window.py
ui/tabs/transliterasi_tab.py
```

`CentralWorkspace` currently documents Transliteration as a hosted feature but does not instantiate `TransliterasiTab`.

Current workspace tabs include:

```text
Home
Script Explorer
Flashcard
Quiz
```

There is currently no active Transliteration tab integration in `CentralWorkspace`.

Therefore UI integration should be a later Phase 2 step, after core transliteration behavior is stable.

The legacy `TransliterasiTab` should not be used as the architectural source of truth.

---

# 10. Existing Tests

Repository scan found:

```text
no dedicated transliteration test module
```

No current automated test was found for:

```text
TransliterasiTab
Latin → Javanese
Javanese → Latin
```

This means Phase 2 must establish the transliteration test foundation before substantial implementation.

The existing project uses `unittest`.

The global test runner is:

```text
run_tests.bat
```

and discovers:

```text
tests/test_*.py
```

---

# 11. Existing Architecture Constraints

The repository architecture confirms:

```text
Core Engine
    ↓
ScriptPack
```

with writing-system-specific linguistic behavior remaining outside the Core Engine.

The project workflow also explicitly follows:

```text
Specification Before Implementation
Documentation as Code
One Source of Truth
Validation Before Release
```

Therefore AD-TR-01 implementation should preserve:

```text
UI
 ↓
Application / feature boundary
 ↓
ScriptPack-specific transliteration capability
 ↓
ScriptPack data
```

rather than placing Javanese rules into the Core Engine.

---

# 12. Recommended Implementation Boundary

Based on the current repository, the preferred direction is:

```text
JavaneseScriptPack
        │
        └── Javanese transliteration capability
                    │
                    └── transliteration engine/module
```

The engine should consume ScriptPack-owned character data and ScriptPack-specific rules.

Possible conceptual separation:

```text
Javanese Transliteration
│
├── tokenizer
├── orthographic composer
├── orthographic parser
├── Latin → Javanese
└── Javanese → Latin
```

The exact module/class names are intentionally **not locked yet**.

We should choose them after the first test/API design checkpoint.

---

# 13. Legacy Code Decision

The existing:

```text
ui/tabs/transliterasi_tab.py
```

must be treated as:

```text
legacy presentation prototype
```

not as the foundation of the new implementation.

The following legacy dependency must not be restored:

```python
from data.aksara_jawa import TRANSLITERATION_MAP
```

The old `str.replace()` approach also cannot satisfy:

- contextual composition;
- pasangan;
- sandhangan;
- pangkon;
- Rekan;
- Murda recognition;
- invalid-context diagnostics;
- deterministic tokenization;
- canonical generation.

---

# 14. Risks Identified

## Risk 1 — Premature Core Engine API

Adding a generic transliteration API to `CoreEngine` now could violate the existing architecture because the standard explicitly leaves transliteration responsibility with ScriptPacks.

**Mitigation:** keep transliteration writing-system-specific unless a real cross-ScriptPack abstraction becomes necessary.

---

## Risk 2 — Global Latin Mapping

Using:

```python
latin_to_glyph
```

as the primary engine will fail on contextual forms such as:

```text
ng
ny
k
```

and will mishandle modifiers.

**Mitigation:** tokenization + orthographic context.

---

## Risk 3 — UI-First Implementation

Extending `TransliterasiTab` before the core behavior is tested would repeat the legacy design pattern.

**Mitigation:** tests and core capability first; UI integration later.

---

## Risk 4 — Silent Data Correction

Some current ScriptPack values may look linguistically unusual, especially Murda and punctuation entries with empty `latin`.

**Mitigation:** follow current ScriptPack data unless an explicit contract amendment is made.

---

## Risk 5 — Overengineering

The existing ScriptPack interface does not yet define a standardized transliteration API.

Creating a large framework for future scripts before Javanese transliteration works would expand scope unnecessarily.

**Mitigation:** implement the smallest architecture that satisfies the current contract and preserves future extensibility.

---

# 15. Recommended Phase 2 Scope

Phase 2 should proceed incrementally:

```text
2A — Implementation Reconnaissance       ✅
2B — Core Transliteration Test Contract  ⏭
2C — Transliteration Core API Design     ⏭
2D — Latin → Javanese                    ⏭
2E — Javanese → Latin                    ⏭
2F — ScriptPack Integration              ⏭
2G — TransliterasiTab Integration        ⏭
2H — Integration / Regression Tests      ⏭
2I — Manual Smoke Test                   ⏭
```

The exact numbering may be adjusted if implementation evidence requires it.

---

# 16. Phase 2A Conclusion

The reconnaissance establishes several important facts:

1. There is **no usable transliteration engine** in the current architecture.
2. The legacy `TransliterasiTab` is only a prototype and must not be extended as the core solution.
3. The legacy `TRANSLITERATION_MAP` is obsolete for the current architecture.
4. Javanese ScriptPack already contains the necessary character datasets.
5. Core Engine currently has no transliteration API, intentionally.
6. There are no dedicated transliteration tests.
7. Transliteration rules should remain ScriptPack-specific.
8. Context-aware parsing/composition is mandatory.
9. UI integration should happen only after core behavior is tested.
10. The next checkpoint should establish tests and the smallest viable core transliteration API.

---

# 17. Phase 2A Decision

### DECISION

Proceed to:

> **AD-TR-01 — Phase 2B — Core Transliteration Test Contract**

Before implementing the engine, establish the first executable contract tests from:

```text
06_AD_TR_01_TRANSLITERATION_CONTRACT_RULES_v0_1.md
```

The first implementation target should therefore be:

```text
Contract
   ↓
Tests
   ↓
Minimal API
   ↓
Implementation
```

No changes to Learning Engine or Quiz are required.

No major Core Engine refactor is justified by the current reconnaissance.

---

# 18. Documentation Trace

This document records the first implementation reconnaissance for Phase 2.

The historical sequence is now:

```text
01 — Phase 0 Reconnaissance
02 — Phase 1 Draft
03 — Phase 1 Correction / Contract Deep Dive
04 — Phase 1B Orthographic Contract Workshop
05 — Phase 1C Invalid, Ambiguous & Context Cases
06 — Consolidated Transliteration Contract Rules v0.1
07 — Phase 2A Implementation Reconnaissance
```

Future Phase 2 decisions must continue the numbered Markdown decision-record sequence.

> **Project Rule:** Important implementation findings, decisions, corrections, and contract amendments must be documented rather than left only in conversation.
