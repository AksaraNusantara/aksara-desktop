# AN-STD-001

# ScriptPack Interface Specification

---

## Document Information

| Item         | Value                              |
| ------------ | ---------------------------------- |
| Document ID  | AN-STD-001                         |
| Title        | ScriptPack Interface Specification |
| Status       | Foundation v1.0 (Frozen)           |
| Version      | 1.0                                |
| Stability    | Frozen                             |
| Owner        | Aksara Nusantara Project           |
| License      | MIT                                |
| Last Updated | 2026-07-26                         |

---

# Revision History

| Version | Date        | Description                                                                |
| ------- | ----------- | -------------------------------------------------------------------------- |
| 0.x     | Development | Initial drafting and architectural exploration                             |
| 1.0     | 2026-07-26  | First frozen specification aligned with the Foundation v0.1 implementation |

---

# Table of Contents

1. Introduction
2. Scope
3. Terminology
4. Conformance
5. Design Principles
6. ScriptPack Architecture
7. ScriptPack Directory Layout
8. Manifest
9. Metadata
10. Versioning and Compatibility
11. BaseScriptPack Interface
12. Script Registry
13. Script Loader
14. Script Validation
15. Core Engine API
16. Character Model
17. Transliteration
18. Audio Support
19. Error Handling
20. Security Considerations
21. Future Compatibility

Appendix A — Manifest Example

Appendix B — Directory Layout Example

Appendix C — Glossary

Appendix D — Core Engine Lifecycle

Appendix E — Reference Implementation

---

# 1. Introduction

This specification defines the architecture and programming interface used by ScriptPacks within the Aksara Nusantara platform.

A ScriptPack is an independent software package that encapsulates all resources required to support a specific writing system.

The objective of this specification is to ensure that all ScriptPacks:

* are portable;
* are independently maintainable;
* can be loaded dynamically;
* remain compatible with future versions of the platform.

This document serves as the normative reference for both the Core Engine and ScriptPack developers.

Whenever implementation conflicts with this specification, this specification SHALL be considered authoritative.

---

# 2. Scope

This specification defines:

* ScriptPack architecture;
* directory structure;
* metadata format;
* loading mechanism;
* validation requirements;
* Core Engine interaction;
* character repository model;
* transliteration support;
* audio support;
* compatibility requirements.

This specification does **not** define:

* graphical user interface behavior;
* quiz implementation;
* educational content;
* application-specific workflows.

Those subjects are intentionally left to higher application layers.

---

# 3. Terminology

The following terminology is used throughout this specification.

| Term                 | Definition                                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| Core Engine          | Platform component responsible for discovering, validating, loading, and managing ScriptPacks.              |
| ScriptPack           | Independent package implementing support for a writing system.                                              |
| Metadata             | Information describing a ScriptPack, loaded from `manifest.json`.                                           |
| Character Repository | Collection of character definitions contained within a ScriptPack.                                          |
| Manifest             | JSON file describing the ScriptPack.                                                                        |
| Entry Point          | Python module used to instantiate the ScriptPack implementation.                                            |
| Identifier           | Unique identifier of a ScriptPack.                                                                          |
| Asset                | Any non-Python resource required by a ScriptPack, including images, audio, fonts, or character definitions. |

Unless otherwise stated, these terms SHALL carry the meanings defined in this section.

---

# 4. Conformance

A ScriptPack conforms to this specification if it satisfies all mandatory requirements defined in this document.

Mandatory requirements are indicated by the keyword **SHALL**.

Recommended behavior is indicated by **SHOULD**.

Optional behavior is indicated by **MAY**.

Prohibited behavior is indicated by **MUST NOT**.

A conforming implementation SHALL remain compatible with the Core Engine APIs defined by this specification.

---

# 5. Design Principles

The ScriptPack architecture is based on the following principles.

## 5.1 Separation of Concerns

The Core Engine SHALL contain only platform functionality.

Writing-system-specific behavior SHALL reside entirely within ScriptPacks.

---

## 5.2 Modularity

Each ScriptPack SHALL be self-contained.

No ScriptPack SHALL depend on the internal implementation of another ScriptPack.

---

## 5.3 Extensibility

New writing systems SHOULD be introduced by creating new ScriptPacks.

The Core Engine SHOULD require no modification when supporting additional writing systems.

