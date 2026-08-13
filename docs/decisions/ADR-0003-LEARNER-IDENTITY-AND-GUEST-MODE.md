# ADR-0003

## Learner Identity and Guest Mode

| Field          | Value |
|----------------|-------|
| ADR            | 0003 |
| Title          | Learner Identity and Guest Mode |
| Status         | Accepted |
| Date           | 2026-08-13 |
| Decision Scope | Learning Engine / Learner Identity |
| Supersedes     | None |
| Related ADR    | ADR-0002 — Learner Ownership of Learning Sessions |

---

# 1. Context

The Learning Engine requires a stable identity for the learner performing
learning activities.

ADR-0002 established explicit learner ownership for every `StudySession`.
A completed learning activity therefore belongs to exactly one learner.

However, the Learning Engine does not yet define the domain representation
of the learner itself.

The application must distinguish between a learner who provides a personal
display name and a learner who chooses to continue as a Guest.

This decision defines the learner identity model, Guest semantics,
persistence boundary, and relationship between learner identity and the
existing Learning Engine domain models.

This ADR is the authoritative source for learner identity semantics.
Future revisions to the Learning Engine Architecture Contract SHALL remain
consistent with this decision unless this ADR is explicitly superseded.

---

# 2. Problem Statement

Without an explicit learner identity model, learner identity would be
distributed across UI state or implicit assumptions.

This would create several problems:

1. `StudySession` ownership could not be traced to a formal learner entity.
2. `LearningProfile` would contain an identifier without a corresponding
   identity domain model.
3. Guest usage could require special handling such as `None` or
   `"anonymous"`.
4. The application could accidentally treat Guest as an absence of identity.
5. Future learner management features would have no defined persistence
   boundary.
6. The Quiz UI could become responsible for determining learner identity.

The Learning Engine therefore requires an explicit and stable identity
concept.

---

# 3. Existing Architecture

ADR-0002 established the following ownership relationship:

```text
Learner
   │
   │ learner_id
   ├──────────────────────┐
   ▼                      ▼
StudySession         LearningProfile
   │
   └── authoritative     └── derived aggregate
       learning history
```

`StudySession` is the authoritative source of learning activity history.

`LearningProfile` represents aggregated learning state associated with a
learner.

Both models already use `learner_id`.

The missing domain concept is therefore:

```text
LearnerIdentity
```

---

# 4. Decision

The Learning Engine SHALL introduce `LearnerIdentity` as the domain model
representing one learner.

A `LearnerIdentity` SHALL contain:

```text
LearnerIdentity
├── learner_id
├── display_name
└── is_guest
```

## 4.1 Stable Learner Identity

`learner_id` SHALL be the stable identifier of a learner.

The identifier SHALL be required, non-empty, unique within the learner
identity store, independent of the learner's display name, and suitable for
referencing the learner from other Learning Engine models.

Changing `display_name` SHALL NOT change `learner_id`.

## 4.2 Display Name

`display_name` SHALL represent the user-facing name of the learner.

For a named learner, `display_name` SHALL be non-empty.

The display name is presentation-oriented identity information and SHALL
NOT be used as the stable identifier.

```text
display_name ≠ learner_id
```

## 4.3 Guest Mode

Guest mode SHALL represent a valid learner identity.

Guest SHALL NOT be represented as `None`, `"anonymous"`, or any other
absence-of-identity state.

A Guest SHALL have a valid `learner_id`.

Canonical Guest representation:

```text
LearnerIdentity
├── learner_id   = generated stable identifier
├── display_name = "Guest"
└── is_guest     = True
```

Named learner representation:

```text
LearnerIdentity
├── learner_id   = generated stable identifier
├── display_name = user-provided name
└── is_guest     = False
```

Guest is therefore a normal learner from the perspective of the Learning
Engine.

---

# 5. Learner Identity Invariants

Every valid `LearnerIdentity` SHALL satisfy:

1. `learner_id` MUST NOT be empty.
2. `display_name` MUST NOT be empty.
3. `learner_id` MUST remain stable after creation.
4. `display_name` MAY change without changing `learner_id`.
5. Guest MUST have a valid `learner_id`.
6. Guest MUST use `"Guest"` as its default display name.
7. `is_guest=True` identifies Guest mode.
8. `is_guest=False` identifies a named learner.
9. A learner identity SHALL represent exactly one learner.

