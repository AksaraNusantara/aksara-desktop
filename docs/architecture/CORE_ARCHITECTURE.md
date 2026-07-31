# 1. Introduction

## 1.1 Purpose

This document defines the architecture of the Aksara Nusantara Foundation.

The Foundation serves as the reusable runtime layer shared by every application within the Aksara Nusantara ecosystem. It establishes the architectural principles, runtime services, public interfaces, and execution model required to discover, validate, register, and expose ScriptPacks in a consistent and implementation-independent manner.

The purpose of this specification is to establish a stable architectural contract for Foundation development. It defines the responsibilities and interactions of the Core Engine and its supporting services while ensuring that all Foundation implementations remain consistent across applications and future platform expansions.

This specification is normative unless otherwise stated.

---

## 1.2 Scope

This specification applies exclusively to the Foundation Layer.

The Foundation Layer provides generic runtime services that are independent of any specific writing system, graphical user interface, or application implementation.

This specification defines:

- the Foundation architecture;
- the Core Engine;
- Foundation services;
- runtime lifecycle;
- ScriptPack discovery;
- ScriptPack validation;
- ScriptPack registration;
- public Foundation APIs;
- extension mechanisms;
- dependency rules between Foundation components.

This specification does not define:

- Application Layer architecture;
- graphical user interface behavior;
- ScriptPack internal implementation;
- ScriptPack asset organization;
- character data format;
- transliteration algorithms;
- audio implementation.

These topics are defined by their respective specifications.

---

## 1.3 Objectives

The objectives of the Foundation are:

- provide a reusable runtime shared by all Aksara Nusantara applications;
- establish a stable execution environment for ScriptPacks;
- isolate applications from ScriptPack implementation details;
- provide deterministic discovery and loading of ScriptPacks;
- ensure consistent validation before runtime registration;
- expose a simple and stable public API;
- minimize coupling between runtime components;
- support future expansion without requiring architectural redesign.

---

## 1.4 Audience

This specification is intended for:

- Foundation developers;
- ScriptPack developers;
- application developers;
- maintainers;
- architecture reviewers;
- contributors participating in Foundation development.

Readers are expected to be familiar with Python programming and the overall architecture of the Aksara Nusantara ecosystem.

---

## 1.5 Related Specifications

This document should be read together with the following specifications:

- APPLICATION_ARCHITECTURE.md
- SCRIPTPACK_INTERFACE_SPECIFICATION.md
- TRACEABILITY.md
- ENGINEERING_PRINCIPLES.md
- PROJECT_BLUEPRINT.md

Where conflicts exist, this specification takes precedence for all Foundation-related architectural decisions.

---

## 1.6 Terminology

The following terminology is used throughout this specification.

### Foundation

The reusable runtime layer responsible for managing ScriptPacks independently of any application.

### Core Engine

The orchestration component responsible for coordinating Foundation services and exposing the public Foundation API.

### Foundation Service

A component that performs a single runtime responsibility on behalf of the Core Engine.

Examples include:

- Loader
- Validator
- Registry

### ScriptPack

A self-contained implementation package that provides support for a specific writing system.

### Runtime

The operational state of the Foundation after initialization has completed successfully.

---

## 1.7 Conformance

The key words SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as described in RFC 2119.

All Foundation implementations claiming conformance with this specification SHALL satisfy every normative requirement defined herein.

---

## 1.8 Architectural Principles

The Foundation is designed according to the following principles.

### Small Core

The Foundation SHALL remain intentionally lightweight.

Writing-system knowledge SHALL reside inside ScriptPacks rather than within the Foundation itself.

### Separation of Responsibilities

Each Foundation component SHALL have exactly one primary responsibility.

No component SHALL duplicate the responsibility of another component.

### Explicit Dependencies

Dependencies between Foundation components SHALL follow a single directional flow.

Circular dependencies SHALL NOT exist.

### Contract-Based Architecture

Communication between the Foundation and ScriptPacks SHALL occur exclusively through the BaseScriptPack contract.

Applications SHALL NOT depend on concrete ScriptPack implementations.

### UI Independence

The Foundation SHALL NOT depend upon any graphical user interface framework.

The Foundation SHALL remain usable from desktop, command-line, automated testing, and future platforms without modification.

### Extensibility

The architecture SHALL permit new ScriptPacks to be introduced without requiring modifications to the Foundation runtime.

Future runtime services MAY be introduced provided that existing architectural contracts remain compatible.

---

# 2. Foundation Overview

## 2.1 Overview

The Aksara Nusantara Foundation is the runtime layer responsible for coordinating ScriptPack execution independently of any application or writing system.

Rather than implementing writing-system-specific behavior, the Foundation provides a collection of reusable runtime services that together establish a consistent execution environment for every ScriptPack.

The Foundation operates as a service-oriented architecture in which each runtime service has a single, clearly defined responsibility.

Applications interact exclusively with the Foundation through the Core Engine. The Core Engine, in turn, coordinates the Foundation services required to discover, validate, load, register, and expose ScriptPacks.

The Foundation does not contain language-specific knowledge. All linguistic rules, character definitions, transliteration logic, and writing-system behavior remain the responsibility of individual ScriptPacks.

---

## 2.2 Architectural Layers

The Foundation architecture is organized into four logical layers.

```

Application Layer
        │
        ▼
+-----------------------------+
|      Coordination Layer     |
|-----------------------------|
|         Core Engine         |
+-----------------------------+
               │
               ▼
+-----------------------------+
|     Foundation Services     |
|-----------------------------|
| Loader                      |
| Validator                   |
| Registry                    |
+-----------------------------+
               │
               ▼
+-----------------------------+
|   Foundation Contracts      |
|-----------------------------|
| BaseScriptPack              |
+-----------------------------+
               │
               ▼
+-----------------------------+
| ScriptPack Implementations  |
+-----------------------------+

```text

Each layer has a distinct architectural responsibility.

Dependencies SHALL flow downward only.

Reverse dependencies SHALL NOT exist.

---

## 2.3 Coordination Layer

The Coordination Layer contains a single component:

- Core Engine

The Core Engine acts as the runtime coordinator of the Foundation.

Its primary responsibility is to orchestrate the interaction between Foundation services while exposing a stable public API to the Application Layer.

The Core Engine SHALL NOT perform ScriptPack validation.

The Core Engine SHALL NOT load Python modules directly.

The Core Engine SHALL NOT store ScriptPack metadata.

Instead, those responsibilities are delegated to specialized Foundation services.

---

## 2.4 Foundation Services

Foundation Services perform the operational work of the runtime.

Each service owns exactly one primary responsibility.

### Loader

The Loader is responsible for discovering available ScriptPacks, importing their implementation modules, instantiating BaseScriptPack implementations, and producing runtime objects suitable for registration.

The Loader SHALL NOT validate ScriptPacks.

The Loader SHALL NOT register ScriptPacks.

---

### Validator

The Validator verifies that every discovered ScriptPack satisfies the architectural requirements defined by the Foundation.

Validation occurs before runtime registration.

Only successfully validated ScriptPacks may proceed to registration.

---

### Registry

The Registry maintains the runtime collection of successfully loaded ScriptPacks.

The Registry provides lookup services for the Core Engine and applications.

The Registry SHALL contain only validated ScriptPacks.

---

## 2.5 Architectural Contract

Communication between the Foundation and every ScriptPack SHALL occur exclusively through the BaseScriptPack contract.

The Foundation SHALL NOT depend upon implementation details of individual ScriptPacks.

Likewise, ScriptPacks SHALL NOT depend upon Foundation implementation details beyond the published BaseScriptPack interface.

This architectural boundary guarantees that ScriptPacks remain independently replaceable.

---

## 2.6 Runtime Representation

After successful loading, every ScriptPack is represented internally by a runtime model.

The runtime representation encapsulates:

- ScriptPack metadata;
- validated manifest information;
- ScriptPack implementation instance.

