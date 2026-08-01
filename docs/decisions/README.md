# Architecture Decision Records (ADR)

---

## Purpose

Architecture Decision Records (ADRs) document significant architectural decisions made during the development of the Aksara Nusantara ecosystem.

Unlike technical specifications, an ADR explains **why** a decision was made rather than **how** it is implemented.

Each ADR becomes part of the project's permanent architectural history.

---

# Objectives

The ADR process exists to:

- document important architectural decisions;
- record the reasoning behind those decisions;
- improve long-term maintainability;
- preserve historical context;
- reduce repeated architectural discussions;
- support future contributors.

---

# Relationship with Other Documents

Project documentation follows a layered architecture.

```
Vision
¦
+-- PROJECT_BLUEPRINT.md
¦
Architecture
¦
+-- CORE_ARCHITECTURE.md
¦
Engineering Principles
¦
+-- ENGINEERING_PRINCIPLES.md
¦
Architecture Decisions
¦
+-- ADR-xxxx
¦
Technical Specifications
¦
+-- SCRIPTPACK_INTERFACE_SPECIFICATION.md
¦
Implementation
¦
+-- Source Code
```

Each layer has a different responsibility.

| Document | Responsibility |
|-----------|----------------|
| PROJECT_BLUEPRINT | Long-term project vision |
| CORE_ARCHITECTURE | System architecture |
| ENGINEERING_PRINCIPLES | Engineering philosophy |
| ADR | Architectural decisions |
| Specifications | Technical contracts |
| Source Code | Implementation |

---

# When to Create an ADR

An ADR SHOULD be created whenever a decision significantly affects the architecture of the project.

Typical examples include:

- introducing new architectural concepts;
- modifying the runtime lifecycle;
- changing public APIs;
- replacing major subsystems;
- introducing new extension mechanisms;
- changing dependency management;
- defining long-term architectural policies.

Routine implementation details SHOULD NOT require an ADR.

---

# ADR Lifecycle

Each ADR progresses through the following lifecycle.

```
Proposed

?

Accepted

?

Implemented

?

Superseded (optional)

?

Deprecated (optional)
```

Only **Accepted** ADRs SHALL influence project specifications.

---

# Status Values

Every ADR SHALL define one of the following status values.

| Status | Meaning |
|---------|---------|
| Proposed | Under discussion |
| Accepted | Official project decision |
| Implemented | Fully reflected in implementation |
| Superseded | Replaced by another ADR |
| Deprecated | Retained for historical reference |

---

# Naming Convention

Each ADR SHALL follow the naming convention:

```
ADR-XXXX-short-title.md
```

Examples:

```
ADR-0001-separate-scriptpack-discovery-from-activation.md

ADR-0002-scriptpack-marketplace.md

ADR-0003-runtime-dependency-resolution.md
```

ADR numbers SHALL be sequential.

Numbers SHALL NOT be reused.

---

# Required Structure

Every ADR SHOULD contain the following sections.

```
Document Information

Introduction

Context

Problem Statement

Decision

Rationale

Architectural Impact

Consequences

Alternatives Considered

Migration Strategy

Backward Compatibility

Future Considerations

References

Decision Summary
```

Additional sections MAY be included when appropriate.

---

# Relationship with Specifications

An ADR does not replace technical specifications.

Instead:

```
ADR

?

Architecture

?

Specification

?

Implementation
```

Specifications SHALL remain consistent with Accepted ADRs.

Implementation SHALL remain consistent with project specifications.

---

# Revision Policy

ADRs SHOULD NOT be modified after being accepted except for:

- correcting typographical errors;
- clarifying wording;
- updating references.

If an architectural decision changes, a new ADR SHOULD be created.

Previous ADRs SHALL remain part of the project's historical record.

---

# Design Philosophy

Architecture evolves.

Design decisions made during one stage of development may become insufficient as the project grows.

Rather than rewriting history, the project records each significant decision together with its rationale.

This preserves architectural context and enables future contributors to understand not only what changed, but why the change occurred.

---

# Current ADRs

| ADR | Title | Status |
|------|-------|--------|
| ADR-0001 | Separate ScriptPack Discovery from Activation | Accepted |