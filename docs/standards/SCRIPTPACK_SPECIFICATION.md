# AN-STD-001



# ScriptPack Specification



---



Document ID : AN-STD-001



Title : ScriptPack Specification



Version : 0.2.0-draft



Status : Draft



Owner : Aksara Nusantara Project



Created : 2026-07-20



Last Updated : 2026-07-20



Related Documents



- PROJECT_WORKFLOW.md

- PROJECT_PRINCIPLES.md

- CORE_ARCHITECTURE.md



---



# Abstract



This document defines the official specification for ScriptPack packages used by the Aksara Nusantara Core Engine.



The purpose of this specification is to establish a stable, extensible, and implementation-independent contract between the Core Engine and every ScriptPack.



This document serves as the canonical reference for all ScriptPack implementations.



Whenever implementation and specification differ, this specification takes precedence.



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



9. Script Information



10. Versioning and Compatibility



11. BaseScriptPack Interface



12. Script Registry



13. Script Loader



14. Script Validation



15. Asset Management



16. Character Model



17. Transliteration



18. Audio Support



19. Error Handling



20. Security Considerations



21. Future Compatibility



Appendix A — Manifest Example



Appendix B — Directory Layout Example



Appendix C — Glossary



---



# 1. Introduction



## 1.1 Purpose



The ScriptPack system provides a standardized mechanism for representing writing systems supported by the Aksara Nusantara ecosystem.



Rather than embedding script-specific logic into the Core Engine, each writing system SHALL be distributed as an independent ScriptPack.



This architecture allows the Core Engine to remain generic while enabling support for additional writing systems without modification.



## 1.2 Goals



The ScriptPack architecture has the following goals:



- Separate Core Engine from script-specific implementation.

- Support multiple writing systems through a common interface.

- Enable independent development of ScriptPacks.

- Encourage community contributions.

- Preserve backward compatibility whenever possible.

- Provide a stable SDK for future extensions.



## 1.3 Non-Goals



This specification does not define:



- graphical user interface

- learning methodology

- quiz implementation

- application workflow

- marketplace protocol



These subjects are covered by separate specifications.



---



# 2. Scope



This specification defines:



- ScriptPack package structure

- Manifest format

- Metadata model

- Versioning rules

- BaseScriptPack interface

- Registry behavior

- Loader behavior

- Validation requirements

- Asset organization

- Character model

- Transliteration contract

- Audio integration



This specification does not mandate any specific programming language.



Although the reference implementation is written in Python, alternative implementations MAY exist provided they conform to this specification.



---



# 3. Terminology



The following terms are used throughout this document.



Core Engine



The runtime responsible for discovering, validating, loading, and managing ScriptPacks.



BaseScriptPack

An abstract interface implemented by every ScriptPack implementation.

ScriptPack

A package representing one writing system, including metadata, assets, and one implementation of BaseScriptPack.

ScriptPack Implementation

The concrete class implementing BaseScriptPack.



Manifest



The primary metadata file describing a ScriptPack.



Registry



The component responsible for maintaining available ScriptPacks.



Loader



The component responsible for loading ScriptPacks into memory.



Validator



The component responsible for verifying ScriptPack conformance.



Character Model



The structured representation of characters, symbols, and related metadata belonging to a writing system.



Conformance



The degree to which an implementation satisfies this specification.



---



# 4. Conformance



An implementation conforms to AN-STD-001 if and only if all mandatory requirements defined by this specification are satisfied.



The key words:



MUST



MUST NOT



SHOULD



SHOULD NOT



MAY



are to be interpreted as described in RFC 2119.



Whenever a conflict exists between implementation and this specification, the specification SHALL take precedence.



---



# 5. Design Principles

## 5.1 Purpose

This section defines the fundamental principles governing the design of the ScriptPack ecosystem.

These principles serve as the architectural foundation for all current and future ScriptPack implementations.

Whenever implementation details are unclear, these principles SHALL take precedence.

---

## 5.2 Core Engine Independence

The Core Engine MUST remain independent from any specific writing system.

The Core Engine SHALL NOT contain logic that is specific to a particular script, language, alphabet, or orthography.