---

## 5.4 Maintainability

The architecture SHALL prioritize readability and maintainability over implementation complexity.

Each component SHOULD have a single clearly defined responsibility.

---

## 5.5 Specification-Driven Development

Major implementations SHALL be based on approved technical specifications.

Changes to platform behavior SHOULD be reflected in both implementation and documentation.

Documentation is considered part of the implementation.

---

## 5.6 Forward Compatibility

The architecture SHOULD support future extensions without breaking existing ScriptPacks whenever practical.

Backward compatibility SHOULD be preserved across minor specification revisions whenever possible.

---

# 6. ScriptPack Architecture

## 6.1 Overview

A ScriptPack is the fundamental extension mechanism of the Aksara Nusantara platform.

Each ScriptPack encapsulates everything required to support a single writing system, including:

* metadata;
* implementation logic;
* character repository;
* assets;
* transliteration resources;
* optional audio resources.

A ScriptPack SHALL be deployable independently of other ScriptPacks.

---

## 6.2 Architectural Principles

The ScriptPack architecture follows these principles.

### Independence

A ScriptPack SHALL operate independently from all other ScriptPacks.

A ScriptPack MUST NOT directly import or depend on another ScriptPack.

---

### Encapsulation

All writing-system-specific resources SHALL reside inside the ScriptPack directory.

The Core Engine SHALL treat ScriptPacks as isolated modules.

---

### Discoverability

The Core Engine SHALL discover ScriptPacks dynamically by scanning the configured ScriptPack directory.

No ScriptPack SHALL require manual registration.

---

### Replaceability

A ScriptPack MAY be upgraded, removed, or replaced without requiring modifications to the Core Engine.

---

### Extensibility

Future ScriptPack capabilities SHALL be introduced without breaking existing implementations whenever practical.

---

# 7. ScriptPack Directory Layout

A conforming ScriptPack SHALL follow the directory structure defined below.

```text
scriptpacks/

    <identifier>/

        manifest.json

        script.py

        assets/

            characters/

            images/

            audio/

            fonts/
```

Additional directories MAY be introduced provided they do not conflict with reserved names defined by this specification.

---

## 7.1 Required Files

Every ScriptPack SHALL contain the following files.

| File          | Required | Description            |
| ------------- | -------- | ---------------------- |
| manifest.json | Yes      | ScriptPack metadata    |
| script.py     | Yes      | ScriptPack entry point |

---

## 7.2 Required Directories

The following directory SHALL exist.

| Directory | Purpose                            |
| --------- | ---------------------------------- |
| assets    | Container for ScriptPack resources |

Subdirectories inside `assets` MAY be omitted when unused.

---

## 7.3 Reserved Directories

The following names are reserved by this specification.

```text
assets/

characters/

images/

audio/

fonts/
```

Future versions of this specification MAY introduce additional reserved directories.

---

# 8. Manifest

## 8.1 Overview

Every ScriptPack SHALL provide a manifest named:

```text
manifest.json
```

The manifest contains metadata required by the Core Engine before the ScriptPack is imported.

---

## 8.2 Required Fields

The following fields are mandatory.

| Field       | Type   | Description                  |
| ----------- | ------ | ---------------------------- |
| identifier  | string | Unique ScriptPack identifier |
| name        | string | Human-readable name          |
| version     | string | ScriptPack version           |
| author      | string | ScriptPack author            |
| entry_point | string | Python entry module          |

---

## 8.3 Optional Fields

The following metadata fields are optional.

| Field          | Purpose                         |
| -------------- | ------------------------------- |
| description    | Human-readable description      |
| specification  | Supported specification version |
| language       | ISO language identifier         |
| writing_system | Writing system name             |
| unicode_blocks | Supported Unicode blocks        |
| license        | Distribution license            |

Unknown fields SHOULD be ignored by the Core Engine.

---

## 8.4 Identifier Rules

The `identifier` field SHALL satisfy the following requirements.

* unique within the ScriptPack directory;
* lowercase;
* ASCII letters, digits, and underscore only;
* immutable after public release whenever practical.

Example:

```text
javanese

balinese

rejang
```

---

## 8.5 Entry Point

The `entry_point` field specifies the Python module used to instantiate the ScriptPack.

Example:

```json
"entry_point": "script.py"
```