Foundation services exchange runtime representations rather than raw Python modules or file-system paths.

This ensures a consistent internal representation throughout the runtime lifecycle.

---

## 2.7 Runtime Lifecycle

The Foundation runtime follows a deterministic initialization sequence.

```

Application
      │
      ▼
CoreEngine.initialize()
      │
      ▼
Discover ScriptPacks
      │
      ▼
Validate
      │
      ▼
Load
      │
      ▼
Register
      │
      ▼
Ready

```text

Each phase SHALL complete successfully before the next phase begins.

Failure during any phase SHALL terminate the initialization process.

No partially initialized runtime SHALL remain active.

---

## 2.8 Dependency Rules

Dependencies within the Foundation SHALL follow the rules below.

Permitted dependencies:

Application
→ Core Engine

Core Engine
→ Loader

Core Engine
→ Validator

Core Engine
→ Registry

Loader
→ BaseScriptPack

Validator
→ BaseScriptPack

Registry
→ Runtime Model

Forbidden dependencies:

ScriptPack
→ Core Engine

ScriptPack
→ Registry

Validator
→ Loader

Registry
→ Validator

Registry
→ Loader

Application
→ Concrete ScriptPack

These rules preserve the architectural independence of every Foundation component.

---

## 2.9 Architectural Characteristics

The Foundation exhibits the following architectural characteristics.

### Deterministic

The initialization sequence always produces identical results for identical inputs.

### Stateless Coordination

The Core Engine coordinates services without owning ScriptPack implementation details.

### Service Isolation

Each Foundation service performs one well-defined responsibility.

### Replaceability

ScriptPacks may be added, removed, or replaced without modifying the Foundation.

### Platform Independence

The Foundation operates independently from graphical user interfaces and application frameworks.

---

# 3. Architectural Principles

## 3.1 Overview

The Foundation is intentionally designed as a minimal runtime platform.

Rather than implementing writing-system functionality directly, the Foundation provides generic runtime services that coordinate independent ScriptPack implementations through stable architectural contracts.

The principles defined in this chapter govern every architectural decision within the Foundation. Future modifications SHALL preserve these principles unless superseded by an approved Architecture Decision Record (ADR).

---

## 3.2 Small Core Principle

The Foundation SHALL remain intentionally small.

Responsibilities that are specific to a writing system SHALL NOT be implemented within the Foundation.

Instead, such functionality SHALL reside within individual ScriptPacks.

This principle minimizes maintenance complexity while allowing the ecosystem to grow without increasing the complexity of the Core Engine.

Examples of functionality that SHALL remain outside the Foundation include:

- character definitions;
- transliteration rules;
- pronunciation rules;
- writing-system metadata;
- educational content.

---

## 3.3 Separation of Responsibilities

Each Foundation component SHALL have one clearly defined primary responsibility.

No component SHALL duplicate the responsibility of another component.

The responsibilities of the primary Foundation services are summarized below.

| Component | Primary Responsibility |
|-----------|------------------------|
| Core Engine | Runtime coordination |
| Loader | ScriptPack discovery and loading |
| Validator | ScriptPack validation |
| Registry | Runtime storage and lookup |
| BaseScriptPack | Architectural contract |

Architectural changes SHALL preserve this separation.

---

## 3.4 Contract-Based Architecture

The Foundation communicates with ScriptPacks exclusively through the BaseScriptPack contract.

Concrete ScriptPack implementations are considered replaceable components.

Applications and Foundation services SHALL depend only on published contracts.

This principle enables independent development of ScriptPacks without requiring changes to the Foundation runtime.

---

## 3.5 Dependency Direction

Dependencies SHALL always point toward lower architectural layers.

The dependency flow is illustrated below.

Application
    ↓
Core Engine
    ↓
Foundation Services
    ↓
Foundation Contracts
    ↓
ScriptPack Implementations

Reverse dependencies SHALL NOT exist.

In particular:

- ScriptPacks SHALL NOT access the Core Engine.
- ScriptPacks SHALL NOT manipulate the Registry.
- Foundation services SHALL NOT depend upon one another unless explicitly defined by this specification.

Maintaining a single dependency direction reduces coupling and simplifies long-term maintenance.

---

## 3.6 Service Isolation

Foundation services SHALL remain independent.

Each service owns its own responsibility and exposes only the behavior required by the Core Engine.

Services SHALL communicate through published interfaces rather than shared implementation details.

This isolation enables services to evolve independently while preserving architectural stability.

---

## 3.7 Deterministic Initialization

Foundation initialization SHALL follow a deterministic sequence.

For identical inputs, initialization SHALL always produce identical runtime results.

The initialization process SHALL terminate immediately if any mandatory phase fails.

Partially initialized Foundation states SHALL NOT be exposed to applications.

This guarantees predictable runtime behavior and simplifies debugging.

---

## 3.8 Explicit Runtime Ownership

Every runtime object SHALL have a clearly defined owner.

Ownership within the Foundation is summarized below.

| Runtime Object | Owner |
|----------------|-------|
| Foundation lifecycle | Core Engine |
| Loaded ScriptPacks | Registry |
| Validation process | Validator |
| Loading process | Loader |
| ScriptPack implementation | ScriptPack |

Ownership SHALL NOT be shared unless explicitly defined by this specification.

---

## 3.9 UI Independence

The Foundation SHALL remain independent of any graphical user interface framework.

The Foundation SHALL NOT import or depend upon desktop, mobile, or web user interface libraries.

Applications are responsible for presenting data to users.

The Foundation is responsible only for providing runtime services.

This separation enables the same Foundation implementation to be reused by multiple applications.

---

## 3.10 Extensibility

The Foundation SHALL support future expansion without requiring modification of existing ScriptPacks.

Examples of future extensions include:

- Session management;
- additional runtime services;
- caching mechanisms;
- remote ScriptPack repositories;
- marketplace integration.

New functionality SHOULD be introduced by extending the architecture rather than modifying existing contracts.

---

## 3.11 Backward Compatibility

Public architectural contracts SHALL remain stable across Foundation releases.

Breaking changes SHALL require:

- a documented migration strategy;
- an Architecture Decision Record (ADR);
- corresponding updates to all affected specifications.

This principle protects existing ScriptPacks from unnecessary incompatibilities.

---

## 3.12 Summary

The architectural principles defined in this chapter establish the long-term design philosophy of the Foundation.

Every component, service, contract, and future extension SHALL conform to these principles unless an approved architectural decision explicitly defines an exception.

---

# 4. Foundation Components

## 4.1 Overview

The Foundation is composed of a small number of independent architectural components.

Each component owns a single runtime responsibility and collaborates with other components exclusively through well-defined interfaces.

The Foundation components are grouped into the following architectural categories.

| Category | Components |
|----------|------------|
| Coordination | Core Engine |
| Runtime Services | Loader, Validator, Registry |
| Architectural Contracts | BaseScriptPack |
| Runtime Models | LoadedScriptPack |
| Error Model | Foundation Exceptions |

Each category is described in the following sections.

---

# 4.2 Coordination Layer

## 4.2.1 Overview

The Coordination Layer contains the Core Engine.

The Core Engine is the entry point of the Foundation runtime.

Applications SHALL communicate exclusively with the Foundation through the Core Engine.

No application component SHALL directly invoke Foundation services.

---

## 4.2.2 Responsibilities

The Core Engine SHALL:

- initialize the Foundation runtime;
- coordinate Foundation services;
- expose the public runtime API;
- manage Foundation lifecycle;
- provide access to registered ScriptPacks.

The Core Engine SHALL NOT:

- validate ScriptPacks;
- discover ScriptPacks;
- import Python modules;
- manipulate ScriptPack assets;
- interpret writing-system data.

Those responsibilities belong to dedicated Foundation services.

---

## 4.2.3 Collaborators

The Core Engine collaborates with:

- Loader
- Validator
- Registry

The Core Engine SHALL NOT collaborate directly with concrete ScriptPack implementations.

All ScriptPack interaction SHALL occur through the BaseScriptPack contract.

---

## 4.2.4 Lifecycle

The Core Engine lifecycle consists of:

1. Construction
2. Initialization
3. Runtime Operation
4. Shutdown

Initialization SHALL complete successfully before runtime services become available.

Applications SHALL NOT access Foundation services before initialization has completed.

---

## 4.2.5 Public Responsibilities

The Core Engine provides the public Foundation interface.

Typical operations include:

- initialize()
- retrieve ScriptPacks
- query runtime information
- expose Foundation state

Applications SHALL NOT access Foundation services directly.

---

## 4.2.6 Requirement IDs

CA-CE-001

The Core Engine SHALL coordinate Foundation services.

CA-CE-002

The Core Engine SHALL expose the public Foundation API.

CA-CE-003

The Core Engine SHALL remain independent from writing-system implementations.

CA-CE-004

The Core Engine SHALL NOT implement ScriptPack functionality.

---

# 4.3 Runtime Services

## 4.3.1 Overview

Runtime Services perform the operational work of the Foundation.

Unlike the Core Engine, runtime services do not coordinate one another.

Each service owns one well-defined responsibility.

Runtime services SHALL remain independent.

```
                    Core Engine
                         │
     ┌───────────┬─────────────┬───────────┐
     ▼           ▼             ▼
 Loader      Validator      Registry
```

No runtime service SHALL become responsible for another runtime service.

---

## 4.3.2 Loader

### Purpose

The Loader is responsible for discovering available ScriptPacks and transforming them into runtime objects that can be managed by the Foundation.

The Loader provides the transition between the file-system representation of a ScriptPack and its runtime representation.

The Loader SHALL remain independent of application logic and SHALL operate exclusively within the Foundation.

---

### Responsibilities

The Loader SHALL:

- discover available ScriptPack directories;
- locate ScriptPack manifests;
- import ScriptPack implementation modules;
- instantiate BaseScriptPack implementations;
- construct runtime representations;
- report loading failures to the Core Engine.

The Loader SHALL NOT:

- validate ScriptPack contents;
- register ScriptPacks;
- modify ScriptPack assets;
- expose public runtime APIs.

---

### Runtime Process

The Loader performs the following sequence.

```
Discover ScriptPack
        │
        ▼
Locate Manifest
        │
        ▼
Import Module
        │
        ▼
Instantiate BaseScriptPack
        │
        ▼
Create LoadedScriptPack
        │
        ▼
Return to Core Engine
```

Each step SHALL complete successfully before the next step begins.

Any unrecoverable error SHALL terminate the loading process for the affected ScriptPack.

---

### Collaboration

The Loader collaborates with:

- Core Engine
- BaseScriptPack
- LoadedScriptPack

The Loader SHALL NOT collaborate directly with:

- Registry
- Applications
- User Interface components

The Loader SHALL NOT perform responsibilities assigned to the Validator.

---

### Runtime Ownership

The Loader owns the loading process only.

Ownership of runtime objects is transferred immediately after loading completes.

Loaded ScriptPack instances SHALL become the responsibility of the Registry after successful registration.

---

### Error Handling

The Loader SHALL report loading failures using the Foundation exception hierarchy.

Typical loading failures include:

- missing implementation module;
- invalid Python import;
- instantiation failure;
- unsupported ScriptPack implementation.

The Loader SHALL NOT suppress runtime exceptions that prevent successful loading.

---

### Requirement IDs

CA-LD-001

The Loader SHALL discover available ScriptPacks.

CA-LD-002

The Loader SHALL instantiate BaseScriptPack implementations.

CA-LD-003

The Loader SHALL construct runtime representations.

CA-LD-004

The Loader SHALL remain independent from validation.

CA-LD-005

The Loader SHALL NOT register ScriptPacks.

---

## 4.3.3 Validator

| Item | Value |
|------|-------|
| Category | Runtime Service |
| Owner | Foundation |
| Lifetime | During Initialization |
| Primary Responsibility | Validate ScriptPacks |
| Input | ScriptPack Directory |
| Output | Validation Result |
| Used By | Core Engine |

---

### Purpose

The Validator is responsible for ensuring that every ScriptPack conforms to the architectural requirements of the Foundation before it becomes available at runtime.

The Validator protects the integrity of the Foundation by preventing incomplete, incompatible, or malformed ScriptPacks from entering the runtime environment.

Validation SHALL occur before any ScriptPack is registered.

---

### Responsibilities

The Validator SHALL:

- verify the existence of required files;
- validate the ScriptPack manifest;
- verify mandatory metadata fields;
- verify the ScriptPack entry point;
- verify BaseScriptPack conformance;
- report validation failures.

The Validator SHALL NOT:

- import application modules;
- register ScriptPacks;
- modify ScriptPack contents;
- repair invalid ScriptPacks.

---

### Validation Pipeline

Validation SHALL follow the sequence below.

```
ScriptPack Directory
          │
          ▼
Directory Validation
          │
          ▼
Manifest Validation
          │
          ▼
Required Field Validation
          │
          ▼
Entry Point Validation
          │
          ▼
Interface Validation
          │
          ▼
PASS / FAIL
```

Each validation stage SHALL complete successfully before the following stage begins.

Validation SHALL terminate immediately after the first unrecoverable error.

---

### Validation Stages

#### Directory Validation

The Validator SHALL verify that the ScriptPack directory exists and conforms to the required directory layout.

---

#### Manifest Validation

The Validator SHALL verify that the manifest exists and can be parsed successfully.

Malformed manifests SHALL invalidate the ScriptPack.

---

#### Required Field Validation

The Validator SHALL verify that every mandatory manifest field is present.

Missing mandatory fields SHALL invalidate the ScriptPack.

---

#### Entry Point Validation

The Validator SHALL verify that the implementation entry point exists.

Missing implementation modules SHALL invalidate the ScriptPack.

---

#### Interface Validation

The Validator SHALL verify that the implementation conforms to the BaseScriptPack architectural contract.

Objects that do not satisfy the required interface SHALL NOT enter the runtime.

---

### Collaboration

The Validator collaborates with:

- Core Engine
- Loader
- BaseScriptPack

The Validator SHALL NOT collaborate directly with:

- Registry
- Applications
- User Interface components

The Validator SHALL remain independent of runtime registration.

---

### Runtime Ownership

The Validator owns the validation process only.

The Validator does not own ScriptPack instances.

The Validator does not retain runtime state after validation completes.

---

### Error Handling

Validation failures SHALL be reported through the Foundation exception hierarchy.

Typical validation failures include:

- missing directory;
- missing manifest;
- malformed manifest;
- missing required fields;
- invalid entry point;
- interface incompatibility.

The Validator SHALL provide sufficient diagnostic information for developers to identify the source of the failure.

---

### Requirement IDs

CA-VA-001

The Validator SHALL verify ScriptPack directory structure.

CA-VA-002

The Validator SHALL validate the ScriptPack manifest.

CA-VA-003

The Validator SHALL verify mandatory manifest fields.

CA-VA-004

The Validator SHALL verify BaseScriptPack conformance.

CA-VA-005

The Validator SHALL reject invalid ScriptPacks before registration.

CA-VA-006

Validation SHALL terminate upon the first unrecoverable error.

---

## 4.3.4 Registry

| Item | Value |
|------|-------|
| Category | Runtime Service |
| Owner | Foundation |
| Lifetime | During Runtime |
| Primary Responsibility | Maintain the runtime ScriptPack repository |
| Input | LoadedScriptPack |
| Output | Runtime lookup services |
| Used By | Core Engine |

---

### Purpose

The Registry is responsible for maintaining the runtime collection of successfully loaded and validated ScriptPacks.