---

# 6. Immutability

`LearnerIdentity` SHALL follow the immutability convention established by
the Learning Engine domain models.

The domain model SHALL therefore be immutable after creation.

Changes to learner information SHALL be represented by creating a new
valid state rather than mutating an existing domain object in place.

This preserves the same domain-model convention used by `LearningProfile`,
`QuizResult`, and `StudySession`.

---

# 7. Relationship with StudySession

`StudySession` SHALL NOT contain a `LearnerIdentity` object.

Instead, `StudySession` SHALL continue to contain only:

```text
learner_id
```

Relationship:

```text
LearnerIdentity
      │
      │ learner_id
      ▼
StudySession
```

This preserves the decision established by ADR-0002.

---

# 8. Relationship with LearningProfile

`LearningProfile` SHALL continue to contain:

```text
learner_id
```

Relationship:

```text
LearnerIdentity
      │
      │ learner_id
      ▼
LearningProfile
```

`LearningProfile` remains derived aggregate data and is not the
authoritative source of learner identity.

---

# 9. LearnerRepository

Persistence of learner identity SHALL be provided through a dedicated
repository boundary:

```text
LearnerRepository
```

Conceptual operations:

```text
save_learner(learner)
load_learner(learner_id)
load_learners()
```

## 9.1 Save Semantics

`save_learner()` SHALL create a learner when the `learner_id` does not
already exist.

When the same `learner_id` already exists, the saved learner SHALL replace
the previous representation.

## 9.2 Load Semantics

`load_learner(learner_id)` SHALL return a `LearnerIdentity` when the learner
exists.

When the learner does not exist, it SHALL return `None`.

The absence of a learner is therefore a repository lookup result and is
not a valid `LearnerIdentity` state.

## 9.3 Load All Semantics

`load_learners()` SHALL return all persisted learner identities.

An empty learner store SHALL return an empty list rather than `None`.

---

# 10. Repository Responsibility

`LearnerRepository` SHALL be responsible for learner identity persistence.

`LearningRepository` SHALL remain responsible for:

- `StudySession`;
- `LearningProfile`.

Boundaries:

```text
LearnerRepository
└── LearnerIdentity

LearningRepository
├── StudySession
└── LearningProfile
```

Neither repository SHALL become responsible for the other repository's
domain objects.

---

# 11. Storage Boundary

The existing `StorageAdapter` SHALL NOT be modified as a consequence of
this decision.

`StorageAdapter` remains a generic persistence abstraction that operates on
logical storage keys and serialized data.

Learner persistence SHALL use the logical storage key:

```text
learners
```

The Learning Engine SHALL NOT make `StorageAdapter` aware of
`LearnerIdentity`.

---

# 12. Persistence Representation

The serialized learner representation SHALL preserve at least:

```text
learner_id
display_name
is_guest
```

Conceptually:

```json
{
    "learner_id": "learner-001",
    "display_name": "Budi",
    "is_guest": false
}
```

Guest may be represented as:

```json
{
    "learner_id": "guest-001",
    "display_name": "Guest",
    "is_guest": true
}
```

The exact serialization structure remains an implementation detail of
`LearnerRepository`, provided that all required domain information survives
a persistence round-trip.

---

# 13. Active Learner

The currently selected learner SHALL be represented as an application
concern called the Active Learner.

The Active Learner SHALL NOT become a responsibility of
`LearnerRepository`.

Conceptually:

```text
LearnerRepository
       │
       │ loads / saves
       ▼
LearnerIdentity
       │
       ▼
Application State
       │
       ▼
Active Learner
```

The Learning Engine SHALL receive the active learner's `learner_id` as
explicit input when recording learning activities.

---

# 14. Learner Selection and Setup

Before a learning activity that records history can begin, the application
SHALL establish an Active Learner.

The initial learner setup interaction SHALL use:

> Siapkah anda belajar AksaraNusantara?

The user SHALL have the option to:

1. provide a display name; or
2. continue as Guest.

The UI SHALL use the term `Guest` rather than `Anonymous`.

The terminology is intentionally user-friendly and SHALL avoid suggesting
that the application is operating in an anonymous or security-related mode.

