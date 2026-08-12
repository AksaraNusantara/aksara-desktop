# ADR-0002

# Learner Ownership of Learning Sessions

---

## Document Information

| Item              | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| ADR               | 0002                                                                               |
| Title             | Learner Ownership of Learning Sessions                                             |
| Status            | Accepted                                                                           |
| Author            | Aksara Nusantara Project                                                           |
| Date              | 2026-08-10                                                                         |
| Supersedes        | None                                                                               |
| Superseded By     | None                                                                               |
| Related Documents | LEARNING_ENGINE_ARCHITECTURE.md, APPLICATION_ARCHITECTURE.md, PROJECT_BLUEPRINT.md |

---

# 1. Introduction

This Architecture Decision Record (ADR) defines how learner ownership is represented within the Learning Engine.

The current Learning Engine already accepts a `learner_id` when processing learning activities and stores learner-specific `LearningProfile` data.

However, `StudySession` does not currently contain learner ownership information.

As a result, persisted learning activity history is not intrinsically associated with the learner who generated the activity.

This decision establishes explicit learner ownership for every `StudySession` and defines the corresponding Repository and persistence boundaries.

This ADR serves as the authoritative source for the learner ownership decision. Future revisions to the Learning Engine Architecture SHALL remain consistent with this decision unless this ADR is explicitly superseded.

---

# 2. Context

The Learning Engine currently defines `StudySession` as the primary data and authoritative source for learning activity history.

`LearningProfile` represents aggregated learning state for a learner and is derived from `StudySession` records.

The current architecture therefore conceptually represents the relationship as:

```text
Learning Profile
       │
       ▼
Study Sessions
```

The current implementation also provides learner-specific profile persistence through `learner_id`.

However, persisted `StudySession` records are currently stored as a shared collection without explicit learner ownership.

This creates an architectural limitation when a single local application installation is used by multiple learners.

For example:

```text
Learner A
    Quiz → StudySession 1

Learner B
    Quiz → StudySession 2
```

The current `StudySession` model does not intrinsically identify which learner owns either session.

This prevents the Learning Engine from providing a reliable learner-scoped learning history.

The limitation becomes particularly important when the application introduces a History feature or supports multiple learners using the same local installation.

---

# 3. Problem Statement

The current Learning Engine has an inconsistency between learner-scoped aggregate data and learning activity history.

`LearningProfile` is explicitly associated with a learner through `learner_id`.

`StudySession` is not.

This creates an implicit ownership relationship that cannot be reliably reconstructed from the session itself.

The following conditions must therefore be addressed:

## 3.1 Explicit Ownership

Every persisted learning activity must identify the learner who generated it.

## 3.2 Learner Isolation

Learning history belonging to one learner must not be presented as belonging to another learner.

## 3.3 Repository Boundary

Learner-specific filtering must remain within the Learning Repository rather than being implemented by User Interface components.

## 3.4 Persistence Integrity

Learner ownership must survive serialization and deserialization.

## 3.5 Architectural Consistency

The solution must preserve the existing principles that:

* `StudySession` is Primary Data;
* `LearningProfile` is Derived Data;
* `Learning Repository` is the persistence boundary;
* `Learning Services` coordinate business processing;
* User Interface does not access Persistent Storage directly.

---

# 4. Decision

The Learning Engine SHALL introduce explicit learner ownership for every `StudySession`.

A `StudySession` SHALL contain a `learner_id` identifying the learner who owns the learning activity.

The conceptual model SHALL therefore become:

```text
StudySession
├── session_id
├── learner_id
├── timestamp
├── activity_type
└── payload
```

---

## 4.1 StudySession Ownership

Every `StudySession` SHALL belong to exactly one learner.

`learner_id` SHALL be a required part of the `StudySession` domain model.

An empty learner identifier SHALL NOT be considered valid.

A `StudySession` SHALL NOT be shared between learners.

---

## 4.2 Learning Profile Relationship

`LearningProfile` SHALL remain a learner-scoped derived aggregate.

