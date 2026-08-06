# PROJECT LOG

---

# Project

## Project Name

Aksara Nusantara

## Repository Status

Application Development

## Current Branch

main

## Current Phase

Application Development

---

# Project Overview

Aksara Nusantara is an extensible desktop learning platform designed to
preserve, learn, and explore the traditional writing systems of the
Indonesian archipelago.

Unlike a single-script application, the platform is built around a
ScriptPack architecture, allowing each writing system to be developed,
maintained, and distributed independently while sharing the same Core
Engine.

The long-term objective is to establish a sustainable ecosystem where
new ScriptPacks, educational modules, datasets, and learning resources
can evolve without requiring changes to the platform architecture.

---

# Current Status

## Foundation

Status

✅ COMPLETED

Summary

The Core Engine architecture has been completed, validated, and frozen
as Foundation v1.0.

Completed

* Core Engine
* Script Registry
* Script Loader
* Script Validator
* ScriptPack Interface
* Character Model v1.0
* Documentation Standards
* Foundation Validation

Validation

Successfully validated using multiple independent ScriptPack
implementations.

---

## Application Development

Status

🟢 ACTIVE

Current Sprint

AD-6 — ScriptPack Audio System

Overall Progress

| Module                | Status     |
| --------------------- | ---------- |
| Home                  | ✅          |
| Script Explorer       | ✅          |
| Audio System          | ✅          |
| Quiz                  | ⏳          |
| Flashcard Enhancement | ⏳          |
| Transliteration       | ⏳          |
| Audio Provider        | 📋 Planned |

---

---

# Foundation Milestones

The Foundation Phase established the architectural principles of the
Aksara Nusantara platform. All components listed in this section are
considered stable and form the long-term foundation for future
development.

---

## Milestone A1

### Core Runtime Architecture

Status

✅ COMPLETED

Completed

* BaseScriptPack interface
* Script Registry
* Script Loader
* Script Validator
* Core Engine public API
* Runtime initialization workflow

Architecture Decisions

* Core Engine is the only public runtime API.
* Registry is the single source of truth for loaded ScriptPacks.
* ScriptPack implementations remain independent from the Core Engine.

---

## Milestone A2

### Exception Hierarchy

Status

✅ COMPLETED

Completed

* CoreEngineError
* ValidationError
* RegistryError
* LoaderError
* EngineError

Result

A unified exception hierarchy is used throughout the Core Engine.

---

## Milestone A3

### ScriptPack Loading Pipeline

Status

✅ COMPLETED

Completed

* Manifest discovery
* Manifest validation
* Dynamic module loading
* ScriptPack registration
* Runtime initialization

Verification

Successfully validated using multiple ScriptPack implementations.

---

## Milestone A4

### Character Model v1.0

Status

✅ COMPLETED

Completed

* Character model simplification
* Repository-based dataset organization
* Character category inferred from repository structure
* Manifest-based ScriptPack versioning

Result

Character Model v1.0 frozen.

---

## Milestone A5

### Foundation Validation

Status

✅ COMPLETED

Completed

* Multi-ScriptPack validation
* Runtime architecture validation
* Public API validation
* Template ScriptPack extraction
* Foundation freeze

Validated ScriptPacks

* Javanese
* Sample

Result

Foundation v1.0 READY

---

# Application Development Milestones

Application Development focuses on building end-user functionality on
top of the frozen Foundation architecture.

---

## AD-1

### Core Engine Integration

Status

✅ COMPLETED

Completed

* Integrated the Core Engine into the desktop application.
* Replaced legacy runtime initialization.
* Established the shared application lifecycle.

---

## AD-2

### Home Module

Status

✅ COMPLETED

Completed

* ScriptPack discovery interface.
* ScriptPack information panel.
* Activation workflow.
* Runtime status display.

---

## AD-3

### Script Explorer

Status

✅ COMPLETED

Completed

* Character browser.
* Dataset navigation.
* Character details.
* Dynamic ScriptPack integration.

---

## AD-4

### AudioService Integration

Status

✅ COMPLETED

Completed