---

# 15. Learner Creation Flow

For a new named learner:

```text
User enters name
       │
       ▼
Generate learner_id
       │
       ▼
Create LearnerIdentity
       │
       ▼
Persist learner
       │
       ▼
Set Active Learner
```

For Guest:

```text
User selects Guest
       │
       ▼
Generate learner_id
       │
       ▼
Create LearnerIdentity
       │
       ├── display_name = "Guest"
       └── is_guest = True
       │
       ▼
Persist learner
       │
       ▼
Set Active Learner
```

---

# 16. Learning Activity Flow

Once an Active Learner exists, the application SHALL propagate the learner
identity into the Learning Engine.

```text
Active Learner
      │
      │ learner_id
      ▼
QuizTab
      │
      ▼
LearningService
      │
      ▼
StudySession
      │
      ├── learner_id
      ├── timestamp
      ├── activity_type
      └── payload
```

`QuizTab` SHALL NOT generate or infer learner identity while recording a
learning activity.

The application SHALL provide the learner identity explicitly.

---

# 17. Guest Persistence Semantics

Guest SHALL be persisted as a normal learner identity.

A Guest therefore participates in the same persistence model as a named
learner.

This ensures that:

- `StudySession` ownership remains valid;
- `LearningProfile` can be associated with the Guest;
- the Learning Engine does not require special null handling;
- Guest activities remain structurally consistent with named learner
  activities.

Whether Guest data is retained across application restarts is an
application-policy decision and is outside the core identity model.

The identity model itself SHALL treat Guest as a valid learner.

---

# 18. Separation of Identity and Learning History

Learner identity SHALL remain separate from learning history.

The architecture SHALL NOT embed complete learner information inside every
`StudySession`.

Instead:

```text
LearnerIdentity
      │
      │ learner_id
      ├───────────────┐
      ▼               ▼
StudySession    LearningProfile
```

This preserves normalized ownership and prevents duplicated identity data
inside historical records.

---

# 19. History and Statistics

History remains derived from `StudySession` records as established by
ADR-0002.

The learner identity provides the ownership boundary required to filter
history.

```text
Active Learner
      │
      ▼
learner_id
      │
      ▼
StudySession records
      │
      ├── Session A
      ├── Session B
      └── Session C
             │
             ▼
          History
```

Statistics and learning aggregates SHALL operate within the learner
ownership boundary.

A learner SHALL NOT receive another learner's learning history merely
because both learners use the same application installation.

---

# 20. Security and Privacy Considerations

The learner identity layer SHALL minimize the amount of personal
information required by the application.

A display name is sufficient for the current learner-facing identity
requirement.

The system SHALL NOT require personally identifying information such as:

- email address;
- telephone number;
- physical address;
- password;
- account credentials.

Such information is outside the scope of this ADR.

The stable `learner_id` is an internal identifier and SHALL be treated as
application data rather than a user-facing name.

---

# 21. Consequences

## 21.1 Positive Consequences

This decision provides:

1. Explicit learner identity.
2. Stable ownership of learning activities.
3. Consistent handling of Guest and named learners.
4. Clear separation between identity and learning history.
5. A dedicated persistence boundary for learner identity.
6. Simpler Learning Engine logic because Guest is not a special null state.
7. A foundation for future learner management features.
8. A clean integration point for the application's Active Learner state.

## 21.2 Negative Consequences

This decision introduces:

1. A new domain model.
2. A new repository.
3. A new persistence collection.
4. Additional application state for the Active Learner.
5. Additional tests and persistence handling.
6. A future requirement to define lifecycle behavior for multiple learners.

These costs are accepted because implicit learner identity would create
greater architectural complexity as the application grows.

---

# 22. Alternatives Considered

## 22.1 No Learner Identity Model

Rejected.

This would leave learner identity distributed across application and UI
logic and would make future learner management difficult.

## 22.2 Use `learner_id` Without a Learner Entity

Rejected.

An identifier without a corresponding identity model does not provide a
complete learner domain boundary.

## 22.3 Use `None` for Guest

Rejected.

Using `None` would make Guest equivalent to the absence of a learner and
would require special-case handling throughout the Learning Engine.

## 22.4 Use `"Anonymous"` for Guest

Rejected.

