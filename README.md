# Aksara Nusantara

> **Learn. Preserve. Extend.**
>
> *An Open Source Platform for Traditional Script Preservation.*

---

## Overview

**Aksara Nusantara** is an open-source platform designed to preserve, study, and extend the traditional writing systems of Indonesia through a modern and extensible software architecture.

Instead of supporting only a single script, Aksara Nusantara introduces a **ScriptPack Architecture**, allowing each writing system to be developed, maintained, and distributed independently while sharing the same Core Engine.

The Desktop Edition is the first reference implementation of this platform.

---

# Vision

Indonesia is home to dozens of traditional writing systems representing centuries of history, literature, philosophy, and culture.

Many of these scripts are becoming less familiar to younger generations.

Aksara Nusantara exists to help preserve this cultural heritage through:

* Open-source software
* Educational resources
* Community collaboration
* Standardized ScriptPack architecture

Technology should not replace culture.

Technology should help preserve it.

---

# Project Architecture

```text
                     Aksara Nusantara Platform

                               ¦

               +-------------------------------+

               ¦                               ¦

          Core Engine                    ScriptPacks

               ¦                               ¦

               ¦                 Javanese ScriptPack

               ¦                 Balinese ScriptPack

               ¦                 Sundanese ScriptPack

               ¦                 ...

               ¦

        Desktop Edition

        Future Mobile Edition

        Future Web Edition
```

The Core Engine provides generic services.

Every writing system is implemented as an independent ScriptPack.

---

# Core Features

Current platform capabilities include:

* ScriptPack Architecture
* Core Engine
* ScriptPack Validator
* ScriptPack Loader
* ScriptPack Registry
* Character Repository
* Asset Management
* Transliteration Framework
* Audio Support Framework
* Extensible Design

The Desktop Edition additionally provides:

* Alphabet Learning
* Flashcards
* Interactive Quiz
* Transliteration
* Progress Tracking

---

# Current Development Status

Project Status

?? Active Development

Current Version

**v0.1 (Foundation)**

Current Milestone

**Foundation v0.1**

Completed

* Core Engine
* ScriptPack Architecture
* Validator
* Loader
* Registry
* Integration Test
* Documentation Framework

In Progress

* Documentation Synchronization
* Reference ScriptPack

Planned

* Desktop Integration
* Additional ScriptPacks

---

# Repository Structure

```text
core/
    Core Engine

scriptpacks/
    ScriptPack implementations

docs/
    Specifications
    Standards
    Development documentation

assets/
    Shared project assets

main.py
requirements.txt
README.md
LICENSE
```

---

# Getting Started

## Requirements

* Python 3.12+
* PySide6
* Windows or Linux

Clone the repository:

```bash
git clone https://github.com/AksaraNusantara/aksara-desktop.git

cd aksara-desktop
```

Create a virtual environment:

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

---

# Documentation

Project documentation is available in the **docs/** directory.

Important documents include:

* START_HERE.md
* PROJECT_WORKFLOW.md
* CHANGELOG.md
* CONTRIBUTING.md
* TRACEABILITY.md
* SCRIPTPACK_INTERFACE_SPECIFICATION.md

---

# Roadmap

## Foundation

* Complete documentation
* Reference ScriptPack
* Desktop integration

## Platform

* Multiple ScriptPacks
* Theme system
* Audio framework
* Character repository

## Ecosystem

* Android Edition
* Web Edition
* Marketplace
* Community ScriptPacks
* Dataset Projects
* Font Projects

---

# Contributing

Contributions are welcome.

Whether you are a developer, linguist, educator, designer, student, or simply interested in preserving Indonesia's traditional writing systems, your contribution is greatly appreciated.

Please read **CONTRIBUTING.md** before submitting pull requests.

---

# License

This project is licensed under the MIT License.

See the **LICENSE** file for details.

---

# About the Project

Aksara Nusantara is not only a desktop application.

It is an extensible platform for preserving traditional writing systems through open standards and reusable software components.

The long-term objective is to build an ecosystem where new writing systems can be added simply by creating new ScriptPacks, without modifying the Core Engine.

---

> **Technology preserves knowledge.**
>
> **People preserve culture.**