All script-specific behavior MUST be implemented by the corresponding ScriptPack.

### Rationale

Keeping the Core Engine script-agnostic ensures long-term maintainability and enables support for additional writing systems without modifying the engine itself.

---

## 5.3 Single Responsibility

Each ScriptPack SHOULD represent one writing system.

A ScriptPack SHOULD NOT combine multiple unrelated writing systems into a single package.

If multiple writing systems are closely related but maintain distinct character inventories or writing rules, separate ScriptPacks SHOULD be created.

### Examples

Recommended:

- Javanese ScriptPack
- Balinese ScriptPack
- Hebrew ScriptPack
- Greek ScriptPack

Not recommended:

- Asian ScriptPack
- Bible ScriptPack
- Ancient Languages ScriptPack

---

## 5.4 Separation of Responsibilities

The responsibilities of the Core Engine and ScriptPack SHALL remain clearly separated.

Core Engine responsibilities include:

- discovery
- loading
- validation
- lifecycle management
- registry management

ScriptPack responsibilities include:

- character definitions
- transliteration rules
- writing system metadata
- audio resources
- educational assets

A ScriptPack MUST NOT modify Core Engine behavior.

---

## 5.5 Specification First

All implementations MUST follow the written specification.

Whenever implementation differs from this specification, the specification SHALL take precedence.

Developers SHOULD update the specification before introducing architectural changes.

### Rationale

A stable specification provides a common reference for contributors and prevents inconsistent implementations.

---

## 5.6 Extensibility

The architecture SHOULD support future writing systems without requiring changes to existing ScriptPacks.

Adding a new ScriptPack SHOULD require only:

- implementing the required interfaces;
- providing a valid manifest;
- supplying the required assets.

No modifications to existing ScriptPacks SHOULD be necessary.

---

## 5.7 Backward Compatibility

Backward compatibility SHOULD be preserved whenever practical.

Changes that break compatibility MUST be accompanied by a version increment as defined in Section 10.

Whenever compatibility cannot be maintained, migration guidance SHOULD be provided.

---

## 5.8 Open Architecture

The ScriptPack ecosystem is designed to encourage community contributions.

Any contributor MAY develop a new ScriptPack provided that it conforms to this specification.

Conformance SHALL be determined through validation rather than authorship.

---

## 5.9 Educational Focus

The primary objective of the ScriptPack ecosystem is education, preservation, and exploration of writing systems.

Commercial or proprietary extensions MAY exist, provided they do not violate this specification or restrict interoperability with conforming ScriptPacks.

---

## 5.10 Future Evolution

This specification is expected to evolve over time.

Future revisions SHOULD extend the specification while minimizing disruption to existing ScriptPacks.

Deprecated features SHOULD remain documented until officially removed in a major specification revision.



---



# 6. ScriptPack Architecture

## 6.1 Overview

The ScriptPack architecture is designed around a modular and extensible plugin model.

Each ScriptPack is a self-contained package that describes a single writing system and exposes a standardized interface to the Aksara Nusantara Core Engine.

The Core Engine is responsible for discovering, validating, loading, and managing ScriptPacks, while each ScriptPack is responsible for providing script-specific data and behavior.

---

## 6.2 High-Level Architecture

The ScriptPack ecosystem consists of three primary components:

- Core Engine
- ScriptPack
- Application Layer

The relationship between these components is illustrated below.

```text
+------------------------------------------------------+
|                  Application Layer                   |
|  (Desktop App, CLI, Future Mobile App, etc.)         |
+---------------------------?--------------------------+
                             
                              API
                             
+------------------------------------------------------+
|                    Core Engine                       |
|------------------------------------------------------|
| Script Registry                                      |
| Script Loader                                        |
| Validator                                            |
| Asset Manager                                        |
| BaseScriptPack Interface                             |
+---------------------------?--------------------------+
                             
                             
                loads and validates
                             
+------------------------------------------------------+
|                    ScriptPack                        |
|------------------------------------------------------|
| manifest.json                                        |
| character data                                       |
| transliteration rules                                |
| assets                                               |
| audio                                                |
| metadata                                             |
+------------------------------------------------------+
```