The conceptual relationship SHALL become:

```text
                  Learner
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   Learning Profile       Study Sessions
   (Derived Data)         (Primary Data)
```

`StudySession` remains the authoritative source for learning activity history.

`LearningProfile` remains derived data that can be reconstructed from the learner's StudySession records.

---

## 4.3 Learning Service Responsibility

`LearningService` SHALL propagate the learner identity received from a learning operation into the resulting `StudySession`.

For a completed Quiz:

```text
learner_id
    │
    ▼
LearningService
    │
    ▼
StudySession
    │
    ├── learner_id
    └── QuizResult
```

A completed learning activity SHALL therefore produce a StudySession owned by the learner who performed the activity.

---

## 4.4 Learning Repository Contract

The Learning Repository SHALL provide learner-scoped retrieval of StudySession records.

The conceptual Repository contract SHALL support:

```text
save_session(session)
load_sessions(learner_id)
```

The Repository SHALL be responsible for determining which persisted StudySession records belong to the requested learner.

User Interface components SHALL NOT load all learning sessions and perform learner filtering themselves.

---

## 4.5 Storage Contract

Persistent storage SHALL preserve the learner ownership of every StudySession.

The serialized representation of a StudySession SHALL therefore contain:

```text
session_id
learner_id
timestamp
activity_type
payload
```

The storage technology and serialization format remain implementation concerns and are not otherwise constrained by this decision.

---

## 4.6 Multi-Learner Isolation

The Learning Engine SHALL support multiple learners within the same application installation.

For example:

```text
Learner A
├── StudySession A1
└── StudySession A2

Learner B
├── StudySession B1
└── StudySession B2
```

Retrieving the learning history of Learner A SHALL NOT return sessions owned by Learner B.

The same isolation rule SHALL apply in the opposite direction.

---

## 4.7 Active Learner Boundary

Learner selection SHALL remain outside the QuizTab and HistoryTab domain responsibilities.

The Application Layer SHALL provide the concept of an active learner.

Application components MAY consume the active learner context through the Application Layer.

The Learning Engine SHALL receive the resulting `learner_id` as explicit input rather than determining learner identity itself.

Conceptually:

```text
Application Layer
       │
       │ Active Learner
       ▼
Learning Engine
       │
       ▼
Learner-owned StudySession
```

The Learning Engine SHALL NOT own User Interface logic for selecting or switching learners.

---

# 5. Rationale

The decision follows the principle that authoritative data should contain the information necessary to establish its own ownership and identity.

Because `StudySession` is the authoritative source of learning activity history, learner ownership must be represented directly within the session.

This avoids implicit relationships between profiles and sessions and prevents higher layers from having to reconstruct ownership.

The decision also preserves architectural separation.

The Application Layer determines the active learner.

The Learning Engine processes learner-specific learning activity.

The Repository enforces persistence boundaries.

The Storage layer persists the resulting data.

---

## 5.1 Explicit Domain Ownership

Explicit ownership makes the domain model self-describing.

A StudySession can independently answer:

```text
Who performed this activity?
```

without depending on external profile state.

---

## 5.2 Multi-Learner Support

The design supports multiple learners sharing one application installation without requiring separate storage technologies or separate application instances.

A single persistent session collection may contain records belonging to multiple learners as long as each record contains its owner.

---

## 5.3 Repository-Level Filtering

Learner filtering belongs to the Repository because learner-specific retrieval is a persistence concern.

This prevents User Interface components from becoming coupled to storage structure.

---

## 5.4 Future History Features

The decision provides a stable foundation for future History features.

History can request:

```text
load_sessions(active_learner_id)
```

without needing to know how learning records are physically stored.

This allows History to remain a presentation feature rather than becoming part of QuizTab or the persistence implementation.

---

# 6. Alternatives Considered

## 6.1 Store learner ownership only in LearningProfile

Rejected.

This would leave StudySession ownership implicit and would require external relationships to determine which learner owns an activity.

