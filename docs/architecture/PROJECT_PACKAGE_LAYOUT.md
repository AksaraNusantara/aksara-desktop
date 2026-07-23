# Project Package Layout

**Document ID:** AN-ARC-003  
**Status:** Draft v1.0  
**Owner:** Aksara Nusantara Project  
**Last Updated:** 2026-07-23

---

# 1. Purpose

This document defines the Python package layout for the Aksara Nusantara ecosystem.

Its purpose is to establish a clean separation between the project repository, the Python source code, the Core Engine, ScriptPack implementations, and application-specific components.

This layout serves as the foundation for future desktop, web, mobile, and command-line applications.

---

# 2. Design Principles

The package layout SHALL follow these principles:

- separation of responsibilities;
- clear package boundaries;
- scalability;
- maintainability;
- traceability;
- future extensibility.

Repository layout and Python package layout SHALL be treated as separate architectural concerns.

---

# 3. Repository Layout

The repository SHALL contain project resources such as:

- documentation;
- assets;
- profiles;
- source code;
- tests;
- examples.

Python source code SHOULD reside inside the `src/` directory.

---

# 4. Python Package Layout

All Python packages SHALL reside under the `src/` directory.

The root Python package SHALL represent the Aksara Nusantara ecosystem.

Example:

```text
src/
    aksara_nusantara/
```

Applications SHOULD import modules from the root package instead of accessing internal files directly.

---

# 5. Root Package

The root package represents the public Python namespace of the ecosystem.

Example:

```python
import aksara_nusantara
```

or

```python
from aksara_nusantara.core import CoreEngine
```

The root package SHALL expose the public API of the framework.

---

# 6. Internal Packages

The root package MAY contain packages such as:

- core
- ui
- data
- utils
- widgets
- applications

Additional packages MAY be introduced in future versions.

---

# 7. Core Package

The `core` package SHALL contain the runtime engine of the ecosystem.

Typical modules include:

- engine
- scriptpack
- registry
- validator
- loader

The Core package SHALL NOT depend on graphical user interface components.

---

# 8. User Interface Packages

Graphical user interface components SHALL remain independent from the Core Engine.

Examples include:

- Desktop GUI
- Web UI
- Mobile UI
- Command Line Interface

Applications SHALL communicate with the Core Engine through its public API.

---

# 9. ScriptPack Packages

Individual ScriptPacks SHOULD remain independent from the Core Engine implementation.

ScriptPacks SHALL communicate with the Core Engine only through the interfaces defined by the ScriptPack Specification.

---

# 10. Import Strategy

Applications SHOULD import public APIs from the root package.

Example:

```python
from aksara_nusantara.core import CoreEngine
```

Applications SHOULD NOT import internal implementation modules unless explicitly documented.

---

# 11. Packaging

The package layout SHOULD support future publication as a standard Python package.

Typical installation MAY use:

```bash
pip install aksara-nusantara
```

The Python import namespace MAY differ from the package distribution name.

Example:

Distribution:

```text
aksara-nusantara
```

Import:

```python
import aksara_nusantara
```

---

# 12. Backward Compatibility

Future package reorganizations SHOULD preserve the public API whenever practical.

Internal module organization MAY evolve without affecting applications.

---

# 13. Future Evolution

Future versions MAY introduce additional packages including:

- marketplace
- cloud
- synchronization
- plugin management
- analytics

Such additions SHOULD preserve the overall architectural principles defined in this document.

---

# 14. Conformance

Implementations claiming compliance with this document SHALL follow the package organization principles described herein.

Alternative implementations MAY extend the package layout provided they preserve compatibility with the public API.
