# Aksara Nusantara Project Blueprint

> Technology changes rapidly, but cultural heritage deserves to endure.
>
> **Aksara Nusantara exists to bridge those two worlds through open collaboration.**

---

# 1. Introduction

Aksara Nusantara is an open-source ecosystem dedicated to the preservation, education, and technological development of the traditional writing systems of the Indonesian archipelago.

Rather than focusing on a single script or a single application, the project aims to establish a sustainable platform where every traditional script can be represented, studied, and expanded through a common technological foundation.

The project combines educational applications, modular software architecture, comprehensive documentation, and an open community to encourage long-term collaboration.

---

# 2. Vision

To become the leading open-source ecosystem for preserving, learning, and advancing the traditional writing systems of the Indonesian archipelago through modern technology and collaborative innovation.

---

# 3. Mission

The project is built upon seven primary missions.

## Preserve

Preserve traditional writing systems through open digital technologies.

## Educate

Provide modern learning tools that make traditional scripts accessible for everyone.

## Standardize

Adopt Unicode as the official representation for every supported script.

## Modularize

Design every script as an independent extension built upon a common Core Engine.

## Collaborate

Encourage educators, researchers, students, cultural communities, and software developers to collaborate.

## Document

Maintain professional documentation that supports both users and contributors.

## Sustain

Build an ecosystem capable of long-term growth through open collaboration and sustainable funding models.

---

# 4. Project Identity

| Item | Value |
|------|-------|
| Project Name | Aksara Nusantara |
| Project Type | Open Source Ecosystem |
| Primary Goal | Education & Cultural Preservation |
| License | GNU GPL v3 |
| Primary Language | Python |
| Architecture | Modular |
| Unicode Compliance | Required |
| Plugin System | Planned |
| Community Driven | Yes |

---

# 5. Core Values

The project follows five fundamental values.

## Education First

Technology serves learning.

## Open by Default

Knowledge grows through collaboration.

## Unicode First

Standards ensure interoperability.

## Modular Architecture

Small Core. Independent Extensions.

## Long-term Sustainability

Every decision should support the future of the ecosystem.

---

# 6. Project Scope

Included within the project:

- Desktop Application
- Script Engine
- Learning Engine
- Plugin System
- Documentation
- Educational Resources
- Website
- SDK

Currently outside the project scope:

- OCR
- Keyboard Driver
- Font Editor
- Typesetting Software

These topics may be considered in future ecosystem projects.

---

# 7. Ecosystem Overview

Aksara Nusantara consists of several major components.

- Core Engine
- Learning Engine
- Desktop Application
- Website
- Documentation
- Plugin Repository
- Community
- SDK

Each component evolves independently while sharing a common architectural philosophy.

---

# 8. Architectural Philosophy

The Core should remain small, stable, and independent.

It should never contain language-specific rules.

Every traditional script is implemented as a plugin.

The User Interface should never contain linguistic logic.

Language rules belong inside each plugin.

---

# 9. Learning Philosophy

Learning traditional scripts requires more than simple transliteration.

The platform supports multiple learning approaches including:

- Flashcards
- Quizzes
- Audio Pronunciation
- Writing Practice
- Progress Tracking
- Review Sessions
- Future Spaced Repetition

The learner—not the technology—is the center of every design decision.

---

# 10. Plugin Philosophy

Every supported writing system is treated equally.

Examples include:

- Javanese
- Balinese
- Sundanese
- Batak
- Lampung
- Rejang
- Bugis
- Makassar
- Kawi

Each plugin owns:

- Unicode Mapping
- Transliteration Rules
- Parser
- Learning Content
- Audio Resources
- Metadata

---

# 11. Sustainability

The Core ecosystem will always remain open source.

Long-term sustainability may be supported through:

- Donations
- Printed learning materials
- Workbooks
- Workshops
- Educational partnerships
- Sponsorships

Commercial activities should strengthen—not restrict—the open-source ecosystem.

---

# 12. Community

The project welcomes contributors from various backgrounds.

Including:

- Software Developers
- Linguists
- Historians
- Educators
- Designers
- Translators
- Students
- Cultural Communities

Everyone contributes according to their expertise.

---

# 13. Five-Year Vision

## Foundation

Build a stable educational platform.

## Expansion

Support multiple traditional scripts.

## Community

Grow an active open-source community.

## Platform

Provide SDKs, APIs, and additional applications.

## Preservation

Become a trusted technological foundation for preserving Nusantara writing systems.

---

# 14. North Star

Every technical decision should make learning easier and cultural preservation stronger.

---

# Conclusion

Aksara Nusantara is more than a desktop application.

It is a long-term open-source ecosystem dedicated to preserving one of Indonesia's most valuable cultural heritages through modern software engineering, collaborative development, and accessible education.

Technology changes.

Culture remains.

Aksara Nusantara exists to connect both.

---

# Architecture Evolution

## From Desktop Application to Ecosystem

The Aksara Nusantara project originally began as a desktop application for learning the Javanese script (Hanacaraka).

As the project evolved, its scope expanded beyond a single application.

The project is now designed as a reusable software ecosystem consisting of:

- a reusable Core Engine;
- standardized ScriptPack implementations;
- multiple applications built upon the same runtime;
- future extension through additional writing systems.

Desktop applications are therefore considered one possible consumer of the framework rather than the framework itself.

---

## Layered Architecture

The ecosystem follows a layered architecture.

```text
Repository

        ¦

        ?

Python Package

        ¦

        ?

Core Engine

        ¦

        ?

ScriptPack

        ¦

        ?

Applications
```

Each layer has a clearly defined responsibility.

Higher layers depend on lower layers.

Lower layers SHALL NOT depend on higher layers.

---

## Architectural Dependency

The dependency direction SHALL always be:

Applications

?

Core Engine

?

ScriptPack Interface

?

ScriptPack Implementation

Applications SHALL communicate with the Core Engine through the public API.

Applications SHOULD NOT access internal runtime components directly.

---

## Architectural Goals

The layered architecture supports:

- maintainability;
- scalability;
- modularity;
- testability;
- future expansion;
- multiple user interfaces.

Future implementations MAY include:

- desktop applications;
- command-line tools;
- web applications;
- mobile applications;
- cloud services.

All implementations SHALL share the same Core Engine whenever practical.