The Registry represents the authoritative source of ScriptPack information during Foundation execution.

Applications SHALL access registered ScriptPacks through the Core Engine rather than interacting with the Registry directly.

---

### Responsibilities

The Registry SHALL:

- register validated ScriptPacks;
- unregister ScriptPacks when required;
- maintain the runtime ScriptPack repository;
- provide lookup operations;
- provide enumeration of registered ScriptPacks.

The Registry SHALL NOT:

- discover ScriptPacks;
- validate ScriptPacks;
- instantiate ScriptPacks;
- manipulate ScriptPack assets.

---

### Runtime Workflow

The Registry receives ownership of runtime objects after successful validation and loading.

```
LoadedScriptPack
        │
        ▼
Register
        │
        ▼
Runtime Repository
        │
        ├────────► Lookup
        │
        ├────────► Enumeration
        │
        └────────► Runtime Access
```

The Registry SHALL become the runtime owner of every successfully registered ScriptPack.

---

### Runtime Repository

The Registry maintains a collection of runtime representations.

Each registered ScriptPack SHALL:

- possess a unique identifier;
- remain available until explicitly removed;
- be retrievable through the public Foundation API.

Duplicate registrations SHALL NOT be permitted.

---

### Collaboration

The Registry collaborates with:

- Core Engine
- LoadedScriptPack

The Registry SHALL NOT collaborate directly with:

- Loader
- Validator
- Applications
- User Interface components

The Registry SHALL remain independent of ScriptPack discovery and validation.

---

### Runtime Ownership

Ownership of ScriptPack runtime objects is transferred to the Registry immediately after successful registration.

The Registry SHALL remain responsible for:

- runtime availability;
- lookup operations;
- registration state.

The Registry SHALL NOT assume ownership of ScriptPack assets or implementation modules.

---

### Lookup Operations

The Registry SHALL provide runtime lookup services.

Typical lookup operations include:

- retrieve ScriptPack by identifier;
- enumerate registered ScriptPacks;
- determine registration status.

Lookup operations SHALL NOT modify Registry state.

---

### Error Handling

Registration failures SHALL be reported using the Foundation exception hierarchy.

Typical Registry errors include:

- duplicate registration;
- unknown ScriptPack identifier;
- invalid registration request.

Registry operations SHALL preserve repository consistency following runtime failures.

---

### Requirement IDs

CA-RG-001

The Registry SHALL maintain the runtime ScriptPack repository.

CA-RG-002

Only validated ScriptPacks SHALL be registered.

CA-RG-003

Duplicate registrations SHALL be rejected.

CA-RG-004

The Registry SHALL provide runtime lookup operations.

CA-RG-005

Lookup operations SHALL NOT modify runtime state.

CA-RG-006

The Registry SHALL become the runtime owner of registered ScriptPacks.

---

# 4.4 Architectural Contract

## 4.4.1 BaseScriptPack

| Item | Value |
|------|-------|
| Category | Architectural Contract |
| Owner | Foundation |
| Lifetime | Entire Runtime |
| Primary Responsibility | Define the ScriptPack contract |
| Implemented By | Every ScriptPack |
| Used By | Loader, Validator, Core Engine |

---

### Purpose

BaseScriptPack defines the architectural contract between the Foundation and every ScriptPack implementation.

It establishes the minimum behavior that every ScriptPack SHALL provide in order to participate in the Foundation runtime.

The Foundation SHALL interact only with this contract.

The Foundation SHALL NOT depend upon implementation-specific behavior.

---

### Architectural Role

BaseScriptPack represents the boundary between the Foundation and independently developed ScriptPacks.

This boundary guarantees that:

- ScriptPacks remain replaceable;
- the Foundation remains implementation-independent;
- applications remain unaware of ScriptPack internals.

The contract therefore serves as the primary extension point of the Foundation.

---

### Responsibilities

Every ScriptPack implementation SHALL:

- implement the BaseScriptPack contract;
- expose the required runtime behavior;
- provide access to ScriptPack metadata;
- expose writing-system services defined by the contract.

Implementations MAY provide additional functionality provided that such functionality does not alter the published contract.

---

### Collaboration

BaseScriptPack collaborates with:

- Loader
- Validator
- Core Engine

Concrete ScriptPack implementations SHALL NOT communicate directly with Foundation services other than through the published contract.

---

### Contract Stability

The BaseScriptPack contract SHALL remain stable across Foundation releases.

Breaking changes SHALL require:

- an approved Architecture Decision Record (ADR);
- corresponding updates to this specification;
- migration guidance for ScriptPack developers.

Contract stability is essential for long-term compatibility across the ecosystem.

---

### Extensibility

New functionality SHOULD be introduced through additive evolution.

Existing contract members SHALL NOT be removed unless a major Foundation version explicitly defines a compatibility break.

This principle minimizes disruption to existing ScriptPacks.

---

### Requirement IDs

CA-CT-001

Every ScriptPack SHALL implement BaseScriptPack.

CA-CT-002

The Foundation SHALL interact exclusively through the published contract.

CA-CT-003

Concrete ScriptPack implementations SHALL remain replaceable.

CA-CT-004

Breaking contract changes SHALL require an ADR.

CA-CT-005

The BaseScriptPack contract SHALL remain backward compatible within a Foundation major version.

---

## 4.5 Runtime Representation

### 4.5.1 LoadedScriptPack

| Item | Value |
|------|-------|
| Category | Runtime Model |
| Owner | Registry |
| Lifetime | During Runtime |
| Primary Responsibility | Represent a loaded ScriptPack |
| Created By | Loader |
| Used By | Registry, Core Engine |

---

### Purpose

LoadedScriptPack is the canonical runtime representation of a ScriptPack within the Foundation.

Rather than exposing implementation modules directly, the Foundation exchanges runtime representations between internal services.

This abstraction provides a stable and implementation-independent model for managing ScriptPacks during runtime.

Applications SHALL NOT interact directly with LoadedScriptPack.

All application interaction SHALL occur through the Core Engine.

---

### Responsibilities

LoadedScriptPack SHALL encapsulate:

- validated ScriptPack metadata;
- the instantiated BaseScriptPack implementation;
- runtime information required by the Foundation.

LoadedScriptPack SHALL remain immutable from the perspective of Foundation services unless explicitly modified through controlled runtime operations.

---

### Runtime Lifecycle

A LoadedScriptPack progresses through the following lifecycle.

```

Filesystem

↓

Loader

↓

LoadedScriptPack Created

↓

Validation Complete

↓

Registry Ownership

↓

Runtime Access

↓

Runtime Shutdown

```text

Runtime representations SHALL exist only while the Foundation runtime is active.

---

### Collaboration

LoadedScriptPack collaborates with:

- Loader
- Registry
- Core Engine

LoadedScriptPack SHALL NOT communicate with:

- Applications
- User Interface components
- Concrete ScriptPack implementations

LoadedScriptPack is a passive runtime model.

It contains runtime information but performs no runtime coordination.

---

### Runtime Ownership

Ownership of LoadedScriptPack SHALL be transferred as follows.

```

Loader

↓

Registry

↓

Foundation Runtime

```text

Ownership SHALL NOT return to the Loader after successful registration.

---

### Design Considerations

The Foundation intentionally separates runtime representation from ScriptPack implementation.

This separation provides several architectural advantages.

- Runtime services exchange a consistent object model.
- ScriptPack implementations remain isolated.
- Runtime metadata remains independent from implementation logic.
- Future runtime information may be added without modifying the ScriptPack contract.

---

### Requirement IDs

CA-RM-001

LoadedScriptPack SHALL represent every successfully loaded ScriptPack.

CA-RM-002

LoadedScriptPack SHALL encapsulate runtime metadata and the ScriptPack instance.

CA-RM-003

Runtime services SHALL exchange LoadedScriptPack objects rather than implementation modules.

CA-RM-004