The term "Anonymous" is unnecessarily technical and may imply a security,
privacy, or identity-hiding feature.

The application will use the more approachable term `Guest`.

## 22.5 Store Full LearnerIdentity in StudySession

Rejected.

Embedding the complete learner object into every historical session would
duplicate identity information and weaken the separation between identity
and activity history.

`StudySession` SHALL therefore retain only `learner_id`.

## 22.6 Make Active Learner a Repository Concern

Rejected.

Repositories persist and retrieve domain data. Determining which learner
is currently active is an application-level responsibility.

---

# 23. Compatibility and Migration

ADR-0002 introduced `learner_id` into `StudySession`.

This ADR introduces a formal `LearnerIdentity` model corresponding to those
existing identifiers.

Existing `StudySession` and `LearningProfile` records may reference learner
identifiers for which no persisted `LearnerIdentity` currently exists.

Such records SHALL NOT be silently assigned to an unrelated learner.

Migration of legacy learner identifiers is therefore an explicit
application concern.

The implementation SHALL provide an intentional migration or legacy
handling strategy before existing persisted learning data is exposed as
fully managed learner history.

No destructive migration SHALL be performed automatically as a consequence
of this ADR.

---

# 24. Implementation Contract

The reference implementation SHALL introduce:

```text
core/learning/models/learner_identity.py
```

containing the `LearnerIdentity` domain model.

The implementation SHALL introduce:

```text
core/learning/repositories/learner_repository.py
```

The repository SHALL provide:

```text
save_learner()
load_learner()
load_learners()
```

The implementation SHALL persist learner identities using the existing
`StorageAdapter` abstraction and the logical storage key:

```text
learners
```

The implementation SHALL NOT modify the generic `StorageAdapter` contract.

---

# 25. Required Validation

The implementation SHALL provide tests covering at least:

1. Valid named learner creation.
2. Valid Guest creation.
3. Empty `learner_id` rejection.
4. Empty `display_name` rejection.
5. Learner identity immutability.
6. Stable `learner_id`.
7. Guest flag behavior.
8. Named learner flag behavior.
9. Learner persistence round-trip.
10. Multiple learner persistence.
11. Replacement of an existing learner with the same `learner_id`.
12. Missing learner lookup returning `None`.
13. Empty learner collection returning an empty list.
14. Preservation of Unicode display names.
15. Independence between learner identity and `StudySession`.

---

# 26. Future Compatibility

This ADR intentionally does not define:

- authentication;
- user accounts;
- cloud synchronization;
- passwords;
- email-based identity;
- user profiles beyond display identity;
- remote identity providers;
- multi-device learner synchronization.

Those capabilities may be introduced by future architecture decisions if
required.

Future learner-management features SHALL preserve the invariant that
`learner_id` is the stable ownership identifier used by the Learning Engine.

---

# 27. Architectural Summary

The resulting architecture is:

```text
                    Application
                         │
                         ▼
                  Active Learner
                         │
                         ▼
                 LearnerIdentity
                         │
                         │ learner_id
             ┌───────────┴───────────┐
             ▼                       ▼
      StudySession             LearningProfile
             │                       │
             └───────────┬───────────┘
                         ▼
                  Learning Engine
```

Persistence boundaries:

```text
LearnerRepository
        │
        ▼
   learners.json


LearningRepository
        │
        ├── learning_sessions.json
        │
        └── learning_profiles.json
```

Generic storage remains:

```text
LearnerRepository
       │
       ▼
StorageAdapter
       │
       ▼
JSONStorage
```

The storage layer remains unaware of learner domain semantics.

---

# 28. Decision Status

This ADR is **Accepted**.

The architecture defined in this document SHALL be treated as the
authoritative contract for learner identity and Guest mode.

Implementation work may proceed against this decision.

Any future change to the learner identity model, Guest semantics,
`learner_id` ownership, or repository boundary SHALL require a new ADR or
an explicit superseding revision.

---

# 29. Related Architecture Decisions

This decision is directly related to:

- **ADR-0002 — Learner Ownership of Learning Sessions**

ADR-0002 establishes that every `StudySession` belongs to exactly one
learner.

ADR-0003 establishes the domain identity of that learner and defines how
named learners and Guest learners participate in the Learning Engine.
