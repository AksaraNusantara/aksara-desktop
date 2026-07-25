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
        scriptpack: BaseScriptPack
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
        identifier = scriptpack.get_script_information()["id"]

        if identifier in self._registry:
            raise RegistryError(
                f"ScriptPack '{identifier}' is already registered."
            )

        self._registry[identifier] = scriptpack

    def unregister(
        self,
        identifier: str
    ) -> None:
        raise NotImplementedError

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
        raise NotImplementedError

    def list(self) -> list[str]:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError
