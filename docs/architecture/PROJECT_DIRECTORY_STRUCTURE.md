# Project Directory Structure

**Document ID:** AN-ARC-004  
**Status:** Draft v1.0  
**Owner:** Aksara Nusantara Project  
**Last Updated:** 2026-07-23

---

# 1. Purpose

This document defines the recommended repository directory structure for the Aksara Nusantara ecosystem.

The purpose of this structure is to maintain a clean separation between documentation, source code, assets, user-generated data, testing resources, and future ecosystem components.

---

# 2. Design Goals

The repository structure SHALL:

- remain easy to understand;
- support long-term maintenance;
- minimize future refactoring;
- separate implementation from documentation;
- support multiple applications built on the same framework.

---

# 3. Top-Level Repository Structure

A typical repository SHALL follow a structure similar to:

```text
Repository/

+-- assets/
+-- docs/
+-- profiles/
+-- src/
+-- tests/
+-- examples/
¦
+-- README.md
+-- LICENSE
+-- CHANGELOG.md
+-- CONTRIBUTING.md
+-- CODE_OF_CONDUCT.md
+-- SECURITY.md
+-- START_HERE.md
+-- requirements.txt
```

Additional top-level directories MAY be introduced when required.

---

# 4. Directory Responsibilities

## assets/

Stores project assets.

Examples include:

- fonts
- icons
- images
- sounds
- themes

Assets SHALL NOT contain Python source code.

---

## docs/

Stores all project documentation.

Documentation categories MAY include:

- architecture
- governance
- standards
- roadmap
- development
- legal

Documentation SHALL remain independent from implementation.

---

## profiles/

Stores user-generated learning data.

Typical contents include:

- quiz results
- learning progress
- application profiles

Profiles SHALL NOT contain application source code.

---

## src/

Contains all Python source code.

No implementation source code SHOULD exist outside this directory.

---

## tests/

Contains automated testing resources.

Examples include:

- unit tests
- integration tests
- regression tests

Testing SHALL remain independent from production code.

---

## examples/

Contains sample applications demonstrating usage of the framework.

Examples MAY include:

- desktop application
- command-line interface
- sample ScriptPacks

Examples SHALL NOT replace production applications.

---

# 5. Source Directory Layout

The `src/` directory SHOULD contain the primary Python package.

Example:

```text
src/

    aksara_nusantara/

        core/

        data/

        ui/

        utils/

        widgets/

        applications/
```

Future versions MAY introduce additional packages.

---

# 6. Documentation Independence

Project documentation SHALL remain outside the Python package.

Documentation SHALL NOT depend on Python imports.

---

# 7. Future Expansion

Future repository versions MAY introduce directories including:

- marketplace/
- plugins/
- tools/
- scripts/
- ci/

Such additions SHOULD preserve the overall repository organization.

---

# 8. Conformance

Repository implementations claiming compliance with this document SHALL preserve the architectural separation described herein.

Alternative layouts MAY be adopted provided that equivalent separation of responsibilities is maintained.
