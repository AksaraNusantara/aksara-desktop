# AD-TR-01 — Phase 0 Reconnaissance

| Field | Value |
|---|---|
| Status | Locked — evidence gathering complete |
| Date | 2026-08-29 |
| Intended repository location | `docs/decisions/01_AD_TR_01_PHASE_0_RECONNAISSANCE.md` |

## Purpose

Phase 0 mapped the existing repository before any Transliterasi implementation. It is an evidence record, not authorization to change source code or Foundation contracts.

## Findings

`ui/tabs/transliterasi_tab.py` is a legacy component. Its Latin-to-Javanese path imports `data.aksara_jawa.TRANSLITERATION_MAP` and uses replacement-based string processing. Javanese-to-Latin is not implemented.

The repository no longer contains `data/aksara_jawa.py`; current Javanese character data belongs to:

```text
scriptpacks/javanese/assets/characters/
├── nglegena.json
├── sandhangan_swara.json
├── sandhangan_wyanjana.json
├── sandhangan_panyigeg.json
├── pasangan.json
├── murda.json
├── rekan.json
├── swara.json
├── angka.json
└── pada.json
```

`SCRIPTPACK_INTERFACE_SPECIFICATION.md` §17 states that transliteration is writing-system-specific, may be provided by a ScriptPack, and SHALL NOT be implemented by Core Engine. A standardized interface is only a future extension; Foundation v1.0 is frozen.

Core Engine, `BaseScriptPack`, and `JavaneseScriptPack` have no transliteration API. `CentralWorkspace` does not integrate `TransliterasiTab`; it is an orphaned legacy component. No dedicated transliteration tests were found.

## Locked decisions

| ID | Decision | Rationale |
|---|---|---|
| TR-ARCH-001 | Do not revive `TRANSLITERATION_MAP`. | Its source module is gone, and UI-owned replacement conflicts with current architecture. |
| TR-ARCH-002 | Do not place Javanese linguistic rules in Core Engine. | Required by AN-STD-001 §17 and the Foundation boundary. |
| TR-ARCH-003 | Keep UI as presentation boundary, not parser/composer. | Avoids legacy business logic and permits independent tests. |
| TR-ARCH-005 | Use the ScriptPack character repository as canonical data source. | It is the current repository source of truth. |

## Proposed decision

| ID | Decision | Reason |
|---|---|---|
| TR-ARCH-004 | Decide a ScriptPack/application transliteration capability before implementation; do not pre-emptively modify `BaseScriptPack`. | Foundation is frozen and does not standardize this capability. |

## Scope boundary

AD-TR-01 covers contract design, Javanese engine, ScriptPack/application integration, UI integration, tests, and regression validation. It does not authorize redesign of Learning Engine, Quiz, Flashcard, Script Explorer, persistence, marketplace, or other ScriptPacks.

# PERATURAN — Project Decision Traceability

> **Percakapan adalah tempat kita berpikir; Markdown adalah tempat kita menyimpan keputusan.**

Every meaningful project note, draft, correction, contract decision, architecture decision, scope change, workshop result, or material analysis MUST be recorded in a Markdown artifact or an appropriate project log. It MUST NOT live only in chat history.

1. Every contract statement MUST have a status: **Draft**, **Proposed**, **Locked**, or **Superseded**.
2. A correction MUST retain the prior reasoning, state why it changed, and state the current decision.
3. Every architecture change MUST record rationale, affected boundary, and compatibility implications.
4. History MUST NOT be deleted when a decision changes; a later record marks it Superseded.
5. Before an implementation checkpoint, contract, rationale, scope, and validation expectations MUST be recorded.

```text
Architecture → specification → implementation → tests → documentation
```
