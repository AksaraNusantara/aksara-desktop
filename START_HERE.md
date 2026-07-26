# START_HERE.md

> Developer Onboarding Guide for Aksara Nusantara

---

# Welcome

Welcome to the **Aksara Nusantara** project.

This document is intended for developers who want to understand the project architecture and contribute to its development.

If this is your first time opening the repository, start here.

---

# What is Aksara Nusantara?

Aksara Nusantara is an open-source platform for learning, preserving, and extending the traditional writing systems of Indonesia.

The project is built around a **ScriptPack Architecture**, allowing each writing system to be implemented independently while sharing a common Core Engine.

The Desktop Edition is the first reference implementation of the platform.

---

# Project Philosophy

The project follows several core principles.

* Specification Before Implementation
* Architecture Before Features
* Traceability Before Coding
* Documentation Is Part of Development
* Small Commits, Clear History

Every major implementation should be backed by an approved specification.

---

# Repository Overview

```text
core/
    Core Engine

scriptpacks/
    Independent ScriptPack implementations

docs/
    Specifications
    Standards
    Development documentation

assets/
    Shared assets

main.py
```

The **Core Engine** contains generic platform services.

Everything specific to a writing system belongs inside a **ScriptPack**.

---

# Read These Documents First

The repository contains several important documents.

| If you want to...                   | Read                                  |
| ----------------------------------- | ------------------------------------- |
| Understand the project              | README.md                             |
| Follow the current development      | PROJECT_WORKFLOW.md                   |
| Understand the architecture         | SCRIPTPACK_INTERFACE_SPECIFICATION.md |
| Understand implementation decisions | TRACEABILITY.md                       |
| View project history                | CHANGELOG.md                          |
| Contribute to the project           | CONTRIBUTING.md                       |

---

# Development Workflow

Every feature follows the same workflow.

```text
Idea

?

Discussion

?

Architecture

?

Specification

?

Review

?

Implementation

?

Testing

?

Documentation

?

Commit
```

Do not skip documentation.

Documentation is considered part of the implementation.

---

# Coding Standards

Before writing code, please read the project's coding standards.

The project follows:

* Python Module Template
* Traceability Rules
* Documentation Standards
* ScriptPack Specification

Whenever possible:

* Write small commits.
* Keep functions focused.
* Avoid hidden dependencies.
* Prefer readability over cleverness.

---

# Current Milestone

Current Milestone

**Foundation v0.1**

Current Focus

* Documentation Synchronization
* Reference ScriptPack
* Desktop Integration Preparation

See **PROJECT_WORKFLOW.md** for the latest sprint information.

---

# Creating Your First Contribution

Before submitting a Pull Request, make sure that you have completed the following checklist.

* Read README.md
* Read PROJECT_WORKFLOW.md
* Read TRACEABILITY.md
* Follow the project coding standards
* Write or update tests
* Update documentation if necessary
* Verify that the application still works
* Create a clear commit message

---

# Commit Message Style

The project prefers Conventional Commit style.

Examples:

```text
feat(core): implement ScriptPack registry

fix(loader): improve manifest validation

docs(readme): rewrite project overview

test(core): add integration tests
```

---

# Need Help?

If you are unsure where to start:

1. Read PROJECT_WORKFLOW.md.
2. Pick the current sprint.
3. Work on one task at a time.
4. Keep commits small and focused.

---

# Thank You

Thank you for contributing to Aksara Nusantara.

Every contribution—whether code, documentation, testing, translation, or design—helps preserve Indonesia's traditional writing systems for future generations.

Happy coding!