Ownership of LoadedScriptPack SHALL belong to the Registry after successful registration.

---

## 5. Foundation Runtime Pipeline

## 5.1 Overview

The Foundation Runtime Pipeline describes the end-to-end lifecycle of a ScriptPack as it transitions from a filesystem artifact into an active runtime component.

Unlike the previous chapter, which describes the structural building blocks of the Foundation, this chapter explains how those building blocks collaborate during runtime initialization.

The Runtime Pipeline defines the canonical execution sequence of the Foundation.

Every Foundation implementation SHALL preserve the ordering and responsibilities defined by this chapter.

---

## 5.2 Pipeline Stages

The Foundation Runtime Pipeline consists of six sequential stages.

```
Filesystem
      │
      ▼
Discovery
      │
      ▼
Loading
      │
      ▼
Validation
      │
      ▼
Registration
      │
      ▼
Runtime Ready
      │
      ▼
Application Access
```

Each stage SHALL complete successfully before the next stage begins.

Pipeline stages SHALL NOT execute concurrently unless explicitly supported by a future Foundation specification.

---

## 5.3 Stage 1 — Discovery

### Purpose

Discovery identifies ScriptPack candidates available to the Foundation.

During this stage, the Foundation scans configured ScriptPack locations and identifies potential ScriptPack directories.

No runtime objects exist during this stage.

### Output

The Discovery stage produces a collection of candidate ScriptPack locations.

---

## 5.4 Stage 2 — Loading

### Purpose

The Loading stage transforms a filesystem-based ScriptPack into its runtime representation.

The Loader performs the following activities.

- locate the manifest;
- import the implementation module;
- instantiate the BaseScriptPack implementation;
- construct the LoadedScriptPack runtime representation.

### Output

The Loading stage produces one LoadedScriptPack instance for each successfully loaded ScriptPack.

---

## 5.5 Stage 3 — Validation

### Purpose

Validation verifies that every loaded ScriptPack satisfies the architectural requirements of the Foundation.

Validation SHALL occur before registration.

### Validation Scope

The Validator verifies:

- directory structure;
- manifest integrity;
- required metadata;
- implementation entry point;
- BaseScriptPack conformance.

### Output

The Validation stage produces a validation decision.

Only ScriptPacks that pass validation SHALL continue to the next stage.

---

## 5.6 Stage 4 — Registration

### Purpose

Registration transfers ownership of runtime representations to the Registry.

Successfully validated ScriptPacks become available for runtime lookup.

### Output

The Registration stage produces the runtime repository.

---

## 5.7 Stage 5 — Runtime Ready

After successful registration, the Foundation enters the operational runtime state.

The Registry becomes the authoritative source of ScriptPack information.

Applications SHALL NOT access ScriptPacks prior to this stage.

---

## 5.8 Stage 6 — Application Access

Applications interact exclusively with the Core Engine.

The Core Engine exposes runtime services while hiding internal Foundation components.

Applications SHALL remain independent of:

- Loader;
- Validator;
- Registry;
- LoadedScriptPack.

---

## 5.9 Pipeline Characteristics

The Foundation Runtime Pipeline possesses the following characteristics.

### Deterministic

Pipeline execution SHALL follow a deterministic ordering.

### Sequential

Each stage SHALL complete before the next begins.

### Fail-Fast

Pipeline execution SHALL terminate immediately upon encountering an unrecoverable architectural error.

### Observable

Pipeline progress SHOULD be observable through logging or diagnostic mechanisms.

### Extensible

Future Foundation versions MAY introduce additional pipeline stages provided existing stage semantics remain unchanged.

---

## 5.10 Pipeline Summary

The complete Foundation Runtime Pipeline is illustrated below.

```
Filesystem
      │
      ▼
Discovery
      │
      ▼
Loader
      │
      ▼
LoadedScriptPack
      │
      ▼
Validator
      │
      ▼
PASS
      │
      ▼
Registry
      │
      ▼
Runtime Repository
      │
      ▼
Core Engine
      │
      ▼
Application
```

This execution model represents the canonical runtime behavior of Foundation v1.0.

---

# 6. Runtime API

## 6.1 Overview

The Runtime API defines the public interface through which applications interact with the Foundation.

Applications SHALL communicate exclusively with the Core Engine.

Internal Foundation components SHALL remain inaccessible to applications.

The Runtime API provides a stable abstraction that isolates applications from Foundation implementation details.

---

## 6.2 Architectural Boundary

The Runtime API establishes the boundary between the Application Layer and the Foundation.

```
+---------------------------+
|      Application          |
+---------------------------+
            │
            ▼
+---------------------------+
|       Runtime API         |
|       (Core Engine)       |
+---------------------------+
            │
            ▼
+---------------------------+
|   Foundation Internals    |
| Loader • Validator •      |
| Registry • Contracts      |
+---------------------------+
```

Applications SHALL NOT bypass the Runtime API.

---

## 6.3 Design Principles

The Runtime API is governed by the following principles.

### Simplicity

Applications SHOULD require minimal knowledge of Foundation internals.

---

### Stability

The Runtime API SHALL remain stable across compatible Foundation releases.

---

### Encapsulation

Internal Foundation services SHALL remain hidden.

Applications SHALL NOT depend upon implementation-specific behavior.

---

### Predictability

Every public operation SHALL exhibit deterministic behavior.

---

## 6.4 Runtime Services

The Runtime API SHALL provide services including, but not limited to:

- Foundation initialization;
- ScriptPack discovery;
- ScriptPack lookup;
- access to writing-system services;
- runtime status inspection.

Applications SHALL obtain these services exclusively through the Core Engine.

---

## 6.5 Runtime Initialization

Applications SHALL initialize the Foundation before requesting runtime services.

The canonical initialization sequence is shown below.

```
Application

↓

CoreEngine.initialize()

↓

Foundation Runtime

↓

Ready
```

Applications SHALL NOT access ScriptPacks before initialization completes successfully.

---

## 6.6 ScriptPack Access

Applications SHALL retrieve ScriptPack functionality through the Runtime API.

Applications SHALL NOT:

- instantiate ScriptPacks directly;
- access the Registry;
- invoke the Loader;
- perform validation.

These responsibilities belong exclusively to the Foundation.

---

## 6.7 Error Reporting

Runtime failures SHALL be reported using the Foundation Exception Model.

Applications MAY:

- recover from runtime failures;
- present diagnostic information;
- terminate execution.

Presentation of runtime errors is outside the scope of the Foundation.

---

## 6.8 Future Compatibility

Future Foundation releases MAY extend the Runtime API.

Existing public behavior SHALL remain backward compatible within the same major Foundation version.

Breaking Runtime API changes SHALL require:

- an approved ADR;
- specification updates;
- migration guidance.

---

## 6.9 Requirement IDs

CA-API-001

Applications SHALL communicate exclusively through the Runtime API.

CA-API-002

The Runtime API SHALL be implemented by the Core Engine.

CA-API-003

Applications SHALL NOT access Foundation internal services directly.

CA-API-004

Runtime initialization SHALL complete before runtime services become available.

CA-API-005

Runtime API changes SHALL preserve backward compatibility within a major Foundation version.

---

# 7. Extension API

## 7.1 Overview

The Extension API defines the architectural contract through which independently developed ScriptPacks integrate with the Foundation.

Unlike the Runtime API, which serves application developers, the Extension API serves ScriptPack developers.

The Extension API enables the Foundation to support independently developed writing systems while preserving architectural consistency and runtime stability.

The Extension API SHALL remain independent of any specific writing system.

---

## 7.2 Architectural Boundary

The Extension API establishes the boundary between the Foundation and ScriptPack implementations.

```
+---------------------------+
|        Foundation         |
|      Extension API        |
|    (BaseScriptPack)       |
+---------------------------+
             ?
             �
+---------------------------+
|      ScriptPack           |
|    Implementation         |
+---------------------------+
```