---

## 6.3 Component Responsibilities

### Application Layer

The Application Layer provides the user interface and learning experience.

Applications SHOULD interact only with the Core Engine.

Applications SHOULD NOT access ScriptPack internals directly.

---

### Core Engine

The Core Engine provides the runtime environment for ScriptPacks.

Its responsibilities include:

- discovering available ScriptPacks;
- validating package integrity;
- loading compatible ScriptPacks;
- exposing a unified API;
- managing ScriptPack lifecycle.

The Core Engine SHALL remain independent of any specific writing system.

---

### ScriptPack

A ScriptPack contains all resources necessary to describe a writing system.

Typical contents include:

- metadata;
- character definitions;
- transliteration rules;
- pronunciation data;
- educational assets.

A ScriptPack SHALL NOT contain application-specific logic.

---

## 6.4 Communication Model

Applications communicate with ScriptPacks indirectly through the Core Engine.

The following communication path SHALL be used.

```text
Application
       
      ?
Core Engine
       
      ?
Script Registry
       
      ?
ScriptPack
```

Direct communication between the Application Layer and ScriptPack SHOULD be avoided.

---

## 6.5 Lifecycle

The lifecycle of a ScriptPack consists of the following stages.

1. Discovery
2. Validation
3. Registration
4. Loading
5. Initialization
6. Runtime Usage
7. Unloading

Each stage SHALL complete successfully before the next stage begins.

---

## 6.6 Design Benefits

The ScriptPack architecture provides the following benefits.

- Separation of concerns.
- Independent development.
- Easier testing.
- Future extensibility.
- Reduced maintenance cost.
- Improved portability.
- Simplified community contribution.



---



# 7. ScriptPack Directory Layout

## 7.1 Purpose

This section defines the recommended directory structure for a ScriptPack.

A consistent directory layout improves discoverability, simplifies validation, and provides a predictable development experience for both users and contributors.

Unless otherwise specified, directory names are case-sensitive.

---

## 7.2 Standard Directory Layout

A ScriptPack SHOULD follow the directory structure shown below.

```text
scriptpack/

+-- manifest.json
+-- README.md
+-- LICENSE
 
+-- characters/
    +-- characters.json
    +-- groups.json
 
+-- transliteration/
    +-- rules.json
 
+-- assets/
    +-- images/
    +-- audio/
    +-- fonts/
 
+-- examples/
 
+-- docs/
```

The above layout represents the recommended organization for ScriptPack packages.

Additional files and directories MAY be included provided they do not interfere with the required structure.

---

## 7.3 Required Files

Every ScriptPack MUST contain the following files.

| File | Required |
|------|----------|
| manifest.json | YES |
| README.md | YES |
| LICENSE | YES |

If any required file is missing, the ScriptPack SHALL fail validation.

---

## 7.4 Recommended Directories

The following directories are recommended.

| Directory | Purpose |
|-----------|---------|
| characters | Character definitions |
| transliteration | Transliteration rules |
| assets | Fonts, images, and audio |
| docs | Documentation |
| examples | Sample resources |

These directories SHOULD be present whenever applicable.

---

## 7.5 Optional Directories

A ScriptPack MAY define additional directories for its own internal organization.

Examples include:

- tests/
- references/
- bibliography/
- datasets/

The Core Engine SHALL ignore unknown directories unless explicitly defined by future specifications.

---

## 7.6 Reserved Names

The following names are reserved by this specification.

- manifest.json
- characters
- transliteration
- assets
- docs

Future versions of this specification MAY reserve additional names.

---

## 7.7 Package Root

The root directory of a ScriptPack SHALL contain exactly one manifest file.

Nested ScriptPacks are not permitted.

Each package represents one logical ScriptPack.

---

## 7.8 Future Compatibility

Future versions of this specification MAY introduce additional directories.

Implementations SHOULD ignore directories that are not recognized unless validation rules explicitly state otherwise.

This approach allows the directory layout to evolve without breaking existing ScriptPacks.



---



# 8. Manifest

## 8.1 Purpose

The manifest is the primary entry point of a ScriptPack.

Every ScriptPack MUST provide exactly one manifest file.