The referenced file SHALL exist.

---

# 9. Metadata

## 9.1 Purpose

Metadata describes a ScriptPack before it is instantiated.

Metadata SHALL originate from `manifest.json`.

The Core Engine SHALL load metadata before importing the ScriptPack module.

---

## 9.2 Metadata Ownership

Metadata is owned by the Core Engine.

The Core Engine SHALL provide metadata to the ScriptPack implementation during loading.

ScriptPack implementations SHOULD treat metadata as read-only.

---

## 9.3 Metadata Availability

After successful loading, metadata SHALL be available to the ScriptPack implementation through the `metadata` property defined by the BaseScriptPack interface.

ScriptPack implementations MUST NOT attempt to reload or duplicate manifest parsing.

---

# 10. Versioning and Compatibility

## 10.1 Specification Version

A ScriptPack MAY declare the specification version it targets.

Example:

```json
"specification": "1.0"
```

---

## 10.2 ScriptPack Version

Each ScriptPack SHALL define its own version.

Example:

```json
"version": "1.0.0"
```

Semantic Versioning is RECOMMENDED.

---

## 10.3 Compatibility

The Core Engine SHOULD reject ScriptPacks declaring incompatible specification versions.

Future versions MAY introduce compatibility negotiation.

---

## 10.4 Forward Compatibility

Unknown optional manifest fields SHALL be ignored unless explicitly reserved by future revisions of this specification.

---

# 11. BaseScriptPack Interface

## 11.1 Purpose

`BaseScriptPack` defines the minimum interface that every ScriptPack SHALL implement.

The Core Engine communicates exclusively through this interface.

Implementations MUST inherit from `BaseScriptPack`.

---

## 11.2 Responsibilities

A ScriptPack implementation SHALL:

* expose metadata supplied by the Core Engine;
* provide character definitions;
* encapsulate writing-system-specific behavior.

A ScriptPack MUST NOT:

* load its own manifest;
* modify Core Engine state;
* access other ScriptPacks directly.

---

## 11.3 Metadata

The Core Engine SHALL inject metadata after a ScriptPack instance has been created.

Metadata SHALL originate from `manifest.json`.

The `metadata` property SHALL be treated as read-only by ScriptPack implementations.

---

## 11.4 Character Repository

Every ScriptPack SHALL provide access to its character repository.

The minimum required interface is:

```python
@property
def metadata(self) -> dict[str, Any]:
    ...

def get_characters(self) -> list[Character]:
    ...
```

Future versions MAY define additional optional interfaces.

---

# 12. Script Registry

## 12.1 Purpose

The Script Registry maintains all successfully loaded ScriptPacks.

The registry acts as the single source of truth for loaded ScriptPack instances.

---

## 12.2 Registration

Only validated ScriptPacks SHALL be registered.

Registration SHALL occur after:

1. validation;
2. successful module import;
3. successful instance creation.

---

## 12.3 Unique Identifier

Each ScriptPack SHALL be registered using its metadata identifier.

Duplicate identifiers SHALL be rejected.

Attempting to register an existing identifier SHALL raise a `RegistryError`.

---

## 12.4 Registry Services

A conforming registry SHALL support the following operations.

| Operation    | Purpose                     |
| ------------ | --------------------------- |
| register()   | Register a ScriptPack       |
| unregister() | Remove a ScriptPack         |
| get()        | Retrieve a ScriptPack       |
| list()       | List registered ScriptPacks |
| clear()      | Remove all registrations    |

Additional convenience methods MAY be introduced in future revisions.

---

# 13. Script Loader

## 13.1 Purpose

The Script Loader is responsible for creating ScriptPack instances.

The loader SHALL perform module import only after successful validation.

---

## 13.2 Loading Sequence

The loading process SHALL follow the sequence below.

```text
ScriptPack Directory

↓

Load manifest.json

↓

Import entry module

↓

Instantiate BaseScriptPack

↓

Inject metadata

↓

Return instance
```

---

## 13.3 Manifest Loading

The loader SHALL read metadata from `manifest.json`.

Manifest parsing SHALL occur exactly once during the loading process.

---

## 13.4 Module Import

The module specified by `entry_point` SHALL be imported dynamically.

Import failures SHALL result in a `LoaderError`.

---

## 13.5 Instance Creation