All ScriptPack implementations SHALL communicate with the Foundation through this boundary.

---

## 7.3 Design Principles

The Extension API is governed by the following principles.

### Contract-Based Integration

ScriptPacks SHALL integrate exclusively through the published architectural contract.

---

### Implementation Independence

The Foundation SHALL remain independent of implementation-specific behavior.

---

### Replaceability

Any compliant ScriptPack MAY be replaced by another compliant implementation without requiring changes to the Foundation.

---

### Compatibility

The Extension API SHALL preserve compatibility within a Foundation major version.

---

### Extensibility

Future versions MAY extend the contract through additive changes.

Existing contract members SHALL NOT be removed without a major version increment.

---

## 7.4 Required Capabilities

Every ScriptPack SHALL provide the capabilities defined by the BaseScriptPack contract.

These capabilities include:

- Script metadata;
- writing system information;
- character access;
- transliteration services;
- optional runtime services defined by future specifications.

The exact programming interface is specified separately in the ScriptPack Interface Specification.

This document defines only the architectural requirements.

---

## 7.5 Foundation Responsibilities

The Foundation SHALL:

- discover ScriptPacks;
- validate contract compliance;
- manage runtime lifecycle;
- provide runtime services.

The Foundation SHALL NOT:

- modify ScriptPack implementations;
- alter ScriptPack assets;
- depend upon implementation-specific extensions.

---

## 7.6 ScriptPack Responsibilities

Each ScriptPack SHALL:

- implement the BaseScriptPack contract;
- provide complete metadata;
- remain self-contained;
- preserve runtime integrity.

ScriptPacks SHOULD avoid dependencies on Foundation internals beyond the published Extension API.

---

## 7.7 Version Compatibility

The Foundation SHALL verify compatibility between the Extension API version and the ScriptPack implementation.

ScriptPacks declaring incompatible versions SHALL be rejected during initialization.

Compatibility requirements are defined by the ScriptPack Interface Specification.

---

## 7.8 Extension Lifecycle

The Foundation manages the lifecycle of every ScriptPack.

```
Develop

?

Package

?

Install

?

Discover

?

Load

?

Validate

?

Register

?

Runtime

?

Unload (Future)
```

ScriptPack developers SHALL remain responsible only for the implementation.

Runtime lifecycle management belongs exclusively to the Foundation.

---

## 7.9 Error Handling

Errors occurring within ScriptPack implementations SHALL be reported using the Foundation Exception Model whenever possible.

The Foundation SHALL prevent invalid ScriptPacks from affecting runtime stability.

---

## 7.10 Requirement IDs

CA-EXT-001

ScriptPacks SHALL integrate exclusively through the Extension API.

CA-EXT-002

Every ScriptPack SHALL implement BaseScriptPack.

CA-EXT-003

The Foundation SHALL validate Extension API compatibility.

CA-EXT-004

ScriptPack implementations SHALL remain independent of Foundation internals.

CA-EXT-005

Breaking Extension API changes SHALL require a major Foundation version.

---

# 8. Versioning and Compatibility

## 8.1 Overview

The Foundation SHALL evolve in a controlled and predictable manner.

Versioning provides a mechanism for communicating compatibility expectations between the Foundation, applications, and ScriptPacks.

This chapter defines the compatibility guarantees provided by the Foundation Architecture.

---

## 8.2 Versioning Model

The Foundation adopts Semantic Versioning (SemVer).

```
MAJOR.MINOR.PATCH
```

Where:

- **MAJOR** introduces incompatible architectural changes.
- **MINOR** introduces backward-compatible functionality.
- **PATCH** introduces backward-compatible corrections and improvements.

Example:

```
1.0.0
1.1.0
1.1.3
2.0.0
```

---

## 8.3 Compatibility Guarantees

Within a Foundation major version:

- Runtime API SHALL remain backward compatible.
- Extension API SHALL remain backward compatible.
- Existing ScriptPacks SHOULD continue to function without modification.

Applications developed against Foundation 1.x SHOULD execute correctly on later Foundation 1.x releases.

---

## 8.4 Breaking Changes

Breaking changes include, but are not limited to:

- removal of Runtime API functionality;
- removal of Extension API contract members;
- incompatible changes to runtime behavior;
- incompatible lifecycle modifications.

Breaking changes SHALL require:

- incrementing the MAJOR version;
- an approved Architecture Decision Record (ADR);
- updates to the relevant specifications;
- documented migration guidance.

---

## 8.5 Additive Changes

The following changes are considered backward compatible:

- new Runtime API operations;
- optional Extension API capabilities;
- additional metadata fields;
- new runtime services;
- performance improvements.

Such changes MAY be introduced in MINOR releases.

---

## 8.6 ScriptPack Compatibility

Every ScriptPack SHALL declare the Foundation version with which it is compatible.

During initialization, the Foundation SHALL verify compatibility before registration.

ScriptPacks declaring unsupported Foundation versions SHALL be rejected.

---

## 8.7 Deprecation Policy

Deprecated functionality SHALL remain available throughout the current MAJOR version unless explicitly documented otherwise.

Deprecated functionality SHOULD:

- produce developer-facing warnings where appropriate;
- identify replacement functionality;
- specify the planned removal version.

Removal SHALL occur only in a subsequent MAJOR release.

---

## 8.8 Requirement IDs

CA-VC-001

The Foundation SHALL use Semantic Versioning.

CA-VC-002

Runtime API compatibility SHALL be preserved within a MAJOR version.

CA-VC-003

Extension API compatibility SHALL be preserved within a MAJOR version.

CA-VC-004

Breaking architectural changes SHALL require a MAJOR version increment.

CA-VC-005

ScriptPack compatibility SHALL be verified during initialization.

---

# 10. Future Evolution

## 10.1 Overview

The Foundation Architecture is designed to evolve while preserving its core architectural principles.

Future enhancements SHALL extend the Foundation through controlled evolution rather than architectural replacement.

This chapter identifies anticipated areas of future development.

Descriptions contained herein are informative unless explicitly stated otherwise.

---

## 10.2 Evolution Principles

Future Foundation development SHALL preserve the following principles.

- Architectural simplicity;
- Separation of responsibilities;
- Stable Runtime API;
- Stable Extension API;
- Deterministic Runtime Pipeline;
- Backward compatibility within a major version.

New functionality SHOULD extend existing architecture rather than replace it.

---

## 10.3 Planned Evolution Areas

Future versions MAY introduce capabilities including, but not limited to:

- Session management;
- Runtime caching;
- Dependency management between ScriptPacks;
- ScriptPack marketplaces;
- Remote ScriptPack repositories;
- Runtime performance optimization;
- Incremental loading;
- Parallel discovery;
- Enhanced diagnostics.

These capabilities SHALL integrate with the existing architectural model.

---

## 10.4 Session Layer

A future Foundation release MAY introduce a Session Layer.

The Session Layer would manage runtime state shared between applications and ScriptPacks without modifying the responsibilities of existing Foundation components.

The introduction of a Session Layer SHALL NOT alter the responsibilities of:

- Core Engine;
- Loader;
- Validator;
- Registry;
- BaseScriptPack.

The Session Layer SHALL be additive.

---

## 10.5 Runtime Extensibility

Future runtime services MAY be introduced provided they satisfy the following requirements.

- clearly defined responsibility;
- compatibility with the Runtime Pipeline;
- compatibility with the Exception Model;
- compatibility with Runtime and Extension APIs.

Runtime services SHALL remain loosely coupled.

---

## 10.6 Extension Evolution

The Extension API MAY evolve through additive functionality.

Future contract extensions SHOULD avoid introducing mandatory requirements for existing ScriptPacks.

Extension evolution SHALL prioritize ecosystem stability.

---

## 10.7 Non-Goals

The following items are outside the scope of Foundation evolution.

