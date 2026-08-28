# Quiz Subsystem Contract

**Status:** Approved / Frozen  
**Scope:** Quiz subsystem architecture and responsibility boundaries  
**Contract version:** v3 (visual contract)  
**Last closure:** 2026-08-24

## 1. Purpose

This document records the architectural contract for the Quiz subsystem after the SoC refactor and production review.

It defines responsibility boundaries, ownership of Quiz state and data, the Official QuizTab API boundary, the QuizSession domain boundary, the QuizResult boundary, the Learning Engine and persistence boundary, forbidden responsibility leakage, testing expectations, and deferred decisions.

This is a normative architectural reference, not an implementation listing.

## 2. Contract v3 — Visual Reference

The authoritative visual representation of Quiz Contract v3 is maintained separately:

- `Quiz Diagram v3.vsdx` — editable/master Visio source.
- `Quiz Diagram v3.jpg` — visual reference/export.

Expected location:

```text
docs/architecture/
├── QUIZ_SUBSYSTEM_CONTRACT.md
├── Quiz Diagram v3.vsdx
└── Quiz Diagram v3.jpg
```

The diagram is the visual companion to this document. Markdown defines textual responsibility and boundary rules; the Visio diagram provides the corresponding visual architecture.

## 3. Architectural Principles

The Quiz subsystem follows **Separation of Concerns (SoC)**.

> Each layer owns its responsibility and does not duplicate the responsibility of another layer.

- `QuizTab` is a UI/presentation and orchestration component.
- `QuizSession` owns active Quiz domain state.
- `QuizResult` represents the completed Quiz result.
- `LearningService` owns the transition from an activity result into learning history.
- Repository/storage layers own persistence and serialization concerns.

## 4. Responsibility Boundaries

### 4.1 QuizTab

`QuizTab` owns presentation and UI orchestration.

It may own:

- selected answer;
- current question presentation;
- feedback presentation;
- UI state;
- result presentation;
- question-navigation presentation;
- interaction with Quiz UI controls;
- orchestration of the Quiz flow;
- passing completed `QuizResult` data to `LearningService`.

It does **not** own:

- correct-answer statistics;
- incorrect-answer statistics;
- answer history;
- Quiz domain lifecycle;
- JSON serialization;
- storage;
- direct persistence of learning history.

### 4.2 QuizSession

`QuizSession` owns the domain state of one Quiz activity.

It owns:

- Quiz lifecycle;
- answer processing;
- answer records;
- correct-answer statistics;
- incorrect-answer statistics;
- answered-question progress;
- difficulty configuration;
- completion;
- cancellation;
- creation of the completed `QuizResult`.

`QuizSession` must not know about Qt, widgets, UI signals, `QuizTab`, persistence implementation, or JSON storage.

### 4.3 QuizResult

`QuizResult` represents the completed result of a Quiz.

It is a completed-result snapshot, not a mutable Quiz session.

The current result contract contains:

- `total_questions`;
- `correct_answers`;
- `incorrect_answers`;
- `difficulty_level`.

The result is immutable and suitable for transfer to the Learning Engine.

### 4.4 LearningService

`LearningService` is the application boundary for recording a completed Quiz as learning history.

The Quiz UI/domain must not construct or persist `StudySession` directly.

```text
QuizSession
    │
    │ build_result()
    ▼
QuizResult
    │
    │ record_quiz_result(...)
    ▼
LearningService
    │
    ▼
StudySession
```

### 4.5 Repository / Storage

Repository and storage layers own persistence concerns, including saving/loading learning history, serialization/deserialization, conversion to storage-compatible data, storage keys, and storage mechanics.

Quiz UI and domain code must not depend on JSON representation or file-storage mechanics.

## 5. Official QuizTab API Boundary

The Official QuizTab API is the UI-facing contract.

UI-facing properties include presentation state such as:

- `is_quiz_active`;
- `is_result_visible`;
- `difficulty_enabled`;
- `start_enabled`;
- `cancel_enabled`;
- `check_enabled`;
- `feedback_visible`;
- `feedback_is_correct`;
- `feedback_text`;
- `correct_answer_text`;
- `next_enabled`;
- `selected_answer`;
- `progress_text`;
- `accuracy_text`.

These properties exist to support UI consumers and tests. Their existence does not transfer ownership of domain state to `QuizTab`.

In particular, public UI compatibility must not reintroduce domain counters or duplicate QuizSession state into `QuizTab`.

## 6. Quiz Lifecycle

The domain lifecycle is owned by `QuizSession`.

```text
READY
  │
  │ start
  ▼
ACTIVE
  │
  ├── answer ──► ACTIVE
  │
  ├── final answer ──► COMPLETED
  │
  └── cancel ──► CANCELLED
```

`QuizTab` presents and orchestrates these states but does not replace the domain lifecycle owned by `QuizSession`.

