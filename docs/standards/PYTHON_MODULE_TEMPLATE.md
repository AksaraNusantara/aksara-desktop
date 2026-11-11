# AN-STD-002

# Python Module Template

---

## 1. Purpose

This document defines the standard structure for all Python modules within the Aksara Nusantara project.

Its goals are to:

- ensure consistency;
- improve readability;
- simplify code reviews;
- improve traceability;
- reduce maintenance cost.

---

## 2. Scope

This standard applies to every Python source file contained within the repository.

Examples include:

- core/
- scriptpacks/
- ui/
- data/
- tests/

Unless explicitly documented otherwise, all Python modules SHALL conform to this standard.

---

## 3. Standard Module Layout

Every Python module SHALL follow the structure below.

1. Module Header
2. Imports
3. Module-Level Constants (optional)
4. Public Classes
5. Private Helper Functions (optional)
6. Public Functions (optional)

The overall layout SHALL remain consistent across the repository.

---

## 4. Module Header

Every module SHALL begin with a standardized documentation header.

Example:

```python
"""
===============================================================================

Aksara Nusantara

Module:
    core.example_service

Module Type:
    Core Service

Purpose:
    Demonstrates the standard Python module structure.

Implements:
    AN-STD-002

References:
    docs/standards/PYTHON_MODULE_TEMPLATE.md

    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""
```

The header SHALL clearly identify:

- module name;
- module type;
- module purpose;
- implemented standards (if applicable);
- referenced documents;
- copyright information;
- SPDX license identifier.

---

## 5. Import Order

Imports SHALL appear in the following order.

```python
# Standard Library

# Third-party Packages

# Local Project Imports
```

Each group SHOULD be separated by one blank line.

Unused imports SHALL NOT be committed.

---

## 6. Module-Level Constants

Constants SHOULD appear immediately after imports.

Example:

```python
DEFAULT_TIMEOUT = 30
```

Constants SHALL use UPPER_CASE naming.

---

## 7. Class Guidelines

Every public class SHALL include:

- a descriptive class docstring;
- explicit public API;
- type hints where appropriate;
- a single well-defined responsibility.

Classes SHOULD follow the Single Responsibility Principle.

---

## 8. Method Guidelines

Public methods SHALL:

- include a docstring;
- use type hints;
- clearly describe their behavior.

Private methods:

- SHOULD encapsulate implementation details;
- MAY omit type hints when obvious from context.

Methods SHOULD remain small and focused.

---

## 9. Exception Guidelines

Core modules SHALL:

- raise exceptions instead of printing errors;
- never interact directly with the user interface;
- preserve exception context using:

```python
raise ValidationError(...) from exc
```

Exceptions SHOULD be meaningful and specific.

---

## 10. Traceability Guidelines

Modules implementing project standards SHALL identify:

- implemented standard(s);
- implemented specification section(s);
- referenced documents.

Traceability improves long-term maintainability and documentation quality.

---

## 11. Example Module

```python
"""
===============================================================================

Aksara Nusantara

Module:
    core.example_service

Module Type:
    Example Service

Purpose:
    Demonstrates the standard module layout.

Implements:
    AN-STD-002

References:
    docs/standards/PYTHON_MODULE_TEMPLATE.md

===============================================================================
"""

# Standard Library
from pathlib import Path

# Third-party Packages
# None

# Local Project Imports
from core.exceptions import CoreEngineError


DEFAULT_TIMEOUT = 30


class ExampleService:
    """
    Demonstrates the recommended class structure.
    """

    def process(self, path: Path) -> bool:
        """
        Process a resource.

        Parameters
        ----------
        path:
            Resource location.

        Returns
        -------
        bool
            True if successful.
        """
        return self._exists(path)

    def _exists(self, path: Path) -> bool:
        """
        Internal helper.
        """
        return path.exists()
```

The purpose of this example is to demonstrate layout rather than implementation.

---

## 12. Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 2026-07 | Initial version |

---

## 13. Design Principles

Python modules SHOULD follow these principles:

- Single Responsibility Principle (SRP);
- Fail Fast;
- Composition over Inheritance;
- Explicit is better than implicit;
- Small public APIs;
- Stateless services where applicable;
- Traceability over memory.

---

## 14. Conformance

Python modules within the Aksara Nusantara repository SHALL conform to this standard unless explicitly documented otherwise.

Project-specific architectural standards (for example AN-STD-001) take precedence where applicable.