- User Interface design;
- Application business logic;
- Individual writing-system implementations;
- ScriptPack content;
- Platform-specific presentation logic.

These concerns belong to higher architectural layers.

---

## 10.8 Requirement IDs

CA-FE-001

Future Foundation evolution SHALL preserve the architectural principles defined by this specification.

CA-FE-002

New functionality SHOULD extend existing architecture rather than replace it.

CA-FE-003

Future runtime services SHALL remain compatible with the Runtime Pipeline.

CA-FE-004

Extension API evolution SHALL preserve ecosystem stability.

CA-FE-005

Application-specific functionality SHALL remain outside the Foundation.

---

# Appendix A � Normative Glossary

## A.1 Scope

This appendix defines the normative terminology used throughout this specification.

Unless explicitly stated otherwise, the definitions contained in this appendix SHALL apply wherever the corresponding terms appear.

The purpose of this glossary is to ensure consistent interpretation of architectural concepts across the Foundation Architecture Specification and related documents.

---

## A.2 Terms

### Application

Software that consumes Foundation services through the Runtime API.

Applications are external to the Foundation and SHALL NOT access internal Foundation components directly.

---

### Architectural Contract

A stable definition of responsibilities and behavior between independently developed software components.

Within the Foundation, the Architectural Contract is represented by the BaseScriptPack interface.

---

### Architecture Decision Record (ADR)

A document that captures a significant architectural decision, including its context, rationale, alternatives, and consequences.

ADRs complement this specification by recording why specific architectural choices were made.

---

### BaseScriptPack

The Foundation-defined contract implemented by every ScriptPack.

BaseScriptPack constitutes the Extension API of the Foundation.

---

### Building Block

A primary architectural element forming part of the Foundation runtime architecture.

Examples include:

- Core Engine
- Runtime Services
- Runtime Representation
- Exception Model
- BaseScriptPack

---

### Core Engine

The central coordinator of the Foundation.

The Core Engine exposes the Runtime API and orchestrates Foundation services during runtime.

---

### Extension API

The published architectural contract through which ScriptPacks integrate with the Foundation.

The Extension API is intended for ScriptPack developers.

---

### Extension Gateway

The architectural boundary through which ScriptPacks communicate with the Foundation.

Foundation v1.0 identifies BaseScriptPack as the Extension Gateway.

---

### Foundation

The runtime platform responsible for discovering, validating, loading, registering, and managing ScriptPacks.

---

### Foundation Runtime

The operational state entered after successful completion of the Runtime Pipeline.

---

### Loader

The Runtime Service responsible for transforming ScriptPacks from filesystem artifacts into Runtime Representations.

---

### Manifest

The metadata document describing a ScriptPack.

The manifest identifies the ScriptPack and provides information required during discovery, validation, and loading.

---

### Registry

The Runtime Service responsible for maintaining the Runtime Repository.

---

### Requirement ID

A unique identifier assigned to a normative architectural requirement.

Requirement IDs enable traceability between architectural decisions, implementation, testing, and documentation.

---

### Runtime API

The public interface exposed by the Core Engine.

Applications SHALL communicate with the Foundation exclusively through the Runtime API.

---

### Runtime Gateway

The architectural component implementing the Runtime API.

Foundation v1.0 identifies the Core Engine as the Runtime Gateway.

---

### Runtime Pipeline

The ordered sequence of stages that transforms ScriptPacks into active runtime components.

The Runtime Pipeline defines the canonical execution model of the Foundation.

---

### Runtime Representation

The canonical in-memory representation of a successfully loaded ScriptPack.

Runtime Representations are created by the Loader and managed by the Registry.

---

### Runtime Repository

The collection of Runtime Representations maintained by the Registry.

---

### Runtime Service

A Foundation component responsible for a specific runtime responsibility.

Foundation v1.0 defines the following Runtime Services:

- Loader
- Validator
- Registry

---

### ScriptPack

An independently developed package implementing support for a writing system.

Every ScriptPack SHALL conform to the Extension API.

---

### ScriptPack Developer

A developer responsible for implementing ScriptPacks using the Extension API.

---

### Validator

The Runtime Service responsible for verifying that a ScriptPack satisfies the architectural requirements of the Foundation before registration.

---

# Appendix B � Architecture Decision References

## B.1 Scope

This appendix identifies architectural decisions that are expected to be documented as Architecture Decision Records (ADRs).

The Foundation Architecture Specification defines the normative architecture of the Foundation. Individual ADRs provide the historical context, alternatives considered, rationale, and consequences behind significant architectural decisions.

This appendix establishes traceability between the architectural concepts defined by this specification and their corresponding ADRs.

Future ADR identifiers shown in this appendix are placeholders and MAY be updated as ADRs are created.

---

## B.2 Planned Architecture Decision Records

| Planned ADR | Architectural Topic | Related Sections | Status |
|--------------|---------------------|------------------|--------|
| ADR-0001 | Runtime Pipeline | Chapter 5 | Planned |
| ADR-0002 | Runtime API | Chapter 6 | Planned |
| ADR-0003 | Extension API | Chapter 7 | Planned |
| ADR-0004 | Runtime Representation | Section 4.5 | Planned |
| ADR-0005 | Foundation Exception Model | Section 4.6 | Planned |
| ADR-0006 | Version Compatibility Policy | Chapter 8 | Planned |
| ADR-0007 | Integrity Before Availability | Chapters 3 & 9 | Planned |
| ADR-0008 | Session Layer Introduction | Chapter 10 | Reserved |

---

## B.3 ADR Scope

Each Architecture Decision Record SHOULD contain the following information.

- Decision identifier
- Decision title
- Status
- Context
- Problem statement
- Considered alternatives
- Decision
- Consequences
- Related specifications
- Revision history

The recommended ADR template is maintained separately from this specification.

---

## B.4 Relationship Between Specifications and ADRs

The Foundation Architecture Specification defines **what** the architecture SHALL be.

Architecture Decision Records explain **why** architectural decisions were made.

Normative architectural requirements SHALL be maintained within this specification.

Historical reasoning SHALL be maintained within ADRs.

---

## B.5 Traceability

Architectural changes affecting this specification SHOULD reference the corresponding ADR.

Likewise, every approved ADR SHOULD identify the affected specification sections.

This bidirectional relationship improves long-term maintainability and architectural traceability.

---

## B.6 Future ADR Topics

Additional Architecture Decision Records MAY be created for topics including:

- Runtime caching
- ScriptPack dependency management
- Package repositories
- Digital signature verification
- Runtime permissions
- Parallel initialization
- Session Layer architecture
- Plugin lifecycle management
- Multi-application runtime support

The absence of an ADR from this appendix does not prohibit the creation of additional ADRs when future architectural decisions require formal documentation.

---

# Appendix C � Architectural Diagrams

## C.1 Scope

This appendix provides informative architectural diagrams illustrating the structure, relationships, and execution flow of the Foundation.

The diagrams in this appendix are intended to improve understanding of the normative architecture defined throughout this specification.

If a conflict exists between a diagram and the normative text, the normative text SHALL take precedence.

---

# C.2 Foundation Overview

```
                     +----------------------+
                     |     Application      |
                     +----------+-----------+
                                |
                           Runtime API
                                |
                     +----------v-----------+
                     |     Core Engine      |
                     +----------+-----------+
                                |
          +---------------------+----------------------+
          |                     |                      |
          |                     |                      |
+---------v---------+ +---------v---------+ +----------v---------+
|      Loader       | |     Validator     | |      Registry      |
+---------+---------+ +---------+---------+ +----------+---------+
          |                     |                      |
          +----------+----------+----------------------+
                     |
             Runtime Representation
                     |
             Loaded ScriptPacks
```

The Core Engine coordinates all Runtime Services and exposes the Runtime API to applications.

---

# C.3 Runtime Pipeline

