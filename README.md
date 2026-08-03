# Aksara Nusantara

> **Learn. Preserve. Extend.**
>
> *An Open Source Platform for Traditional Script Preservation.*

------------------------------------------------------------------------

## Overview

**Aksara Nusantara** is an open-source platform for preserving,
studying, and extending the traditional writing systems of Indonesia
through a modular software architecture.

The project is built around a **Core Engine** and a standardized
**ScriptPack Architecture**. Each writing system is implemented as an
independent ScriptPack while sharing the same engine, making the
platform extensible without modifying its foundation.

The Desktop Edition is the first reference implementation of the
platform.

------------------------------------------------------------------------

# Vision

Indonesia is home to dozens of traditional writing systems representing
centuries of history, literature, philosophy, and culture.

Aksara Nusantara exists to help preserve this heritage through:

-   Open-source software
-   Educational resources
-   Community collaboration
-   Standardized ScriptPack architecture

> Technology should help preserve culture---not replace it.

------------------------------------------------------------------------

# Project Architecture

``` text
                    Aksara Nusantara Platform

                           Core Engine
                                │
      ┌─────────────────────────┼─────────────────────────┐
      │                         │                         │
 ScriptPack API          Desktop Edition          Future Editions
      │                         │              (Mobile / Web / CLI)
      │
 ├── Javanese
 ├── Balinese
 ├── Rejang
 └── Community ScriptPacks
```

------------------------------------------------------------------------

# Current Features

## Core Platform

-   Core Engine
-   ScriptPack Architecture
-   ScriptPack Loader
-   ScriptPack Registry
-   ScriptPack Validator
-   Character Repository
-   Asset Management
-   Transliteration Framework
-   Audio Framework

## Desktop Edition

-   HomeTab
-   ScriptPack Management
-   ScriptPack Activation
-   Runtime Asset Registration
-   Core Engine Integration

------------------------------------------------------------------------

# Development Status

**Project Status**

Active Development

**Current Version**

v0.1 Foundation

**Current Milestone**

**Milestone M1 -- Core Engine Integration**

### Completed

-   Core Engine
-   ScriptPack Architecture
-   Loader
-   Registry
-   Validator
-   Reference Javanese ScriptPack
-   Desktop Integration
-   HomeTab
-   ScriptPack Management Interface

### In Progress

-   Flashcard Module

### Planned

-   Quiz Module
-   Transliteration Module
-   Progress Tracking
-   Additional ScriptPacks

------------------------------------------------------------------------

# Repository Structure

``` text
application/
core/
docs/
scriptpacks/
ui/
main.py
requirements.txt
README.md
LICENSE
```

Each ScriptPack owns its own assets (fonts, characters, audio, images).
Shared runtime behavior belongs in the Core Engine.

------------------------------------------------------------------------

# Getting Started

## Requirements

-   Python 3.12+
-   PySide6

``` bash
git clone https://github.com/AksaraNusantara/aksara-desktop.git
cd aksara-desktop
python -m venv .venv
```

Windows

``` bash
.venv\Scripts\activate
```

Linux

``` bash
source .venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run:

``` bash
python main.py
```

------------------------------------------------------------------------

# Documentation

Project documentation is located in the `docs/` directory.

Recommended reading order:

1.  START_HERE.md
2.  PROJECT_CHARTER.md
3.  ENGINEERING_PRINCIPLES.md
4.  CORE_ARCHITECTURE.md
5.  SCRIPTPACK_INTERFACE_SPECIFICATION.md
6.  PROJECT_WORKFLOW.md

------------------------------------------------------------------------

# Roadmap

## Milestone M1

-   Core Engine Integration ✅
-   HomeTab ✅

## Milestone M2

-   Flashcard Module
-   Quiz Module
-   Transliteration

## Milestone M3

-   Additional ScriptPacks
-   Theme System
-   Audio Expansion

## Long-term Vision

-   Android Edition
-   Web Edition
-   Community Marketplace
-   ScriptPack Ecosystem

------------------------------------------------------------------------

# Contributing

Contributions from developers, linguists, educators, designers, and
cultural communities are welcome.

Please read **CONTRIBUTING.md** before submitting pull requests.

------------------------------------------------------------------------

# License

Released under the MIT License.

See **LICENSE** for details.

------------------------------------------------------------------------

# About

Aksara Nusantara is more than a desktop application.

It is an extensible platform for preserving traditional writing systems
through open standards, reusable software components, and an open
ScriptPack ecosystem.

> **Technology preserves knowledge.**
>
> **People preserve culture.**