The manifest contains metadata, compatibility information, and implementation references required by the Core Engine.

Before loading any ScriptPack implementation, the Core Engine SHALL first validate and process the manifest.

This process is referred to as Manifest First Loading.

---

## 8.2 File Name

The manifest file SHALL be named:

```text
manifest.json
```

The file SHALL be located in the root directory of the ScriptPack package.

Example:

```text
<package-root>/

+-- manifest.json
+-- README.md
+-- LICENSE
+-- ...
```

---

## 8.3 File Format

The manifest SHALL use JSON format.

The manifest SHALL be encoded using UTF-8.

The use of UTF-8 with BOM is NOT RECOMMENDED.

Implementations SHOULD reject malformed JSON documents.

---

## 8.4 Manifest Structure

A manifest SHALL contain a single JSON object.

Example:

```json
{
    "script_id": "jawa",
    "name": "Javanese Script",
    "version": "1.0.0",
    "api_version": "1.0",
    "implementation": "implementation.py"
}
```

Additional fields MAY be included.

Unknown fields SHALL be ignored unless explicitly defined by future specifications.

---

## 8.5 Required Fields

The following fields are mandatory.

| Field | Required |
|---------|----------|
| script_id | YES |
| name | YES |
| version | YES |
| api_version | YES |
| implementation | YES |

A manifest missing any required field SHALL fail validation.

---

## 8.6 Field Constraints

### script_id

The script_id uniquely identifies a ScriptPack.

Requirements:

- MUST be unique.
- MUST be lowercase.
- MUST use ASCII letters, digits, and hyphens only.
- MUST NOT contain spaces.

Examples:

Valid:

```text
jawa
balinese
hebrew
greek
arabic
```

Invalid:

```text
Aksara Jawa
Hebrew Script
Ancient Greek
```

---

### name

Human-readable name of the ScriptPack.

Examples:

```text
Javanese Script
Hebrew Script
Greek Script
```

---

### version

Version number of the ScriptPack.

The version SHALL follow Semantic Versioning.

Examples:

```text
1.0.0
1.2.3
2.0.0
```

---

### api_version

Version of the ScriptPack API supported by the package.

This field is used for compatibility checking.

Examples:

```text
1.0
1.1
2.0
```

---

### implementation

Relative path to the ScriptPack implementation.

Examples:

```text
implementation.py

src/implementation.py

core/scriptpack.py
```

The referenced file MUST exist.

---

## 8.7 Validation Rules

The Core Engine SHALL validate the manifest before loading any implementation.

Validation SHALL include:

- file existence;
- JSON validity;
- required fields;
- field constraints;
- compatibility checks.

If validation fails, the ScriptPack SHALL NOT be loaded.

---

## 8.8 Unknown Fields

Unknown fields SHALL NOT cause validation failure.

This requirement supports future extensions of the specification.

Example:

```json
{
    "script_id": "jawa",
    "name": "Javanese Script",
    "version": "1.0.0",
    "api_version": "1.0",
    "implementation": "implementation.py",
    "future_field": "reserved"
}
```

The Core Engine SHOULD ignore the field if it is not recognized.

---

## 8.9 Manifest First Loading

The Core Engine SHALL process ScriptPacks using the following sequence.

```text
Locate Package

?

Locate manifest.json

?

Validate Manifest

?

Compatibility Check

?

Locate Implementation

?

Load Implementation

?

Initialize Runtime
```

No implementation SHALL be loaded before manifest validation succeeds.

---

## 8.10 Future Extensions

Future versions of this specification MAY define additional manifest fields.

Implementations SHOULD remain forward-compatible by ignoring fields they do not recognize.

This approach minimizes compatibility issues across specification revisions.



---



# 9. Script Information

## 9.1 Purpose

This section defines the information describing a writing system represented by a ScriptPack.

Script information provides human-readable metadata that enables applications, users, and the Core Engine to identify and present ScriptPacks consistently.

Unlike the manifest, which is primarily intended for package discovery and loading, Script Information describes the writing system itself.

---

## 9.2 Scope

Script Information SHALL describe the writing system represented by the ScriptPack.

It SHALL NOT describe implementation details.

