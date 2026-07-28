# PROJECT_WORKFLOW.md

> **Project:** Aksara Nusantara
>
> **Document Version:** 1.1
>
> **Status:** Active
>
> **Last Updated:** 2026-07
>
> **Maintainer:** Aksara Nusantara Project

---

# 1. Purpose

This document describes the overall development workflow of the
Aksara Nusantara ecosystem.

It serves as the primary navigation document for the project,
allowing contributors to understand:

- current project phase
- current sprint
- completed milestones
- upcoming milestones
- implementation workflow
- development policies

This document intentionally provides a high-level overview.
Technical specifications are documented separately.

---

# 2. Current Project Status

## Current Phase

**Phase D — AksaraDesktop Revival**

---

## Current Sprint

**Sprint AD-1**

Goal:

Bring AksaraDesktop back to life using the new Core Engine and
the official Javanese ScriptPack.

---

## Current Milestone

?? **First Character Loaded**

Target:

The application successfully displays the first Javanese character
loaded through the complete Core Engine pipeline.

---

## Foundation Status

? Foundation v1.0 Frozen

The Foundation architecture has been completed and SHALL remain
stable unless a future major version requires architectural changes.

---

# 3. Project Roadmap

```
Phase A
Foundation Design
        ¦
        ?
Phase B
Core Engine
        ¦
        ?
Phase C
ScriptPack Ecosystem
        ¦
        ?

==========================
FOUNDATION v1.0 FROZEN
==========================

        ¦
        ?
Phase D
AksaraDesktop Revival
        ¦
        ?
Phase E
Learning Modules
        ¦
        ?
Phase F
Plugin Ecosystem
        ¦
        ?
Phase G
Marketplace
```

---

# 4. Completed Milestones

## Milestone F1

Foundation v1.0 Frozen

Completed Components:

- Core Engine
- Registry
- Validator
- Exception Hierarchy
- BaseScriptPack
- ScriptPack Specification
- Character Repository Specification
- Character Style Guide
- Reference Template
- Sample ScriptPack
- Javanese ScriptPack
- Foundation Validation

Status:

? COMPLETE

---

# 5. Current Sprint (AD-1)

Objective

Reconnect the desktop application to the new Foundation.

Deliverables

- CoreEngine.initialize()
- MainWindow
- ScriptPack loading
- Character Repository loading
- Character Browser
- First Character Loaded

---

# 6. Development Workflow

Every new feature SHALL follow the workflow below.

```
Idea

    ¦

    ?

Specification

    ¦

    ?

Reference Implementation

    ¦

    ?

Reference Dataset

    ¦

    ?

Validation

    ¦

    ?

Integration Test

    ¦

    ?

Production
```

No implementation SHALL bypass this workflow.

---

# 7. ScriptPack Development Workflow

Every ScriptPack SHALL follow the same lifecycle.

```
Create ScriptPack

        ¦

        ?

script.json

        ¦

        ?

Character Repository

        ¦

        ?

Validation

        ¦

        ?

Integration Test

        ¦

        ?

Production Ready
```

---

# 8. Character Repository Workflow

Character repositories SHALL follow a consistent structure.

```
Character Definition

        ¦

        ?

JSON Validation

        ¦

        ?

Repository Validation

        ¦

        ?

Core Engine Loading

        ¦

        ?

UI Integration
```

Character repositories SHALL comply with:

- CHARACTER_STYLE_GUIDE.md
- SCRIPTPACK_INTERFACE_SPECIFICATION.md

---

# 9. Reference Implementation Policy

Whenever a specification changes,
the following components SHALL be updated together.

1. Specification
2. Template
3. Sample ScriptPack
4. Production ScriptPack
5. Reference Dataset
6. Tests
7. Documentation

No implementation SHALL intentionally diverge from the
current specification.

---

# 10. Validation Policy

Every architectural component SHALL provide validation.

Validation levels include:

- Unit Test
- Foundation Validation
- Integration Test

A feature SHALL NOT be considered complete until all
relevant validation passes successfully.

---

# 11. Documentation Policy

Documentation SHALL evolve together with the source code.

Whenever a structural change occurs,
the following SHALL be reviewed.

- README
- PROJECT_WORKFLOW
- CHANGELOG
- Specifications
- Style Guides

Documentation SHALL NOT become outdated.

---

# 12. Git Workflow

Recommended workflow.

```
Specification

        ¦

        ?

Implementation

        ¦

        ?

Validation

        ¦

        ?

Commit

        ¦

        ?

Documentation Review
```

Every commit SHOULD represent one logical change.

---

# 13. Current Backlog

Priority

## High

- Character Browser
- MainWindow integration
- CoreEngine.initialize()
- Character rendering
- ScriptPack selector

---

## Medium

- Flashcard module
- Quiz module
- Search
- Character details

---

## Low

- Marketplace
- Plugin Manager
- Theme system

---

# 14. Future Milestones

## AD-1

?? First Character Loaded

---

## AD-2

Character Browser Completed

---

## AD-3

Flashcard System

---

## AD-4

Quiz System

---

## AD-5

Transliteration Engine

---

## AD-6

ScriptPack Marketplace

---

# 15. Guiding Principles

The project follows several fundamental principles.

- Foundation First
- Specification Before Implementation
- Validation Before Release
- Documentation as Code
- Simplicity Over Complexity
- One Source of Truth
- Backward compatibility is optional during Foundation development
- Consistency across all ScriptPacks

---

# 16. Definition of Done

A task is considered complete only when:

- implementation finished
- validation passed
- integration test passed
- documentation updated
- specification synchronized
- reference implementation synchronized
- reference dataset synchronized

Only then may the task be marked as completed.

---

# 17. Next Immediate Goal

Current target:

?? **First Character Loaded**

Pipeline:

```
MainWindow

    ¦

    ?

CoreEngine.initialize()

    ¦

    ?

Registry

    ¦

    ?

Javanese ScriptPack

    ¦

    ?

Character Repository

    ¦

    ?

Character Browser

    ¦

    ?

?
```

This milestone marks the successful completion of the Foundation
integration into AksaraDesktop.

---

End of Document