Because StudySession is authoritative history, this would weaken the domain model.

---

## 6.2 Store separate session files for each learner

Rejected.

For example:

```text
sessions_budi.json
sessions_siti.json
```

This unnecessarily couples learner identity to the physical storage structure.

The Repository abstraction should allow the storage implementation to change without changing the domain model.

---

## 6.3 Load all sessions and filter in the User Interface

Rejected.

This violates persistence boundaries and exposes the UI to data organization concerns.

Filtering SHALL occur through the Learning Repository.

---

## 6.4 Introduce a separate History database

Rejected.

History is already defined as a presentation view of StudySession data.

Creating another authoritative history store would duplicate Primary Data and introduce synchronization problems.

---

# 7. Backward Compatibility

Existing StudySession records created before learner ownership was introduced may not contain `learner_id`.

Such records SHALL NOT be silently assigned to an arbitrary learner.

The system SHALL NOT infer ownership from profile order, timestamps, session identifiers, or other indirect information.

Legacy records without reliable learner ownership SHALL be treated as unassigned legacy data until an explicit migration strategy is defined.

A future migration mechanism MAY associate legacy records with a learner when sufficient authoritative information is available.

No automatic ownership inference SHALL be introduced.

---

# 8. Versioning Impact

This decision changes the Learning Engine Architecture Contract because it changes the structure and ownership relationship of the StudySession domain model.

Under the Learning Engine versioning rules, this constitutes a Breaking Change.

The Architecture Version SHALL therefore advance when this decision is incorporated into the Architecture Contract.

The Storage Version SHALL also advance when the persisted StudySession representation changes.

Reference Implementation Version MAY advance independently according to the implementation release process.

The exact version numbers SHALL be recorded in the corresponding architecture and implementation documentation when the contract update is accepted.

---

# 9. Consequences

## 9.1 Positive Consequences

The decision provides:

* explicit learner ownership;
* reliable multi-learner isolation;
* learner-scoped learning history;
* a clear Repository query boundary;
* a stable foundation for History UI;
* improved domain integrity;
* support for multiple learners within one local installation;
* future compatibility with other learning activities.

---

## 9.2 Negative Consequences

The decision requires changes to:

* `StudySession`;
* `LearningRepository`;
* `StorageLearningRepository`;
* `LearningService`;
* serialization and deserialization;
* existing tests;
* Quiz-to-Learning integration tests;
* Learning Engine Architecture documentation;
* storage compatibility handling.

Existing persisted StudySession data may require migration or explicit legacy handling.

---

# 10. Implementation Requirements

The Reference Implementation SHALL implement the following changes after this ADR is accepted:

1. Add required `learner_id` to `StudySession`.
2. Validate `learner_id`.
3. Update `LearningService` to populate `learner_id`.
4. Update `LearningRepository` to support learner-scoped session retrieval.
5. Update storage serialization and deserialization.
6. Add multi-learner isolation tests.
7. Update Quiz integration tests.
8. Update Learning Engine regression tests.
9. Update the Learning Engine Architecture Contract.
10. Update traceability documentation.

The implementation SHALL preserve existing behavior for:

* completed Quiz persistence;
* cancelled Quiz non-persistence;
* QuizResult integrity;
* LearningProfile aggregation;
* Repository storage abstraction.

---

# 11. Decision Status

This ADR is **Accepted**.

The corresponding Learning Engine Architecture Contract has been updated through
Architecture Decision **AD-LE-014**.

The accepted decision establishes explicit learner ownership for every
`StudySession` through the required `learner_id` attribute, together with
learner-scoped retrieval through the Learning Repository.

The implementation has passed the required Learning Engine regression tests.
The remaining full-suite failures are unrelated Audio test failures and do not
affect the learner ownership decision.

---

# 12. Related Architecture Decision

This decision introduces the next available Learning Engine Architecture Decision identifier:

```text
AD-LE-014
```

AD-LE-010 is already assigned to the existing Domain Model separation decision and SHALL NOT be reused.