* Shared AudioService.
* Microsoft Edge Neural TTS integration.
* Script Explorer pronunciation support.
* Audio playback service abstraction.

---

## AD-5

### Home Module Refinement

Status

✅ COMPLETED

Completed

* Runtime activation improvements.
* Listener synchronization.
* Script Explorer refresh integration.
* General UI refinement.

---

## AD-6

### ScriptPack Audio System

Status

✅ COMPLETED

Objective

Provide a reusable ScriptPack-aware audio pipeline for the entire
platform.

Completed

* Runtime asset registration.
* ScriptPack runtime paths.
* Bundled audio resolver.
* Generated audio resolver.
* Persistent synthesized speech cache.
* ScriptPack-owned generated audio directory.

Architecture Decisions

* Runtime assets belong to each ScriptPack.
* Generated audio is persistent.
* Playback priority:

  1. Bundled ScriptPack audio.
  2. Generated audio cache.
  3. Microsoft Edge Neural TTS.

Known Limitations

* Edge TTS pronunciation of isolated syllables may differ from native
  pronunciation.

Future Improvements

* Audio Provider architecture.
* Native recorded voices.
* Multiple TTS providers.

---

---

# Current Architecture Status

The application architecture is divided into independent layers with
well-defined responsibilities.

| Layer                | Status                 |
| -------------------- | ---------------------- |
| Core Engine          | ✅ Stable               |
| ScriptPack API       | ✅ Stable               |
| Runtime Registry     | ✅ Stable               |
| Character Repository | ✅ Stable               |
| Asset Management     | ✅ Stable               |
| Audio System         | ✅ Stable               |
| Home Module          | ✅ Stable               |
| Script Explorer      | ✅ Stable               |
| Flashcard            | 🔄 Enhancement Planned |
| Quiz                 | ⏳ Planned              |
| Transliteration      | ⏳ Planned              |

---

# Current ScriptPack Status

| ScriptPack | Status                     |
| ---------- | -------------------------- |
| Javanese   | ✅ Operational              |
| Sample     | ✅ Reference Implementation |

---

# Current Sprint

## AD-7

### Quiz Module

Status

⏳ PLANNED

Objectives

* Implement the Quiz learning module.
* Integrate the Core Engine character repository.
* Support all available ScriptPacks.
* Integrate AudioService.
* Record quiz progress.
* Prepare the foundation for future learning analytics.

Success Criteria

* Quiz works with any active ScriptPack.
* No ScriptPack-specific logic exists inside the Quiz module.
* Character data is obtained exclusively through the Core Engine API.

---

# Technical Backlog

The following items have been identified but intentionally postponed to
maintain focus on the current development roadmap.

---

## AD-10

### Audio Provider Architecture

Status

📋 Planned

Objective

Separate speech generation from AudioService by introducing a provider
abstraction.

Candidate Providers

* Native Recorded Audio
* Microsoft Edge Neural TTS
* Google Text-to-Speech
* Future AI Speech Providers

Expected Benefits

* Improved pronunciation quality.
* Configurable speech engines.
* Native speaker recordings.
* ScriptPack-specific voice resources.

---

## Future Learning System

Status

📋 Planned

Potential Features

* Spaced repetition.
* Learning statistics.
* Progress synchronization.
* Adaptive difficulty.
* Achievement system.

---

## Future ScriptPack Marketplace

Status

📋 Planned

Potential Features

* ScriptPack installation.
* ScriptPack updates.
* Official ScriptPack repository.
* Community-contributed ScriptPacks.
* Version compatibility management.

---

# Long-Term Vision

Aksara Nusantara is designed as an extensible educational platform
rather than a single desktop application.

The Core Engine remains independent from any specific writing system,
allowing new ScriptPacks to be developed without modifying the platform
itself.

Future development will focus on expanding educational modules,
improving learning experiences, and growing the ScriptPack ecosystem
while preserving the stability of the Foundation architecture.

---

# Document Status

Version

2.0

Last Updated

Application Development — AD-6

Repository Status

Foundation v1.0 Completed

Current Focus

AD-7 — Quiz Module

---

