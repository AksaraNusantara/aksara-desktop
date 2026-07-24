# AN-STD-002

## 1. Purpose

This document defines the standard structure for all Python modules
within the Aksara Nusantara project.

Its goals are:

- Ensure consistency
- Improve readability
- Simplify code reviews
- Improve traceability
- Reduce maintenance cost


## 2. Scope

This standard applies to every Python source file inside the repository.

Examples:

- core/
- scriptpacks/
- ui/
- tests/


## 3. Standard Module Layout

Every Python module SHALL follow the layout below.

1. Module Header
2. Imports
3. Module Constants (optional)
4. Public Classes
5. Private Functions (optional)
6. Public Functions (optional)

The layout SHALL remain consistent across the entire repository.


##4. Module Header
===============================================================================

Aksara Nusantara

Module:
    core.validator

Module Type:
    Core Service

Purpose:
    Validate ScriptPack implementations.

Implements:
    AN-STD-001
    Section 14

References:
    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md

    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================


##5. Import Order
# Standard Library

# Third-party

# Local Project


##6. Module-Level Constants
DEFAULT_TIMEOUT = 30


##7. Class Guidelines
Every public class SHALL include:

- Class docstring
- Public API
- Type hints


##8. Method Guidelines
Public methods:

- Shall include a docstring.

- Shall use type hints.

- Shall describe workflow.

Private methods:

- Shall perform implementation details.

- May omit type hints when obvious.


##9. Exception Guidelines
Core modules SHALL:

- Raise exceptions.

- Never print errors.

- Never interact with UI.

- Preserve exception context using

raise ... from exc


##10. Traceability Guidelines
Each module SHALL identify:

Implemented Standard

Implemented Section

Reference Documents


##11. Example Module
Header

?

Imports

?

Class

?

Public Method

?

Private Method


##12. Revision History
| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2026-07 | Initial version |


## 13. Design Principles

Python modules within Aksara Nusantara SHOULD follow these principles:

- Single Responsibility Principle (SRP)
- Fail Fast
- Composition over Inheritance
- Explicit is better than implicit
- Small public API
- Stateless services where applicable
- Traceability over memory