Exactly one concrete implementation of `BaseScriptPack` SHALL be instantiated.

Failure to instantiate SHALL result in a `LoaderError`.

---

## 13.6 Metadata Injection

After instance creation, the loader SHALL inject metadata into the ScriptPack.

ScriptPack implementations SHALL NOT be responsible for loading or parsing the manifest.

---

# 14. Script Validation

## 14.1 Purpose

Validation ensures that a ScriptPack conforms to this specification before loading.

Validation SHALL occur before any module import.

---

## 14.2 Validation Scope

Validation SHALL include:

* directory structure;
* required files;
* manifest format;
* required metadata fields;
* entry point existence.

Additional validation MAY be introduced by future Core Engine versions.

---

## 14.3 Required Manifest Fields

The validator SHALL verify the following mandatory fields.

| Field       |
| ----------- |
| identifier  |
| name        |
| version     |
| author      |
| entry_point |

Missing required fields SHALL result in a `ValidationError`.

---

## 14.4 Entry Point Validation

The validator SHALL verify that the file referenced by `entry_point` exists.

Missing files SHALL prevent ScriptPack loading.

---

## 14.5 Validation Failures

Validation failures SHALL stop the loading process immediately.

The Core Engine MUST NOT attempt to import invalid ScriptPacks.

---

# 15. Core Engine API

## 15.1 Purpose

The Core Engine coordinates all ScriptPack lifecycle operations.

It is responsible for:

* discovery;
* validation;
* loading;
* registration.

The Core Engine SHALL NOT contain writing-system-specific logic.

---

## 15.2 Initialization Sequence

Initialization SHALL follow the sequence below.

```text
Discover ScriptPacks

↓

Validate

↓

Load

↓

Register

↓

Ready
```

---

## 15.3 Discovery

The Core Engine SHALL discover candidate ScriptPacks by scanning the configured ScriptPack directory.

Discovery SHALL ignore non-directory entries.

---

## 15.4 Public Services

A conforming Core Engine SHALL provide:

| Service      | Purpose                           |
| ------------ | --------------------------------- |
| initialize() | Load all ScriptPacks              |
| list()       | List loaded ScriptPacks           |
| get()        | Retrieve ScriptPack by identifier |

Future revisions MAY extend the public API while preserving backward compatibility.

---

# 16. Character Model

## 16.1 Purpose

The Character Model defines the minimum information required to represent a writing-system character.

Character definitions SHALL remain independent from application-specific logic.

The Character Model serves as the canonical representation of writing-system data exchanged between ScriptPacks and the Core Engine.

---

## 16.2 Character Repository

Character definitions SHALL be provided by the ScriptPack.

The Core Engine SHALL treat the repository as read-only.

A ScriptPack MAY organize character data using one or more resource files.

The storage format is implementation-defined, provided it can be exposed through the BaseScriptPack interface.

The Foundation Reference ScriptPacks use JSON as the canonical storage format for character repositories.

Alternative storage formats MAY be used by third-party ScriptPacks provided they remain compatible with the BaseScriptPack interface.

---

## 16.3 Minimum Character Attributes

Each character SHALL provide the minimum attributes defined below.

Additional attributes MAY be introduced by individual ScriptPacks provided they do not break compatibility with this Character Model.

| Attribute   | Required | Description                         |
| ------------|----------|-------------------------------------|
| id          | Yes      | Unique character identifier         |
| name        | Yes      | Human-readable character name       |
| glyph       | Yes      | Native script character             |
| latin       | Yes      | Latin transliteration               |
| unicode     | Yes      | Unicode code point                  |
| description | No       | Human-readable description          |

Character classification SHALL be determined by the repository in which the character is stored (for example, `nglegena.json`, `sandhangan.json`, or `pasangan.json`).

Therefore, character definitions SHALL NOT include a `category` attribute.

Future revisions MAY extend this model while preserving backward compatibility.

---

# 17. Transliteration

## 17.1 Purpose

A ScriptPack MAY provide transliteration support.

The transliteration algorithm is writing-system specific and SHALL remain the responsibility of the ScriptPack.

---

## 17.2 Responsibilities

The Core Engine SHALL NOT implement transliteration rules.

The Core Engine SHALL provide only the infrastructure required to access ScriptPack functionality.

