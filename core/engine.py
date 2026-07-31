"""
===============================================================================

Aksara Nusantara

Module:
    core.engine

Module Type:
    Core Service

Purpose:
    Coordinates the ScriptPack lifecycle within the Core Engine.

Implements:
    AN-STD-001
    Section 15 — Core Engine API

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

from pathlib import Path

# =============================================================================
# Third-party Packages
# =============================================================================

# None

# =============================================================================
# Local Project Imports
# =============================================================================

from core.loader import ScriptPackLoader
from core.registry import ScriptPackRegistry
from core.scriptpack import BaseScriptPack
from core.validator import ScriptPackValidator


class CoreEngine:
    """
    Coordinates the ScriptPack lifecycle.

    The CoreEngine orchestrates discovery, validation,
    loading, and registration of ScriptPacks.

    The CoreEngine SHALL NOT implement
    ScriptPack-specific logic.
    """

    def __init__(self) -> None:
        """
        Initialize the Core Engine.

        The CoreEngine owns the Validator, Loader,
        and Registry services.

        These services remain independent and are
        coordinated exclusively by the CoreEngine.
        """
        self._validator = ScriptPackValidator()
        self._loader = ScriptPackLoader()
        self._registry = ScriptPackRegistry()

    def initialize(
        self,
        scriptpacks_directory: Path,
    ) -> None:
        """
        Initialize the Core Engine.

        Parameters
        ----------
        scriptpacks_directory:
            Directory containing ScriptPack packages.

        Raises
        ------
        EngineError
            Reserved for future versions.
        """
        packages = self._discover(scriptpacks_directory)

        for package in packages:
            self._validator.validate(package)
            loaded = self._loader.load(package)
            identifier = loaded.manifest["identifier"]
            self._registry.register(
                identifier,
                loaded.instance,
            )
            #
            # Register runtime assets owned by the ScriptPack.
            #

            loaded.instance.register_assets()

    def _discover(
        self,
        scriptpacks_directory: Path,
    ) -> list[Path]:
        """
        Discover available ScriptPack packages.

        Parameters
        ----------
        scriptpacks_directory:
            Directory containing ScriptPack packages.

        Returns
        -------
        list[Path]
            List of candidate ScriptPack directories.
        """
        if not scriptpacks_directory.exists():
            return []

        return sorted(
            path
            for path in scriptpacks_directory.iterdir()
            if path.is_dir()
        )

    def list(self) -> list[str]:
        """
        Return identifiers of all loaded ScriptPacks.

        Returns
        -------
        list[str]
            List of ScriptPack identifiers.
        """
        return self._registry.list()

    def get(
        self,
        identifier: str,
    ) -> BaseScriptPack:
        """
        Retrieve a loaded ScriptPack.

        Parameters
        ----------
        identifier:
            ScriptPack identifier.

        Returns
        -------
        BaseScriptPack
        Loaded ScriptPack implementation.
        """
        return self._registry.get(identifier)

    def get_characters(
        self,
        identifier: str,
    ) -> list[dict]:
        """
        Return all characters from a ScriptPack.
        """

        return self.get(identifier).get_characters()