Examples of implementation details include:

- Python modules
- internal file names
- validation rules
- runtime configuration

---

## 9.3 Required Information

Every ScriptPack MUST provide the following information.

| Field | Description |
|--------|-------------|
| Name | Official writing system name |
| Native Name | Name written in its own script (if applicable) |
| ISO Code | ISO 15924 script code when available |
| Direction | Writing direction |
| Unicode Support | Unicode availability |

---

## 9.4 Writing Direction

The writing direction SHALL be one of the following values.

| Value | Description |
|--------|-------------|
| LTR | Left-to-Right |
| RTL | Right-to-Left |
| TTB | Top-to-Bottom |
| BTT | Bottom-to-Top |

Examples:

- Latin ? LTR
- Javanese ? LTR
- Greek ? LTR
- Hebrew ? RTL
- Arabic ? RTL

Future revisions MAY introduce additional writing directions.

---

## 9.5 Native Name

If the writing system has a native representation, it SHOULD be provided.

Examples:

| Writing System | Native Name |
|----------------|-------------|
| Javanese | ????? |
| Greek | ???????? |
| Hebrew | ????? |
| Arabic | ??????? |

If no native representation exists, this field MAY be omitted.

---

## 9.6 ISO Script Code

Whenever available, the ScriptPack SHOULD specify the ISO 15924 code.

Examples:

| Writing System | ISO 15924 |
|----------------|-----------|
| Latin | Latn |
| Javanese | Java |
| Greek | Grek |
| Hebrew | Hebr |
| Arabic | Arab |

If no ISO code exists, the field MAY be left empty.

---

## 9.7 Unicode Support

A ScriptPack SHOULD indicate whether the writing system is represented in Unicode.

Possible values include:

- Full
- Partial
- None

This information assists applications in determining rendering capabilities.

---

## 9.8 Informational Nature

The fields defined in this section are descriptive.

They SHALL NOT influence ScriptPack loading, validation, or compatibility checks.

Their primary purpose is to improve interoperability and user experience.



---



# 10. Versioning and Compatibility

## 10.1 Purpose

This section defines the versioning model and compatibility requirements for ScriptPacks and the Core Engine.

Consistent versioning enables predictable upgrades, reliable validation, and long-term ecosystem stability.

---

## 10.2 Version Types

The ScriptPack ecosystem defines two independent version numbers.

| Version | Purpose |
|---------|---------|
| ScriptPack Version | Version of the ScriptPack package |
| API Version | Version of the ScriptPack API implemented by the package |

These version numbers SHALL be managed independently.

---

## 10.3 ScriptPack Version

The ScriptPack Version identifies releases of an individual ScriptPack.

It SHALL follow Semantic Versioning.

Examples:

```text
1.0.0
1.2.0
1.2.3
2.0.0
```

A change to ScriptPack content does not necessarily require an API version change.

---

## 10.4 API Version

The API Version identifies the version of the ScriptPack interface implemented by the package.

The Core Engine SHALL use this version to determine compatibility.

Example:

```text
1.0
1.1
2.0
```

---

## 10.5 Compatibility Rules

A ScriptPack SHALL declare the API Version it implements.

The Core Engine SHALL reject ScriptPacks implementing unsupported API versions.

Compatibility SHALL be determined before loading any implementation.

---

## 10.6 Semantic Versioning

ScriptPack Version SHALL follow Semantic Versioning.

Version numbers use the format:

```text
MAJOR.MINOR.PATCH
```

Definitions:

- MAJOR   incompatible changes.
- MINOR   backward-compatible new functionality.
- PATCH   backward-compatible fixes.

---

## 10.7 API Evolution

Future revisions of the ScriptPack API SHOULD preserve backward compatibility whenever practical.

Breaking API changes SHALL require a new major API version.

---

## 10.8 Forward Compatibility

The Core Engine SHOULD ignore optional fields and extensions that are unknown but do not affect compatibility.

This requirement allows newer ScriptPacks to coexist with older Core Engine implementations whenever possible.

---

## 10.9 Validation Sequence

Compatibility validation SHALL occur after manifest validation and before implementation loading.

