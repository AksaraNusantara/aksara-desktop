# ADR-0001

# Separate ScriptPack Discovery from Activation

---

## Document Information

| Item | Value |
|------|-------|
| ADR | 0001 |
| Title | Separate ScriptPack Discovery from Activation |
| Status | Accepted |
| Author | Aksara Nusantara Project |
| Date | 2026-07-31 |
| Supersedes | None |
| Superseded By | None |
| Related Documents | CORE_ARCHITECTURE.md, PROJECT_BLUEPRINT.md, SCRIPTPACK_INTERFACE_SPECIFICATION.md |

---

# 1. Introduction

This Architecture Decision Record (ADR) documents the decision to separate **ScriptPack Discovery** from **ScriptPack Activation** within the Aksara Nusantara Foundation runtime.

Foundation v1.0 successfully established a modular runtime capable of discovering, validating, loading, and registering ScriptPacks during application initialization. The implementation fulfilled the original architectural objectives and demonstrated that the Foundation could operate independently from any specific writing system.

As the project evolved toward a reusable ecosystem supporting multiple writing systems, it became evident that the responsibilities of **discovering available ScriptPacks** and **activating a ScriptPack for runtime use** represent two distinct architectural concerns.

This document records the decision to formally separate these responsibilities, explains the rationale behind the decision, and defines the architectural direction for future Foundation development.

This ADR serves as the authoritative source for this architectural decision. Future revisions to the Foundation specifications SHALL remain consistent with the principles established herein.

---

# 2. Context

Foundation v1.0 defines a deterministic runtime initialization process responsible for preparing the application before user interaction begins.

The runtime currently performs the following sequence.

```text
Application

?

CoreEngine.initialize()

?

Discover ScriptPacks

?

Validate ScriptPacks

?

Load ScriptPacks

?

Register Runtime Services

?

Ready
```

During initialization, every discovered ScriptPack is instantiated and prepared for immediate runtime use.

This architecture was intentionally designed to achieve several objectives.

- deterministic startup behavior;
- centralized lifecycle management;
- complete runtime availability before application execution;
- simplified desktop integration during the initial development phase.

The implementation has proven reliable and successfully fulfills the requirements defined by Foundation v1.0.

At the time of writing, the Foundation assumes that the application will immediately use one of the available ScriptPacks after initialization.

Consequently, ScriptPack discovery and ScriptPack activation are effectively treated as a single operation.

This assumption was appropriate during the early stages of the project when only a limited number of ScriptPacks existed and the desktop application primarily targeted a single writing system.

However, the long-term vision of Aksara Nusantara extends beyond a single-script application.

The Foundation is intended to support an ecosystem in which multiple writing systems can coexist, evolve independently, and be consumed by various applications including desktop, mobile, web, command-line, and future platforms.

Within this broader ecosystem, the current runtime lifecycle no longer provides sufficient separation between resource management and application behavior.

---

# 3. Problem Statement

The current runtime lifecycle combines two independent responsibilities.

The first responsibility is discovering and preparing ScriptPacks that are available within the runtime environment.

The second responsibility is determining which ScriptPack should actively provide writing-system services to an application.

Although these operations currently occur together, they address fundamentally different architectural concerns.

Discovery concerns **resource availability**.

Activation concerns **application behavior**.

Treating these responsibilities as a single operation introduces several limitations.

## 3.1 Coupled Runtime Responsibilities

The Foundation cannot distinguish between ScriptPacks that are merely installed and those that are actively used.

As a result, runtime state becomes unnecessarily coupled to initialization behavior.

---

## 3.2 Reduced Scalability

As additional ScriptPacks become available, the runtime performs increasing amounts of work during application startup regardless of whether those ScriptPacks will ever be used.

This approach scales poorly for a plugin-oriented architecture.

---

## 3.3 Limited Application Flexibility

Applications cannot determine which ScriptPack should become active after initialization.

Instead, runtime behavior is implicitly determined by the initialization sequence.

This limits future application workflows, including:

- runtime ScriptPack selection;
- user-configurable writing systems;
- project-specific ScriptPack preferences;
- dynamic ScriptPack switching;
- platform-specific activation strategies.

---

## 3.4 Architectural Ambiguity

The existing lifecycle does not explicitly distinguish between:

- ScriptPacks that are available to the Foundation; and
- the ScriptPack currently serving runtime requests.

This ambiguity complicates both the conceptual architecture and future API design.

The Foundation requires a clearer runtime model in which resource discovery and runtime activation are recognized as separate responsibilities.

---

## 3.5 Long-Term Ecosystem Goals

The Aksara Nusantara ecosystem is intended to support an expanding collection of independently developed ScriptPacks.

Future capabilities may include:

- community-developed ScriptPacks;
- downloadable ScriptPack repositories;
- marketplace integration;
- optional ScriptPack installation;
- third-party extensions.

These scenarios require the Foundation to manage a collection of available ScriptPacks independently from the ScriptPack currently selected by an application.

The current initialization model does not adequately support these long-term architectural goals.

---

# 4. Decision

The Foundation runtime SHALL separate **ScriptPack Discovery** from **ScriptPack Activation**.

These operations SHALL be treated as two independent phases of the runtime lifecycle.

The Discovery phase SHALL establish the complete set of ScriptPacks available to the Foundation.

The Activation phase SHALL establish the single ScriptPack currently providing writing-system services to an application.

The Foundation SHALL distinguish between the following runtime concepts.

## 4.1 Available ScriptPack

An **Available ScriptPack** is a ScriptPack that has been successfully:

- discovered;
- validated;
- registered within the Foundation runtime.

An Available ScriptPack SHALL be eligible for activation.

An Available ScriptPack SHALL NOT be considered active solely because it exists within the runtime.

Multiple Available ScriptPacks MAY coexist simultaneously.

---

## 4.2 Active ScriptPack

An **Active ScriptPack** is the ScriptPack currently selected by an application to provide runtime services.

The Active ScriptPack SHALL serve as the authoritative provider for:

- character definitions;
- transliteration;
- rendering resources;
- fonts;
- audio assets;
- metadata;
- other writing-system services defined by the ScriptPack interface.

At any given time, a single application instance SHALL have no more than one Active ScriptPack.

Changing the Active ScriptPack SHALL be considered a runtime operation rather than an initialization operation.

---

## 4.3 Discovery Phase

The Discovery phase SHALL be responsible for identifying ScriptPacks that are available within the runtime environment.

The Foundation SHALL perform the following operations during Discovery.

- locate ScriptPack packages;
- validate package structure;
- validate manifests;
- validate runtime compatibility;
- collect metadata;
- register ScriptPack information.

The Discovery phase SHALL NOT activate any ScriptPack.

---

## 4.4 Activation Phase

The Activation phase SHALL begin only after an explicit request from the application.

Activation SHALL establish the runtime context required for a ScriptPack to provide writing-system services.

The Foundation SHALL expose an activation mechanism through the Runtime API.

Applications SHALL determine when activation occurs.

The Foundation SHALL NOT automatically select an Active ScriptPack unless explicitly defined by application policy.

---

# 5. Rationale

The decision to separate Discovery from Activation follows established software architecture principles.

Discovery and Activation solve different problems.

Discovery answers the question:

> "Which ScriptPacks are available?"

Activation answers the question:

> "Which ScriptPack should the application use?"

Because these questions address different responsibilities, they SHOULD remain independent.

Separating these concerns results in a runtime architecture that is easier to understand, easier to maintain, and easier to extend.

---

## 5.1 Separation of Responsibilities

Discovery is a Foundation responsibility.

Activation is an application responsibility.

The Foundation manages resources.

Applications determine behavior.

Separating these responsibilities reduces coupling between the runtime and application-specific workflows.

---

## 5.2 Single Responsibility Principle

The decision reinforces the Single Responsibility Principle at the runtime level.

The Foundation SHALL manage ScriptPack availability.

Applications SHALL determine ScriptPack usage.

