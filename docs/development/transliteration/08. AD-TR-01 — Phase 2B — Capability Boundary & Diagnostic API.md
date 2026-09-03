# AD-TR-01 — Phase 2B — Capability Boundary & Diagnostic API

> **Status:** LOCKED  
> **Phase:** AD-TR-01 — Phase 2 — Core Transliteration Implementation  
> **Checkpoint:** 2B — Capability Boundary & Diagnostic API  
> **Decision:** Finalized after Partner Review

---

## 1. Purpose

Phase 2B closes the implementation-critical gaps identified during Phase 2A:

1. Where the transliteration capability lives.
2. What the transliteration API returns when processing succeeds or encounters orthographic issues.

The `ng` / `ny` tokenizer and orthographic-resolution problem is deliberately deferred to Phase 2C.

---

## 2. Capability Boundary

### CAP-001 — Transliteration Is an Optional Capability

Transliteration is an optional capability provided by a ScriptPack.

Not every ScriptPack is required to support transliteration.

**Status: LOCKED**

### CAP-002 — BaseScriptPack Remains Frozen

`BaseScriptPack` is not modified to add a mandatory transliteration method.

Existing ScriptPacks such as:

```text
JavaneseScriptPack
SampleScriptPack
TemplateScriptPack
```

remain valid without implementing transliteration.

**Status: LOCKED**

### CAP-003 — Protocol-Based Capability

The shared capability contract uses Python `typing.Protocol`.

Conceptually:

```python
class TransliterationCapable(Protocol):
    ...
```

This provides structural capability detection without adding another inheritance requirement to `BaseScriptPack`.

**Status: LOCKED**

### CAP-004 — Core Contains Contracts, Not Javanese Rules

The conceptual shared package is:

```text
core/transliteration/
    capability.py
    contracts.py
```

It contains shared contracts/data models such as:

```text
Protocol
Direction
Result
Status
Diagnostic
DiagnosticKind
```

It must not contain Javanese-specific orthographic rules.

**Status: LOCKED**

### CAP-005 — ScriptPack Ownership

Javanese-specific transliteration implementation belongs under the Javanese ScriptPack.

Conceptually:

```text
scriptpacks/
└── javanese/
    └── transliteration/
        ├── tokenizer
        ├── resolver
        ├── composer
        ├── parser
        └── decomposer
```

Exact filenames/classes remain implementation details.

**Status: LOCKED**

### CAP-006 — Application as Coordinator

The Application layer may provide a transliteration coordinator/boundary:

```text
UI
 ↓
Transliteration Coordinator
 ↓
Active ScriptPack
 ↓
Transliteration Capability
```

The coordinator may obtain the active ScriptPack, detect capability, invoke it, and return the result. It must not implement Javanese orthographic rules.

**Status: LOCKED**

### CAP-007 — No Legacy Fallback

The new subsystem must not restore or depend on the legacy:

```python
TRANSLITERATION_MAP
```

If a ScriptPack does not expose transliteration capability, the Application reports that capability as unavailable rather than invoking a second legacy implementation.

**Status: LOCKED**

---

# 3. Diagnostic / Result API

### API-001 — Result Object Is Mandatory

The transliteration operation always returns a structured result:

```python
TransliterationResult(
    output=...,
    status=...,
    diagnostics=...,
)
```

The API does not alternate between `str` and `Result`.

**Status: LOCKED**

### API-002 — Success States

The initial status set is:

```text
SUCCESS
SUCCESS_WITH_DIAGNOSTICS
```

`SUCCESS` means processing completed without diagnostics.

`SUCCESS_WITH_DIAGNOSTICS` means output was produced while one or more orthographic issues were reported.

**Status: LOCKED**

### API-003 — INVALID_INPUT Is Removed

The previously proposed `INVALID_INPUT` status is removed.

The contract instead distinguishes:

```text
UNKNOWN
        → preserve

INVALID_CONTEXT
        → diagnostic

UNSUPPORTED
        → diagnostic

AMBIGUOUS
        → diagnostic
```

A future genuinely distinct failure state requires a contract amendment.

**Status: LOCKED**

---

## 4. Diagnostic Model

### API-004 — Structured Diagnostic

Conceptually:

```python
Diagnostic(
    start=...,
    end=...,
    segment=...,
    kind=...,
    message=...,
)
```

These fields represent the semantic diagnostic contract.

**Status: LOCKED**

### API-005 — Start/End Range

Diagnostics identify an input range with:

```text
start = inclusive
end   = exclusive
```

Indices use Python string indexing based on Unicode code points.

**Status: LOCKED**

### API-006 — Original Input Segment

`segment` is the original substring from the user's input corresponding to the diagnostic range.

It is not a normalized or reconstructed internal token.

Example:

```text
input = "kry"
segment = "kry"
```

**Status: LOCKED**

### API-007 — Diagnostic Kinds

Initial diagnostic kinds:

```text
INVALID_CONTEXT
UNSUPPORTED
AMBIGUOUS
```

**Status: LOCKED**

### API-008 — UNKNOWN Is Not a Diagnostic

Unknown external characters are preserved rather than reported as diagnostics:

```text
UNKNOWN
    ↓
preserve
    ↓
no diagnostic
```

This differs from:

```text
INVALID_CONTEXT
UNSUPPORTED
AMBIGUOUS
    ↓
diagnostic
```

**Status: LOCKED**

### API-009 — Human-Readable Message

Diagnostics contain a human-readable `message`.

The message is not the primary machine-readable contract. Tests should primarily assert:

```text
kind
start
end
segment
```

rather than exact wording.

**Status: LOCKED**

### API-010 — Diagnostic vs Exception

Orthographic problems produce diagnostics.

Programming/API misuse or genuine system failures may raise exceptions.