UI state such as feedback visibility or result visibility is presentation state and is not automatically equivalent to domain state.

## 7. Statistics Ownership

Statistics are owned by `QuizSession` while the Quiz is active.

The UI must not maintain duplicate mutable counters such as:

```text
_correct_count
_incorrect_count
```

The completed `QuizResult` contains the final statistics required by the Learning Engine.

```text
QuizSession / QuizResult
        │
        ▼
     statistics
        │
        ▼
      QuizTab
        │
        ▼
        UI
```

There must be one authoritative source for domain statistics.

## 8. Answer and Feedback Boundary

`QuizSession.answer(...)` is responsible for domain answer processing and returns whether the submitted answer is correct.

`QuizTab` uses that outcome to present feedback.

The UI may access question data required by its current presentation contract, including the correct answer when required by the existing feedback behavior.

A future change to introduce a dedicated answer/feedback DTO must be treated as a contract change, not as an opportunistic refactor.

## 9. Completion and Persistence

```text
QuizSession
    │
    │ completed
    ▼
QuizResult
    │
    ▼
LearningService
    │
    ▼
StudySession
    │
    ▼
Repository
    │
    ▼
Storage
```

A cancelled Quiz does not become learning history.

A completed Quiz produces one learning result and one corresponding learning-history record.

The UI does not perform persistence directly.

## 10. Forbidden Responsibility Leakage

The following patterns are prohibited unless the contract is explicitly changed:

```text
QuizTab
  ✗ calculating correct/incorrect domain statistics
  ✗ maintaining duplicate QuizSession counters
  ✗ persisting StudySession directly
  ✗ performing JSON serialization
  ✗ owning QuizSession lifecycle transitions internally

QuizSession
  ✗ importing/using Qt UI concerns
  ✗ manipulating widgets
  ✗ emitting UI presentation signals
  ✗ writing learning-history storage directly
  ✗ knowing JSON storage format

QuizResult
  ✗ becoming a mutable QuizSession
  ✗ acquiring UI responsibilities
  ✗ acquiring persistence responsibilities
```

## 11. Testing Contract

The Quiz subsystem is regression-green at the current contract boundary:

```text
QuizSession                         21 PASS
QuizTab                             51 PASS
QuizTab Learning Integration         4 PASS
────────────────────────────────────────────
TOTAL                               76 PASS
```

The test suite is part of the executable contract.

A future change to a responsibility boundary, Official API, lifecycle rule, or persistence behavior must update affected tests as part of the same change.

Passing tests alone do not authorize a contract change.

## 12. Production Review Status

The completed production review covered:

- `QuizTab`;
- `QuizSession`;
- `QuizResult`;
- LearningService integration;
- StudySession/repository/storage boundary.

Final status:

```text
QuizTab
  APPROVED — no mandatory production refactor

QuizSession
  APPROVED — no mandatory production refactor

QuizResult / Learning boundary
  APPROVED — no mandatory production refactor
```

The subsystem is:

> **DESIGN-COMPLETE + TEST-COMPLETE + PRODUCTION-REVIEW-APPROVED**

The Quiz subsystem is frozen for the current scope.

## 13. Deferred Decisions

### 13.1 Correct-answer presentation boundary

The current implementation allows `QuizTab` to use question data required to display the correct answer in feedback.

A future dedicated answer/feedback result object may be considered if the Contract explicitly requires a stricter boundary.

### 13.2 QuizAnswer as a broader domain model

Current answer records remain an internal part of the QuizSession domain.

They may become a broader learning/analytics contract in a future version, but this is outside the current scope.

### 13.3 Serialization policy

Enum/domain-to-JSON conversion remains a repository/storage concern.

It must not be moved into `QuizResult` merely for convenience.

## 14. Change Policy

Once the Quiz subsystem is frozen, changes must follow:

```text
Requirement
    ↓
Contract Change
    ↓
Impact Mapping
    ↓
Affected Tests
    ↓
Production Change
    ↓
Regression
    ↓
Production Review
    ↓
Contract Closure
```

Do not begin by modifying `QuizTab` or `QuizSession` when a change affects their responsibility boundary. The contract must be evaluated first.

## 15. Relationship to Future Subsystems

The Quiz subsystem establishes the project pattern for future feature development, especially `TransliterationTab`:

```text
Contract
    ↓
Responsibility Map
    ↓
State Machine
    ↓
Official API
    ↓
Impact Mapping
    ↓
Unit Tests
    ↓
Production Code
    ↓
Integration
    ↓
Production Review
    ↓
Freeze
```

This sequence is intended to reduce accidental coupling, duplicated state, and iterative refactoring caused by unclear ownership.

## 16. Closure Statement

The Quiz subsystem has completed its current architectural cycle.

The contract, implementation, tests, integration, and production review are considered aligned for the current release scope.

The next changes to Quiz must be driven by an explicit requirement or contract change.

**Quiz subsystem: FROZEN.**