```
Filesystem
     |
     v
ScriptPack Discovery
     |
     v
Manifest Loading
     |
     v
Validation
     |
     v
Registration
     |
     v
Foundation Runtime
```

Each stage SHALL complete successfully before the next stage begins.

---

# C.4 Runtime Ownership

```
Core Engine
      |
      +-----------------------------+
      |                             |
      v                             v
  Runtime API               Runtime Services
                                    |
          +-------------+-----------+-------------+
          |             |                         |
          v             v                         v
      Loader       Validator                 Registry
                                              |
                                              v
                                      Runtime Repository
                                              |
                                              v
                                   Loaded ScriptPacks
```

Each Runtime Service owns a single architectural responsibility.

---

# C.5 Runtime API

```
+-------------+
| Application |
+------+------+
       |
       | Runtime API
       |
+------v------+
| Core Engine |
+-------------+
```

Applications SHALL interact exclusively with the Runtime API.

---

# C.6 Extension API

```
ScriptPack Developer
        |
        v
+----------------------+
|   BaseScriptPack     |
+----------+-----------+
           |
           v
     Core Foundation
```

The BaseScriptPack interface defines the Extension API.

---

# C.7 ScriptPack Lifecycle

```
Filesystem
      |
      v
Discovery
      |
      v
Load ScriptPack
      |
      v
Validate
      |
      +------ invalid ------> Reject
      |
      v
Register
      |
      v
Available at Runtime
```

Only validated ScriptPacks become part of the Foundation Runtime.

---

# C.8 Runtime Representation

```
Filesystem
      |
      v
 ScriptPack
      |
      v
 Loader
      |
      v
LoadedScriptPack
      |
      v
 Registry
      |
      v
 Runtime Repository
```

The Runtime Representation separates implementation from runtime metadata.

---

# C.9 Exception Flow

```
Failure
   |
   v
Exception Raised
   |
   v
Core Engine
   |
   +------ Recoverable ------> Continue
   |
   +------ Fatal ------------> Initialization Failed
```

The Foundation follows the principle of *Integrity Before Availability*.

---

# C.10 Future Evolution

```
                 Foundation v1.x

                       |
          +------------+-------------+
          |                          |
          v                          v
    Session Layer            Runtime Cache

          |                          |
          +------------+-------------+
                       |
                       v
              Future Runtime Services
```

Future architectural components SHALL extend the Foundation without breaking existing Runtime or Extension APIs.

---

# Appendix D � Design Rationale

## D.1 Scope

This appendix records the architectural rationale behind significant design decisions adopted by the Foundation.

Unlike the normative chapters of this specification, this appendix is informative. It explains the motivation, objectives, and trade-offs that influenced the architecture.

If a conflict exists between this appendix and the normative sections of this specification, the normative sections SHALL take precedence.

---

# D.2 Separation of Responsibilities

The Foundation adopts a responsibility-oriented architecture.

Each Runtime Service owns exactly one primary responsibility.

This separation provides the following benefits:

- Clear architectural boundaries.
- Independent implementation and testing.
- Reduced coupling between components.
- Improved long-term maintainability.

The Foundation intentionally avoids components with overlapping responsibilities.

---

# D.3 Runtime Pipeline

The Foundation processes ScriptPacks through an ordered Runtime Pipeline rather than allowing individual services to interact arbitrarily.

The pipeline provides:

- Predictable execution.
- Deterministic initialization.
- Easier debugging.
- Consistent error handling.

The Runtime Pipeline also simplifies future extension because additional stages can be inserted without redesigning the overall architecture.

---

# D.4 Runtime API

Applications communicate exclusively through the Runtime API.

This architectural boundary isolates applications from internal implementation details.

As a result:

- Internal Runtime Services may evolve independently.
- Applications remain stable across Foundation revisions.
- Compatibility can be preserved more easily.

The Runtime API therefore represents the public contract of the Foundation.

---

# D.5 Extension API

ScriptPacks interact with the Foundation through the BaseScriptPack interface.

Using an explicit architectural contract provides several advantages:

- Consistent ScriptPack implementation.
- Reliable validation.
- Clear extension points.
- Stable ecosystem growth.

The Foundation intentionally prefers explicit contracts over implicit behavior.

---

# D.6 Runtime Representation

The Foundation separates ScriptPack implementation from runtime metadata.

Instead of exposing implementation objects directly to Runtime Services, the Loader produces a Runtime Representation.

This design:

- Decouples runtime management from implementation details.
- Simplifies runtime bookkeeping.
- Supports future metadata expansion without affecting ScriptPack implementations.

---

# D.7 Validation Before Registration

Validation is performed before a ScriptPack becomes part of the Runtime Repository.

This decision prevents invalid ScriptPacks from entering the runtime.

Consequently:

- Registry integrity is preserved.
- Runtime behavior becomes more predictable.
- Failures are detected during initialization rather than execution.

---

# D.8 Integrity Before Availability

The Foundation prioritizes runtime integrity over partial availability.

If a fatal architectural inconsistency is detected during initialization, the Foundation SHALL refuse to enter operational state.

Although this approach may temporarily reduce availability, it significantly improves runtime reliability and architectural correctness.

---

# D.9 Evolution Without Disruption

The Foundation is designed for incremental evolution.

Future architectural components should extend the Foundation rather than replace existing contracts.

Examples include:

- Session Layer
- Runtime Cache
- Package Repository
- Dependency Management

This philosophy minimizes disruption while allowing the architecture to grow over time.

---

# D.10 Documentation as an Architectural Asset

The Foundation treats documentation as a first-class engineering artifact.

Architecture, contracts, responsibilities, and rationale are documented alongside the implementation.

This approach:

- Preserves architectural knowledge.
- Reduces dependency on individual contributors.
- Improves maintainability.
- Facilitates community participation.

Documentation is considered part of the architecture rather than a description written after implementation.

---

# Appendix E � Document Status and Revision History

## E.1 Scope

This appendix records the publication status and revision history of this specification.

The purpose of this appendix is to provide traceability for architectural changes introduced between document revisions.

---

# E.2 Document Status

| Version | Status | Description |
|----------|--------|-------------|
| 0.x | Working Draft | Internal development and architectural exploration. |
| 1.0 | Initial Release | First stable Foundation Architecture Specification. |
| 1.x | Maintenance | Editorial improvements and backward-compatible updates. |
| 2.x | Major Revision | Architectural changes requiring compatibility review. |

---

# E.3 Revision History

| Version | Date | Summary |
|----------|------|---------|
| 0.1 | YYYY-MM-DD | Initial document structure. |
| 0.2 | YYYY-MM-DD | Building Blocks introduced. |
| 0.3 | YYYY-MM-DD | Runtime Services formalized. |
| 0.4 | YYYY-MM-DD | Runtime Pipeline specified. |
| 0.5 | YYYY-MM-DD | Runtime API defined. |
| 0.6 | YYYY-MM-DD | Extension API defined. |
| 0.7 | YYYY-MM-DD | Exception Model introduced. |
| 0.8 | YYYY-MM-DD | Security considerations added. |
| 0.9 | YYYY-MM-DD | Future evolution documented. |
| 1.0 | YYYY-MM-DD | Initial public specification. |

---

# E.4 Versioning Policy

Editorial improvements MAY be introduced without affecting the architectural version.

Normative architectural changes SHALL require a new specification revision.

Backward-incompatible architectural changes SHOULD result in a new major specification version.

---

# E.5 Change Classification

Changes to this specification are classified as follows.

### Editorial

Changes that improve readability without modifying architectural meaning.

Examples:

- Grammar corrections
- Formatting improvements
- Clarifications

---

### Normative

Changes affecting architectural behavior or requirements.

Examples:

- New Runtime Service
- Modified Runtime API
- Updated Extension API
- Compatibility policy changes

---

### Informative

Changes affecting explanatory material only.

Examples:

- Additional examples
- Improved diagrams
- Expanded rationale

---