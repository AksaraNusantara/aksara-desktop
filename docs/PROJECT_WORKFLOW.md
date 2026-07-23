# PROJECT_WORKFLOW.md

> Single Source of Truth for Aksara Nusantara Development

---

## Project

**Aksara Nusantara**

## Current Milestone

**Core Engine v1.0**

---

# Current Progress

## Phase A — Specification

| Sprint | Topic | Status |
|--------|-------|--------|
| A1 | Introduction, Goals, Terminology | ✅ Complete |
| A2 | Architecture Overview, Lifecycle, Directory Layout | ✅ Complete (Pending Final Review) |
| A3 | Manifest, Metadata, Versioning | 🟡 In Progress |
| A4 | BaseScriptPack Interface | ⏳ Pending |
| A5 | Character Model | ⏳ Pending |
| A6 | Transliteration API | ⏳ Pending |
| A7 | Asset Management | ⏳ Pending |
| A8 | Error Handling, Compatibility, Testing Requirements | ⏳ Pending |
| A9 | Reference Implementation | ⏳ Pending |
| A10 | Review & Freeze Specification v1.0 | ⏳ Pending |

---

## Phase B — Core Engine Implementation

B1 BaseScriptPack
B2 ScriptRegistry
B3 ScriptLoader
B4 ScriptValidator
B5 Character Model
B6 Asset Loader
B7 Unit Tests
B8 Integration Tests
B9 Documentation Update
B10 Core Engine v1.0

Status: ⏳ Waiting for Phase A

---

## Phase C — Reference ScriptPack (Jawa)

C1 Metadata
C2 Character Data
C3 Transliteration
C4 Assets
C5 Flashcard
C6 Quiz
C7 Integration Tests
C8 Alpha Release

Status: ⏳ Waiting for Phase B

---

# Current Session

Current Phase:
Phase A

Current Sprint:
A3

Today's Goal:
- Manifest Specification
- Metadata Specification
- Versioning Rules

Current Mode:
Document Writing

---

# Locked Decisions

## ADR-0001

Entry Point:
scriptpack.py

Status:
Accepted

Reason:
Official entry point for every ScriptPack.

---

# Editorial Policy

- Specifications: English
- ADR: Bahasa Indonesia
- Workflow: English + Bahasa Indonesia (practical)

---

# Development Constitution

1. One Sprint = One Goal
2. Specification Before Implementation
3. Freeze Before Coding
4. New Ideas → Parking Lot
5. Finish → Test → Commit
6. One Conversation = One Deliverable

---

# Parking Lot

- Marketplace
- Plugin Repository
- Cloud Sync
- AI Features
- OCR
- Mobile Version
- Web Version

---

# Definition of Done (Core Engine v1.0)

- BaseScriptPack
- ScriptRegistry
- ScriptLoader
- ScriptValidator
- Character Model
- Transliteration API
- Asset Loader
- Reference ScriptPack (Jawa)
- Unit Tests
- Documentation

---

## Specification Traceability

Before implementation begins, every approved specification SHOULD be mapped to one or more implementation files.

Implementation SHOULD include references to the specification sections being implemented.

This mapping SHALL be maintained in:

docs/development/TRACEABILITY.md

---

---

# Development Lifecycle

Every major feature SHALL follow the lifecycle defined below.

```text
Idea

↓

Discussion

↓

Architecture

↓

Specification

↓

Review

↓

Freeze

↓

Traceability

↓

Implementation

↓

Testing

↓

Review

↓

Release
```

The objective of this lifecycle is to ensure that implementation follows approved specifications rather than undocumented assumptions.

No implementation SHOULD begin before the relevant specification has been reviewed and frozen.

---

# Milestones

The project progresses through major architectural milestones.

## M1 — Core Runtime Frozen

Completed:

- Core Runtime Architecture
- ScriptPack Specification
- Core Engine API
- Traceability Workflow

---

## M2 — Repository Layout Frozen

Completed:

- Repository Structure
- Python Package Layout
- Architectural Layering
- Documentation Organization

---

## M3 — Core Engine Implementation

Planned:

- BaseScriptPack
- Script Validator
- Script Registry
- Script Loader
- Core Engine

---

## M4 — Reference Desktop Application

Planned:

- PySide6 Desktop Application
- Learning Modules
- Quiz System
- User Profiles

---

## M5 — ScriptPack Ecosystem

Future:

- Additional ScriptPacks
- Marketplace
- Plugin Distribution
- Community Contributions

---

# Development Rule

Every implementation SHALL satisfy all of the following:

- traceable to an approved specification;
- documented;
- reviewable;
- testable;
- maintainable.

If an implementation cannot be traced to an approved specification, the implementation SHOULD be reviewed before development continues.

Last Updated:
Sprint A3