---

## 17.3 Future Extensions

Future versions MAY define a standardized transliteration interface.

---

# 18. Audio Support

## 18.1 Purpose

ScriptPacks MAY provide pronunciation audio.

Audio support is optional.

---

## 18.2 Audio Assets

Audio resources SHOULD be stored within:

```text id="c8ijoe"
assets/audio/
```

The file format is implementation-defined.

---

## 18.3 Missing Audio

The absence of audio SHALL NOT invalidate a ScriptPack.

Applications SHOULD degrade gracefully when audio resources are unavailable.

---

# 19. Error Handling

## 19.1 Purpose

Errors SHALL be reported through well-defined exception types.

The Core Engine SHALL avoid exposing low-level implementation exceptions whenever practical.

---

## 19.2 Exception Hierarchy

The Foundation implementation defines the following exception hierarchy.

| Exception       | Purpose              |
| --------------- | -------------------- |
| CoreEngineError | Base exception       |
| ValidationError | Validation failures  |
| LoaderError     | Loading failures     |
| RegistryError   | Registry failures    |
| EngineError     | Core Engine failures |

Future revisions MAY extend this hierarchy.

---

## 19.3 Error Propagation

Validation failures SHALL prevent loading.

Loading failures SHALL prevent registration.

Registry failures SHALL prevent duplicate registrations.

The Core Engine SHALL fail fast whenever integrity cannot be guaranteed.

---

# 20. Security Considerations

## 20.1 Trust Model

ScriptPacks execute Python code.

Applications SHOULD load ScriptPacks only from trusted sources.

---

## 20.2 Validation

Validation improves structural integrity but SHALL NOT be considered a security mechanism.

Applications requiring stronger security SHOULD implement additional verification.

---

## 20.3 Future Security

Future versions MAY introduce:

* digital signatures;
* trusted publishers;
* package verification;
* integrity checks.

---

# 21. Future Compatibility

The ScriptPack architecture is designed to evolve without requiring major Core Engine redesign.

Future revisions MAY introduce:

* additional metadata fields;
* optional interfaces;
* plugin capabilities;
* marketplace integration;
* cloud synchronization;
* package signing;
* dependency management;
* localization support.

Whenever practical, backward compatibility SHOULD be preserved.

---

# Appendix A — Manifest Example

```json id="u0wb3x"
{
    "identifier": "javanese",
    "name": "Javanese Script",
    "description": "Official Javanese ScriptPack.",
    "version": "1.0.0",
    "specification": "1.0",
    "author": "Aksara Nusantara Project",
    "license": "MIT",
    "entry_point": "script.py",
    "language": "jv",
    "writing_system": "Hanacaraka",
    "unicode_blocks": [
        "Javanese"
    ]
}
```

---

# Appendix B — Directory Layout Example

```text id="4g5ttd"
scriptpacks/

    javanese/

        manifest.json

        script.py

        assets/

            characters/

            images/

            audio/

            fonts/
```

---

# Appendix C — Glossary

| Term                 | Meaning                                               |
| -------------------- | ----------------------------------------------------- |
| Core Engine          | Platform runtime responsible for ScriptPack lifecycle |
| ScriptPack           | Writing-system extension package                      |
| Metadata             | Manifest information owned by the Core Engine         |
| Character Repository | Script-defined character collection                   |
| Entry Point          | Python module used to instantiate a ScriptPack        |

---

# Appendix D — Core Engine Lifecycle

```text id="xw31o7"
ScriptPack Directory

↓

Validator

↓

Loader

↓

BaseScriptPack

↓

Registry

↓

Core Engine

↓

Application
```

---

# Appendix E — Foundation Reference Implementation

| Component                     | Status |
| ----------------------------- | ------ |
| BaseScriptPack                | ✅      |
| Registry                      | ✅      |
| Loader                        | ✅      |
| Validator                     | ✅      |
| Core Engine                   | ✅      |
| Javanese Reference ScriptPack | ✅      |
| Integration Test              | ✅ PASS |

---

# End of Specification

This document defines the Foundation v1.0 ScriptPack architecture for the Aksara Nusantara platform.

Future revisions SHALL preserve backward compatibility whenever practical while allowing the platform to evolve.

This specification serves as the normative reference for all Foundation-compliant ScriptPack implementations.