Neither component should assume the responsibilities of the other.

---

## 5.3 Open/Closed Principle

Separating Discovery from Activation allows new application workflows to be introduced without modifying the Discovery process.

Future applications may choose different activation strategies while continuing to use the same Foundation.

Examples include:

- desktop applications;
- command-line tools;
- web services;
- mobile applications;
- educational platforms.

The Foundation therefore remains open for extension while remaining closed for modification.

---

## 5.4 Scalability

As the number of ScriptPacks increases, Discovery continues to describe runtime availability.

Activation remains independent of the total number of installed ScriptPacks.

This separation prevents runtime behavior from becoming increasingly coupled to initialization complexity.

---

## 5.5 Ecosystem Alignment

The long-term objective of the Aksara Nusantara ecosystem is to support multiple independent writing systems.

This objective naturally introduces two different runtime concepts.

The first concept is the collection of ScriptPacks installed within a Foundation instance.

The second concept is the ScriptPack currently serving an application.

Separating Discovery from Activation reflects this conceptual distinction directly within the runtime architecture.

---

# 6. Architectural Impact

This decision changes the conceptual runtime lifecycle of the Foundation.

The previous lifecycle can be summarized as follows.

```text
Initialize

?

Discover

?

Validate

?

Load

?

Register

?

Ready
```

The revised lifecycle becomes:

```text
Initialize

?

Discover

?

Validate

?

Register Available ScriptPacks

?

Foundation Ready

?

Application selects ScriptPack

?

Activate ScriptPack

?

Application Runtime
```

Initialization now prepares the runtime environment.

Activation prepares the application context.

These responsibilities SHALL remain independent.

---

# 7. Runtime Lifecycle

Following this decision, the Foundation runtime SHALL consist of two major phases.

## Phase 1 — Runtime Initialization

Responsible for:

- discovery;
- validation;
- registration;
- metadata preparation.

Result:

The Foundation knows every available ScriptPack.

No ScriptPack is active.

---

## Phase 2 — Runtime Activation

Responsible for:

- selecting a ScriptPack;
- creating the active runtime context;
- exposing writing-system services.

Result:

The application communicates exclusively with the Active ScriptPack.

Applications SHALL interact only with the Active ScriptPack during normal execution.

Direct interaction with inactive ScriptPacks SHOULD be avoided except for management purposes.

---

# 8. Runtime API

This ADR defines the conceptual runtime behavior.

The exact programming interface SHALL be specified by the Foundation Runtime API.

Future Foundation versions SHOULD provide capabilities equivalent to the following conceptual interface.

```python
initialize()

available_scriptpacks()

active_scriptpack()

activate(identifier)
```

The semantics of these operations are defined below.

---

## 8.1 initialize()

The `initialize()` operation SHALL prepare the Foundation runtime.

Initialization SHALL perform the following tasks.

- discover ScriptPacks;
- validate ScriptPacks;
- register ScriptPack metadata;
- prepare runtime services.

The operation SHALL NOT activate a ScriptPack.

Upon successful completion:

- the Foundation SHALL be ready for use;
- Available ScriptPacks SHALL be known;
- no Active ScriptPack SHALL exist.

---

## 8.2 available_scriptpacks()

This operation SHALL return the collection of ScriptPacks known to the Foundation.

The returned information SHOULD contain sufficient metadata for an application to present ScriptPack choices to the user.

Typical metadata MAY include:

- identifier;
- display name;
- version;
- supported writing system;
- author;
- description.

The returned collection SHALL NOT imply activation.

---

## 8.3 activate(identifier)

The `activate()` operation SHALL establish the Active ScriptPack.

Activation SHALL verify that the requested ScriptPack exists within the Available ScriptPack registry.

If activation succeeds:

- the requested ScriptPack becomes Active;
- runtime services SHALL be provided by the Active ScriptPack;
- previous runtime context MAY be replaced.

If activation fails:

- the previously active ScriptPack SHALL remain unchanged.

The Foundation SHALL report activation failures using the Foundation exception hierarchy.