The recommended validation order is:

```text
Locate Package

?

Read Manifest

?

Validate Manifest

?

Check API Version

?

Load Implementation

?

Initialize ScriptPack
```

---

## 10.10 Compatibility Failure

If compatibility requirements are not satisfied, the Core Engine SHALL reject the ScriptPack.

Implementations SHOULD provide a meaningful error message indicating the reason for rejection.

The Core Engine SHALL continue processing other available ScriptPacks whenever possible.



---


# 11. BaseScriptPack Interface

## 11.1 Purpose

This section defines the minimum interface that every ScriptPack Implementation SHALL provide.

The BaseScriptPack interface establishes a consistent contract between ScriptPack Implementations and the Core Engine.

All ScriptPack Implementations MUST conform to this interface.

---

## 11.2 Abstract Interface

BaseScriptPack represents an abstract interface.

It SHALL NOT represent a concrete writing system.

Applications SHALL interact with ScriptPack Implementations through the Core Engine rather than directly.

---

## 11.3 Implementation Requirement

Every ScriptPack Implementation MUST inherit from BaseScriptPack.

A ScriptPack Implementation that does not inherit from BaseScriptPack SHALL fail validation.

---

## 11.4 Lifecycle Participation

Every ScriptPack Implementation SHALL participate in the ScriptPack lifecycle defined in Section 6.

Implementations SHALL support initialization and runtime usage.

Implementations MAY support unloading and cleanup operations.

---

## 11.5 Required Methods

Every ScriptPack Implementation MUST provide the following methods.

| Method | Required |
|---------|----------|
| get_script_information() | YES |
| get_characters() | YES |

Failure to implement any required method SHALL result in validation failure.

---

## 11.6 get_script_information()

This method returns the descriptive information defined in Section 9.

This information is intended for applications, user interfaces, and educational presentation.

The returned information SHALL NOT affect compatibility checks or loading decisions.

---

## 11.7 get_characters()

This method returns the character definitions provided by the ScriptPack.

Character definitions MAY include:

- base characters;
- diacritics;
- punctuation;
- numerals;
- grouping information.

Future versions of this specification MAY define additional character categories.

---

## 11.8 Optional Methods

Implementations MAY define additional methods.

Examples:

- get_audio()
- get_examples()
- get_fonts()
- get_transliteration_rules()

Optional methods SHALL NOT be required for compatibility unless defined by future specification revisions.

---

## 11.9 Runtime State

ScriptPack Implementations SHOULD minimize mutable runtime state whenever possible.

Implementations SHOULD behave consistently across repeated calls.

---

## 11.10 Engine Ownership

The Core Engine SHALL own the ScriptPack lifecycle.

ScriptPack Implementations SHALL NOT manage registration, discovery, validation, or loading of other ScriptPacks.

---

## 11.11 Future Evolution

Future versions of the specification MAY introduce additional required methods.

Such additions SHOULD preserve backward compatibility whenever practical.

Breaking interface changes SHALL require an API version increment.



---


# 12. Script Registry

## 12.1 Purpose

The Script Registry is responsible for maintaining information about all validated ScriptPacks.

Only ScriptPacks that successfully complete validation SHALL be registered.

The Registry provides a centralized view of available ScriptPacks and their current status.

Applications SHALL obtain ScriptPack information through the Core Engine rather than interacting with the Registry directly.

---

## 12.2 Responsibilities

The Script Registry SHALL be responsible for:

- maintaining manifest information;
- providing lookup services;
- tracking runtime loading status.

The Registry SHALL NOT load ScriptPack implementations.

Loading is the responsibility of the Script Loader.

---

## 12.3 Registry Entry

Each discovered ScriptPack SHALL be represented by one Registry Entry.

A Registry Entry SHOULD contain:

- package location;
- manifest information;
- validation result;
- compatibility status;
- loading status.

Future versions MAY define additional registry fields.

---

## 12.4 Registration Process

The registration process consists of the following steps.

1. Discover package.
2. Locate manifest.
3. Validate manifest.
4. Create Registry Entry.
5. Store Registry Entry.

Registration SHALL complete before implementation loading begins.

---