```text
Orthographic problem
        ↓
Diagnostic

Programming/API misuse
        ↓
Exception
```

**Status: LOCKED**

### API-011 — Immutable Result

Result and diagnostic data should be immutable.

Conceptually:

```python
@dataclass(frozen=True)
```

and:

```python
diagnostics: tuple[Diagnostic, ...]
```

**Status: LOCKED**

### API-012 — Partial Processing

An orthographic problem in one segment does not automatically invalidate unrelated valid segments.

Conceptually:

```text
valid segment
    → process

unknown external character
    → preserve

invalid/ambiguous segment
    → diagnostic
```

The exact recovery strategy remains subject to Phase 2C and implementation details.

**Status: LOCKED AS PRINCIPLE**

---

# 5. API Shape

The conceptual API is:

```python
result = transliterator.transliterate(
    text,
    direction,
)
```

returning:

```text
TransliterationResult
```

The exact placement of the method and internal class names remain open for implementation.

**Status: LOCKED AS CONTRACT SHAPE**

---

# 6. Architecture Summary

```text
                         CORE
                          │
              Transliteration Contracts
                          │
               ┌──────────┴──────────┐
               │                     │
          Capability              Data Models
           Protocol            Result / Diagnostic
               │
               ▼
          APPLICATION
               │
      Transliteration Coordinator
               │
               ▼
        ACTIVE SCRIPTPACK
               │
               ▼
    Javanese Transliteration
               │
       ┌───────┴────────┐
       │                │
    Forward           Reverse
       │                │
   Tokenizer          Scanner
       │                │
   Resolver            Parser
       │                │
   Composer          Decomposer
       │                │
       └───────┬────────┘
               ▼
        Javanese Unicode
```

The ownership boundary is locked; exact internal decomposition is not.

---

# 7. Explicitly Deferred to Phase 2C

The following are deliberately not locked by Phase 2B:

```text
ng / ny token recognition
longest-valid-token implementation
lookahead rules
orthographic role resolution
syllable boundary detection
ambiguous Latin sequence handling
pairing of tokens into orthographic structures
```

The earlier `ng` / `ny` proposal remains input to Phase 2C.

---

# 8. Decision Summary

| Decision | Status |
|---|---|
| Transliteration is an optional capability | LOCKED |
| `BaseScriptPack` remains unchanged | LOCKED |
| Capability uses `Protocol` | LOCKED |
| Core contains shared contracts only | LOCKED |
| Javanese rules belong to Javanese ScriptPack | LOCKED |
| Application may provide coordinator | LOCKED |
| No legacy `TRANSLITERATION_MAP` fallback | LOCKED |
| Result object always returned | LOCKED |
| `SUCCESS` | LOCKED |
| `SUCCESS_WITH_DIAGNOSTICS` | LOCKED |
| `INVALID_INPUT` | REMOVED |
| Diagnostic kinds | LOCKED |
| UNKNOWN → preserve, not diagnostic | LOCKED |
| Diagnostic uses `start/end` | LOCKED |
| Python Unicode-code-point indexing | LOCKED |
| Segment = original input substring | LOCKED |
| Message is human-readable | LOCKED |
| Orthographic issues → diagnostics | LOCKED |
| Programming/API failures → exceptions | LOCKED |
| Result/diagnostics immutable | LOCKED |
| Partial processing principle | LOCKED |
| Exact internal class/file names | OPEN |
| `ng` / `ny` resolution | DEFERRED TO PHASE 2C |

---

# 9. Phase 2B Conclusion

**AD-TR-01 Phase 2B is LOCKED.**

The two major pre-implementation gaps identified after Phase 2A are now resolved at contract level:

```text
Capability Boundary
        ↓
        LOCKED

Diagnostic / Result API
        ↓
        LOCKED
```

The next unresolved implementation-critical problem is:

```text
Latin input
    ↓
Tokenization
    ↓
Orthographic Resolution
```

especially for:

```text
ng
ny
kh
gh
dz
...
```

---

# 10. Next Checkpoint

Proceed to:

> **AD-TR-01 — Phase 2C — Tokenization & Orthographic Resolution**

Primary focus:

```text
Latin
 ↓
Tokenizer
 ↓
Token Stream
 ↓
Orthographic Resolver
 ↓
Composer
```

The Phase 2C workshop must determine behavior before executable tokenizer tests are finalized.

---

## Documentation Trace

```text
01 — Phase 0 Reconnaissance
02 — Phase 1 Draft
03 — Phase 1 Correction / Contract Deep Dive
04 — Phase 1B Orthographic Contract Workshop
05 — Phase 1C Invalid, Ambiguous & Context Cases
06 — Consolidated Transliteration Contract Rules v0.1
07 — Phase 2A Implementation Reconnaissance
08 — Phase 2B Capability Boundary & Diagnostic API
```

> **Project Rule:** Every important implementation finding, decision, correction, and contract amendment must be documented in Markdown. The conversation is the workshop; the Markdown record is the project's durable trace.

---

## Implementation Note (non-normative, does not alter LOCKED status)

`SUCCESS_WITH_DIAGNOSTICS` does not distinguish "mostly valid, one issue" from "entirely diagnostic, nothing usable." Both are the same status; severity is only visible by inspecting `diagnostics` against the input.

This is not a defect in the LOCKED contract — it is a consequence of removing `INVALID_INPUT` (API-003), which is correct per the Partial Processing principle (API-012). It is noted here only so the UI layer (`TransliterasiTab` / coordinator) does not treat `status == SUCCESS_WITH_DIAGNOSTICS` as "mostly succeeded" — it must always render `diagnostics` explicitly rather than inferring severity from `status` alone.

No contract field is proposed or changed by this note.