---

## 8.4 active_scriptpack()

This operation SHALL return the ScriptPack currently providing runtime services.

Applications SHOULD communicate exclusively through the Active ScriptPack.

Applications SHALL NOT directly instantiate ScriptPack implementations.

---

# 9. Consequences

This decision introduces several architectural consequences.

Some are beneficial, while others require additional implementation effort.

---

## 9.1 Advantages

Separating Discovery from Activation provides several long-term benefits.

### Clearer Runtime Model

The Foundation explicitly distinguishes between installed resources and runtime behavior.

The conceptual architecture becomes easier to understand.

---

### Improved Scalability

Runtime initialization no longer assumes immediate use of every available ScriptPack.

Future Foundation implementations can optimize activation independently from discovery.

---

### Better Application Flexibility

Applications gain control over ScriptPack selection.

Different applications may implement different activation strategies without modifying the Foundation.

Examples include:

- automatic activation;
- user-selected activation;
- project-specific activation;
- configuration-based activation.

---

### Stronger Modularity

The Foundation manages ScriptPacks.

Applications manage workflow.

The separation reduces architectural coupling between runtime infrastructure and application behavior.

---

### Future Extensibility

The architecture naturally supports future capabilities such as:

- ScriptPack marketplaces;
- downloadable ScriptPacks;
- user-installed extensions;
- runtime ScriptPack switching;
- cloud-hosted repositories.

These capabilities can be introduced without redesigning the runtime lifecycle.

---

## 9.2 Trade-offs

The decision also introduces additional complexity.

The Runtime API becomes larger.

Applications become responsible for selecting an Active ScriptPack.

Foundation specifications require revision.

Desktop applications require an activation workflow before writing-system services become available.

These trade-offs are considered acceptable because they improve long-term maintainability and architectural clarity.

---

# 10. Alternatives Considered

Several architectural alternatives were evaluated.

---

## Alternative A — Activate Every ScriptPack During Initialization

Under this approach, initialization would continue to instantiate every ScriptPack.

### Advantages

- simple lifecycle;
- minimal Runtime API.

### Disadvantages

- startup cost grows with the number of ScriptPacks;
- poor scalability;
- no distinction between availability and usage.

### Decision

Rejected.

This approach does not support the long-term ecosystem vision.

---

## Alternative B — Select ScriptPack During Startup

Under this approach, applications would display a startup dialog or splash screen allowing the user to choose a ScriptPack before entering the application.

### Advantages

- explicit user choice;
- simple runtime model.

### Disadvantages

- additional startup step;
- interrupts application launch;
- unsuitable for automated workflows and command-line environments.

### Decision

Rejected.

Activation should remain an application concern rather than a mandatory startup requirement.

---

## Alternative C — Separate Discovery from Activation

Discovery prepares the runtime.

Applications determine activation.

### Advantages

- scalable;
- modular;
- platform-independent;
- flexible.

### Disadvantages

- larger Runtime API;
- requires lifecycle revision.

### Decision

Accepted.

This approach best satisfies the architectural objectives of the Foundation.

---

# 11. Migration Strategy

Migration SHALL proceed incrementally.

The following sequence SHALL be followed.

---

## Step 1

Approve this ADR.

This document becomes the authoritative architectural decision.

---

## Step 2

Revise Foundation specifications.

The following documents SHALL be updated.

- CORE_ARCHITECTURE.md
- SCRIPTPACK_INTERFACE_SPECIFICATION.md

The PROJECT_BLUEPRINT specification remains unaffected because its long-term architectural vision already aligns with this decision.

---

## Step 3

Extend the Runtime API.

The Foundation SHALL expose runtime operations supporting:

- Available ScriptPacks;
- Active ScriptPack;
- activation.

---

## Step 4

Update Desktop Integration.

Desktop applications SHALL obtain writing-system services exclusively through the Active ScriptPack.

Direct assumptions regarding ScriptPack initialization SHALL be removed.

---

## Step 5

Validate Runtime Behavior.