## 12.5 Lookup

The Registry SHALL support lookup using ScriptPack identifiers.

Lookup operations SHOULD be deterministic.

If multiple ScriptPacks declare the same identifier, the Registry SHALL reject all conflicting entries.

---

## 12.6 Registry State

The Registry SHALL maintain the following states for each ScriptPack.

| State | Description |
|--------|-------------|
| Discovered | Package found |
| Validated | Manifest validated |
| Compatible | API compatibility confirmed |
| Loaded | Implementation loaded |
| Failed | Registration or loading failed |

---

## 12.7 Duplicate Detection

Each ScriptPack identifier MUST be unique.

Duplicate identifiers SHALL result in registration failure.

The Core Engine SHOULD continue processing other ScriptPacks after detecting duplicates.

---

## 12.8 Read-Only Metadata

The Registry SHALL treat manifest information as read-only.

Runtime modifications to manifest data SHALL NOT be permitted.

---

## 12.9 Separation of Responsibilities

The Registry SHALL NOT:

- instantiate ScriptPack implementations;
- load assets;
- perform transliteration;
- manage application state.

These responsibilities belong to other Core Engine components.

---

## 12.10 Future Evolution

Future specification revisions MAY extend Registry capabilities.

Extensions SHOULD preserve backward compatibility whenever practical.



---


# 13. Script Loader

## 13.1 Purpose

The Script Loader is responsible for loading validated ScriptPack Implementations into the Core Engine.

The Loader SHALL only process ScriptPacks that have successfully completed manifest validation and compatibility checks.

The Loader SHALL NOT perform package discovery or manifest validation.

---

## 13.2 Responsibilities

The Script Loader SHALL be responsible for:

- locating the implementation module;
- importing the implementation module;
- locating the ScriptPack Implementation class;
- instantiating the ScriptPack Implementation;
- reporting loading results.

The Loader SHALL NOT modify manifest information.

---

## 13.3 Preconditions

Before loading begins, the following conditions SHALL be satisfied:

- the package has been discovered;
- the manifest has been validated;
- the ScriptPack is compatible with the Core Engine;
- the implementation module exists.

Failure to satisfy any precondition SHALL prevent loading.

---

## 13.4 Loading Sequence

The recommended loading sequence is:

```text
Registry Entry

↓

Read implementation information

↓

Import module

↓

Locate ScriptPack class

↓

Verify inheritance

↓

Instantiate ScriptPack

↓

Register runtime instance
```

---

## 13.5 Class Verification

The Loader SHALL verify that the discovered implementation class inherits from BaseScriptPack.

Classes that do not inherit from BaseScriptPack SHALL be rejected.

---

## 13.6 Runtime Instance

Each successfully loaded ScriptPack SHALL produce one runtime instance.

The Core Engine SHALL maintain ownership of runtime instances.

ScriptPack Implementations SHALL NOT instantiate other ScriptPacks.

---

## 13.7 Error Handling

Loading failures SHALL NOT terminate the Core Engine.

The Loader SHOULD continue processing remaining ScriptPacks whenever possible.

Errors SHOULD include:

- package identifier;
- failure stage;
- human-readable description.

---

## 13.8 Loading Status

The Loader SHALL report one of the following outcomes.

| Status | Description |
|--------|-------------|
| Loaded | Implementation successfully loaded |
| Failed | Loading failed |
| Skipped | Loading skipped due to validation failure |

---

## 13.9 Runtime Ownership

The Script Loader SHALL transfer ownership of successfully instantiated ScriptPacks to the Core Engine.

The Loader SHALL NOT manage runtime execution after initialization.

---

## 13.10 Separation of Responsibilities

The Script Loader SHALL NOT:

- discover packages;
- validate manifests;
- perform compatibility checks;
- manage registry entries;
- perform transliteration;
- manage user data.

These responsibilities belong to other Core Engine components.

---

## 13.11 Future Evolution

Future specification revisions MAY extend loading capabilities.

Such extensions SHOULD preserve backward compatibility whenever practical.



---


# 14. Script Validator

## 14.1 Purpose

The Script Validator is responsible for verifying that a ScriptPack conforms to this specification before it is loaded by the Core Engine.

