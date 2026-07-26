# Contributing to Aksara Nusantara

First of all, thank you for considering contributing to **Aksara Nusantara**.

Every contribution—whether it is code, documentation, design, translation, testing, research, or simply reporting an issue—helps preserve Indonesia's traditional writing systems for future generations.

We believe open-source software grows through collaboration, mutual respect, and continuous learning.

Welcome aboard.

---

# Project Philosophy

Aksara Nusantara follows an **architecture-first** development model.

Before implementing major features, contributors are expected to understand the project's architecture and specifications.

The project follows these principles:

* Specification Before Implementation
* Architecture Before Features
* Traceability Before Coding
* Documentation Is Part of Development
* Testing Before Commit
* Small Commits, Clear History

Maintainability is always preferred over rapid feature development.

---

# Ways to Contribute

There are many ways to contribute.

## 💻 Code

* Bug fixes
* New features
* Performance improvements
* Refactoring
* Unit tests

## 📚 Documentation

* Improve documentation
* Write tutorials
* Fix grammar
* Improve examples
* Translate documents

## 🎨 Design

* Icons
* UI improvements
* Illustrations
* Screenshots

## 🔤 Linguistics

* Transliteration improvements
* Script validation
* Unicode verification
* Historical research

## 🧪 Testing

* Integration testing
* Unit testing
* Platform compatibility
* Bug verification

---

# Development Workflow

Every major contribution follows the same workflow.

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

Implementation

↓

Testing

↓

Documentation

↓

Commit
```

Please do not skip documentation.

Documentation is considered part of the implementation.

---

# Development Setup

Clone the repository.

```bash
git clone https://github.com/AksaraNusantara/aksara-desktop.git
```

Enter the project directory.

```bash
cd aksara-desktop
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
python main.py
```

---

# Branch Naming

Please create a dedicated branch for your work.

Examples

```text
feature/add-balinese-script

feature/improve-quiz

fix/transliteration-bug

docs/update-readme

refactor/core-engine
```

Avoid committing directly to the `main` branch.

---

# Commit Message Convention

The project follows the Conventional Commit style.

Examples

```text
feat(core): implement ScriptPack registry

fix(loader): improve manifest validation

docs(readme): rewrite project overview

refactor(core): simplify registry implementation

test(core): add integration tests

chore: update dependencies
```

Keep commits focused on a single logical change.

---

# Coding Standards

General guidelines:

* Follow PEP 8.
* Prefer readability over cleverness.
* Keep functions focused.
* Avoid unnecessary complexity.
* Write descriptive variable names.
* Minimize hidden dependencies.
* Document public APIs.

Please follow the project's coding templates whenever applicable.

---

# Documentation

Documentation is part of the implementation.

If your contribution changes:

* architecture,
* workflow,
* APIs,
* specifications,
* repository structure,

please update the relevant documentation before submitting a Pull Request.

Documentation and code should evolve together.

---

# Traceability

Major implementations should be traceable to an approved specification.

Whenever practical, reference the specification or design document being implemented.

Examples include:

* AN-STD-001
* TRACEABILITY.md
* SCRIPTPACK_INTERFACE_SPECIFICATION.md

Traceability helps future contributors understand *why* a piece of code exists.

---

# Testing

Before submitting a Pull Request:

* Verify the application starts correctly.
* Run available tests.
* Ensure new functionality behaves as expected.
* Update tests when necessary.
* Verify documentation remains accurate.

Code that cannot be verified should not be merged.

---

# Pull Requests

Before opening a Pull Request, ensure that:

* The application runs correctly.
* Coding standards are followed.
* Documentation has been updated when necessary.
* Tests pass.
* Commit messages follow the project convention.

Please provide a clear description of the changes and their purpose.

---

# Reporting Bugs

When reporting bugs, please include:

* Operating system
* Python version
* Steps to reproduce
* Expected behavior
* Actual behavior
* Screenshots (if applicable)

The more information you provide, the easier it is to reproduce and fix the problem.

---

# Suggesting Features

Feature requests are always welcome.

Please explain:

* What problem does it solve?
* Why is it valuable?
* Possible implementation ideas (optional)

Major features may require architectural discussion before implementation.

---

# Useful Documents

The following documents are recommended reading.

| Document                              | Purpose                      |
| ------------------------------------- | ---------------------------- |
| README.md                             | Project overview             |
| START_HERE.md                         | Developer onboarding         |
| PROJECT_WORKFLOW.md                   | Current milestone and sprint |
| TRACEABILITY.md                       | Design traceability          |
| SCRIPTPACK_INTERFACE_SPECIFICATION.md | ScriptPack architecture      |
| CHANGELOG.md                          | Project history              |

---

# Questions

If you are unsure about anything, please open a GitHub Discussion or Issue before starting major work.

Early discussion usually leads to better solutions.

---

# Thank You

Thank you for helping preserve Indonesia's traditional writing systems through open-source software.

Every contribution—large or small—helps build a sustainable platform for future generations.

---

**Learn. Preserve. Extend.**