Existing integration tests SHALL be updated to verify:

- Discovery;
- Registration;
- Activation;
- Runtime services.

The Foundation SHALL continue to satisfy all existing functional requirements after migration.

---

# 12. Backward Compatibility

This decision introduces a conceptual change to the Foundation runtime lifecycle.

Applications and components developed for Foundation v1.0 assume that a ScriptPack becomes available for runtime use immediately after initialization.

Following this ADR, initialization and activation become separate runtime responsibilities.

Existing applications MAY require minor modifications to explicitly activate a ScriptPack before requesting writing-system services.

This change is considered acceptable because it improves architectural clarity without altering the fundamental responsibilities of the Foundation.

Migration SHALL be performed in accordance with the strategy defined in this document.

---

# 13. Non-Goals

This Architecture Decision Record intentionally does not define implementation details beyond the architectural level.

In particular, this ADR does NOT define:

- the concrete Runtime API signatures;
- user interface design;
- menu structures;
- desktop workflow;
- mobile workflow;
- command-line workflow;
- marketplace implementation;
- ScriptPack installation mechanisms;
- ScriptPack packaging format.

These topics SHALL be addressed by their respective specifications or future Architecture Decision Records.

---

# 14. Future Considerations

This architectural decision establishes a foundation for future runtime capabilities.

Future Foundation versions MAY introduce:

## Runtime ScriptPack Switching

Applications MAY allow users to activate a different ScriptPack without restarting the application.

---

## ScriptPack Deactivation

The Foundation MAY support releasing resources associated with an Active ScriptPack before activating another.

---

## ScriptPack Dependency Resolution

Future ScriptPacks MAY declare dependencies on shared resources or other ScriptPacks.

Dependency management is outside the scope of this ADR.

---

## Marketplace Integration

Future versions of the ecosystem MAY allow ScriptPacks to be discovered, installed, updated, and removed through a marketplace or repository service.

This capability naturally builds upon the distinction between Available ScriptPacks and the Active ScriptPack.

---

## Remote ScriptPack Repositories

The Foundation MAY support downloading ScriptPacks from remote repositories while preserving the same runtime lifecycle defined by this ADR.

---

## Multiple Application Types

Because Discovery and Activation are independent responsibilities, different application types MAY implement different activation policies.

Examples include:

- desktop applications;
- web applications;
- mobile applications;
- command-line tools;
- educational platforms;
- automated processing services.

The Foundation SHALL remain independent of these application-specific decisions.

---

# 15. References

The following project documents are directly related to this decision.

- CORE_ARCHITECTURE.md
- PROJECT_BLUEPRINT.md
- SCRIPTPACK_INTERFACE_SPECIFICATION.md
- ENGINEERING_PRINCIPLES.md

Future revisions of these documents SHALL remain consistent with the architectural principles established by this ADR.

---

# 16. Decision Summary

This Architecture Decision Record establishes a clear separation between **ScriptPack Discovery** and **ScriptPack Activation**.

The Foundation SHALL manage the discovery, validation, and registration of available ScriptPacks.

Applications SHALL determine which ScriptPack becomes active.

This separation distinguishes runtime infrastructure from application behavior, reinforces established software engineering principles, and improves the scalability, maintainability, and extensibility of the Foundation.

By introducing the concepts of **Available ScriptPacks** and **Active ScriptPack**, the Foundation gains a clearer runtime model capable of supporting the long-term vision of the Aksara Nusantara ecosystem.

This decision SHALL serve as the architectural basis for future revisions of the Foundation runtime and related specifications.

---

## Revision History

| Version | Date | Description |
|----------|------------|---------------------------------------------|
| 1.0 | 2026-07-31 | Initial version. |

---

## Architecture Status

This decision has been accepted.

Implementation SHALL follow this Architecture Decision Record before corresponding specification revisions are performed.

Affected specifications include:

- CORE_ARCHITECTURE.md
- SCRIPTPACK_INTERFACE_SPECIFICATION.md

PROJECT_BLUEPRINT.md is unaffected by this decision.