Validation SHALL occur before any ScriptPack Implementation is imported or instantiated.

The Validator serves as the primary gatekeeper of the ScriptPack ecosystem.

---

## 14.2 Responsibilities

The Script Validator SHALL be responsible for:

- verifying package structure;
- locating the manifest;
- validating manifest syntax;
- validating required manifest fields;
- verifying API compatibility;
- reporting validation results.

The Validator SHALL NOT load ScriptPack implementations.

---

## 14.3 Validation Scope

Validation SHALL include, at minimum:

- package existence;
- required directory structure;
- manifest existence;
- manifest syntax;
- required fields;
- field constraints;
- API compatibility.

Future revisions MAY extend validation requirements.

---

## 14.4 Validation Sequence

The recommended validation sequence is:

Locate Package

↓

Verify Directory Structure

↓

Locate manifest.json

↓

Parse JSON

↓

Validate Required Fields

↓

Validate Field Constraints

↓

Check API Compatibility

↓

Validation Result

---

## 14.5 Validation Result

Validation SHALL produce one of the following outcomes.

| Result | Description |
|--------|-------------|
| Valid | The ScriptPack satisfies all mandatory requirements |
| Invalid | One or more validation checks failed |

Validation SHALL complete before registration begins.

---

## 14.6 Error Reporting

Validation failures SHOULD include:

- package identifier, if available;
- validation stage;
- descriptive error message.

Error reporting SHOULD assist developers in correcting invalid ScriptPacks.

---

## 14.7 Failure Handling

Failure to validate one ScriptPack SHALL NOT terminate validation of remaining ScriptPacks.

The Core Engine SHOULD continue validating all discovered ScriptPacks whenever possible.

---

## 14.8 Separation of Responsibilities

The Script Validator SHALL NOT:

- register ScriptPacks;
- load implementations;
- instantiate ScriptPack classes;
- perform transliteration;
- manage runtime instances.

These responsibilities belong to other Core Engine components.

---

## 14.9 Future Evolution

Future specification revisions MAY introduce additional validation rules.

Such additions SHOULD preserve backward compatibility whenever practical.



---



# 15. Core Engine API

## 15.1 Purpose

The Core Engine provides the primary interface between applications and the ScriptPack ecosystem.

Applications SHOULD interact with the Core Engine rather than directly accessing internal components such as the Validator, Registry, or Loader.

---

## 15.2 Responsibilities

The Core Engine SHALL be responsible for:

- coordinating the ScriptPack lifecycle;
- initializing internal components;
- exposing available ScriptPacks;
- providing access to loaded ScriptPack implementations;
- managing runtime ownership.

The Core Engine SHALL NOT implement writing-system-specific behavior.

---

## 15.3 Initialization

Initialization SHALL perform the following sequence:

1. Discover ScriptPack packages.
2. Validate discovered packages.
3. Register validated ScriptPacks.
4. Load compatible ScriptPack implementations.
5. Make loaded ScriptPacks available to applications.

Initialization SHOULD complete before user interaction begins.

---

## 15.4 Public API

Applications SHOULD access ScriptPacks using the Core Engine public interface.

Typical operations MAY include:

- initialize();
- get_available_scripts();
- get_script(identifier);
- get_loaded_scripts();

Future specification revisions MAY define additional API methods.

---

## 15.5 Ownership

The Core Engine SHALL own:

- Script Registry;
- Script Loader;
- Script Validator;
- runtime ScriptPack instances.

Applications SHALL NOT directly modify these components.

---

## 15.6 Error Handling

Initialization failures SHALL be reported through the Core Engine.

The Core Engine SHOULD continue operating whenever possible, even if one or more ScriptPacks fail validation or loading.

---

## 15.7 Separation of Responsibilities

The Core Engine SHALL coordinate internal components.

The Core Engine SHALL NOT duplicate responsibilities already assigned to:

- Script Validator;
- Script Registry;
- Script Loader;
- ScriptPack Implementations.

---

## 15.8 Future Evolution

Future versions of the specification MAY extend the public API.

Such extensions SHOULD preserve backward compatibility whenever practical.



---



