"""
===============================================================================

Aksara Nusantara

Module:
    core.registry

Module Type:
    Core Service

Purpose:
    Provides ScriptPack registry services for the Core Engine.

Implements:
    AN-STD-001
    Section 12 — Script Registry

References:
    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md

    docs/standards/PYTHON_MODULE_TEMPLATE.md

    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

# =============================================================================
# Standard Library
# =============================================================================

# None

# =============================================================================
# Third-party Packages
# =============================================================================

# None

# =============================================================================
# Local Project Imports
# =============================================================================

from core.exceptions import RegistryError
from core.scriptpack import BaseScriptPack


class ScriptPackRegistry:
    """
    Stores and manages validated ScriptPack implementations.
    """

    def __init__(self) -> None:
        """
        Initialize an empty ScriptPack registry.
        """
        self._registry: dict[str, BaseScriptPack] = {}

    def register(
        self,
        identifier: str,
        scriptpack: BaseScriptPack,
    ) -> None:
        """
        Register a validated ScriptPack.

        Parameters
        ----------
        scriptpack:
            ScriptPack implementation.

        Raises
        ------
        RegistryError
            If the ScriptPack is already registered.
        """
        
        if identifier in self._registry:
            raise RegistryError(
                f"ScriptPack '{identifier}' is already registered."
            )

        self._registry[identifier] = scriptpack

    def unregister(
        self,
        identifier: str
    ) -> None:
        """
        Unregister a ScriptPack.

        Parameters
        ----------
        identifier:
            ScriptPack identifier.

        Raises
        ------
        RegistryError
            If the ScriptPack is not registered.
        """
        try:
            del self._registry[identifier]

        except KeyError as exc:
            raise RegistryError(
                f"Unknown ScriptPack: '{identifier}'."
            ) from exc

    def get(
        self,
        identifier: str
    ) -> BaseScriptPack:
        """
        Retrieve a registered ScriptPack.

        Parameters
        ----------
        identifier:
            ScriptPack identifier.

        Returns
        -------
        BaseScriptPack
            The registered ScriptPack implementation.

        Raises
        ------
        RegistryError
            If the ScriptPack is not registered.
        """
        try:
            return self._registry[identifier]

        except KeyError as exc:
            raise RegistryError(
                f"Unknown ScriptPack: '{identifier}'."
            ) from exc

    def contains(
        self,
        identifier: str
    ) -> bool:
         return identifier in self._registry

    def list(self) -> list[str]:
        """
        Return the identifiers of all registered ScriptPacks.

        Returns
        -------
        list[str]
            Registered ScriptPack identifiers.
        """
        return sorted(self._registry.keys())

    def clear(self) -> None:
        """
        Remove all registered ScriptPacks.
        """
        self._registry.clear()
