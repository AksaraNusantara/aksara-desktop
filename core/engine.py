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
from collections.abc import Callable

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

        self._listeners: list[Callable[[], None]] = []

        #
        # Runtime state.
        #

        self._active_scriptpack: BaseScriptPack | None = None

    @property
    def active_scriptpack(self) -> BaseScriptPack | None:
        """
        Return the currently active ScriptPack.

        Returns
        -------
        BaseScriptPack | None
            Active ScriptPack instance, or None if no
            ScriptPack has been activated.
        """
        return self._active_scriptpack

    @property
    def has_active_scriptpack(self) -> bool:
        """
        Return True if a ScriptPack is active.
        """
        return self._active_scriptpack is not None

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

    def activate(
        self,
        identifier: str,
    ) -> BaseScriptPack:
        """
        Activate a registered ScriptPack.

        Parameters
        ----------
        identifier:
            ScriptPack identifier.

        Returns
        -------
        BaseScriptPack
            Activated ScriptPack instance.
        """

        scriptpack = self.get(identifier)

        self._active_scriptpack = scriptpack

        self._notify_listeners()

        return scriptpack

    def deactivate(self) -> None:
        """
        Deactivate the current ScriptPack.
        """

        self._active_scriptpack = None

    def get_active_scriptpack(self) -> BaseScriptPack | None:
        """
        Return the currently active ScriptPack.

        Returns
        -------
        BaseScriptPack | None
            The active ScriptPack instance if one has been
            activated; otherwise, ``None``.
        """

        return self._active_scriptpack

    def get_characters(self) -> list[dict]:
        """
        Return the characters provided by the active ScriptPack.

        Returns
        -------
        list[dict]
            A list of character definitions.

        Raises
        ------
        EngineError
            If no ScriptPack is currently active.
        """

        scriptpack = self.get_active_scriptpack()

        if scriptpack is None:
            return []

        return scriptpack.get_characters()

    def get_active_characters(
        self,
    ) -> list[dict]:
        """
        Return characters from the active ScriptPack.

        Returns
        -------
        list[dict]
            Character definitions from the active ScriptPack.

        Raises
        ------
        RuntimeError
            If no ScriptPack has been activated.
        """

        if self._active_scriptpack is None:
            raise RuntimeError(
                "No active ScriptPack."
            )

        return self._active_scriptpack.get_characters()

    def is_active(
        self,
        identifier: str,
    ) -> bool:
        """
        Determine whether the specified ScriptPack is active.

        Parameters
        ----------
        identifier:
            ScriptPack identifier.

        Returns
        -------
        bool
            True if the specified ScriptPack is currently
            active; otherwise False.
        """

        if self._active_scriptpack is None:
            return False

        return (
            self._active_scriptpack.metadata["identifier"]
            == identifier
        )

    def get_current_dataset_name(self) -> str:
        """
        Return the name of the currently loaded character dataset.

        Returns
        -------
        str
            Dataset name (for example ``nglegena``).

        Raises
        ------
        EngineError
            If no ScriptPack is currently active.
        """

        if self._active_scriptpack is None:
            raise EngineError(
                "No active ScriptPack."
            )

        return self._active_scriptpack.get_dataset_name()

    def register_listener(
        self,
        callback: Callable[[], None],
    ) -> None:
        """
        Register a listener that will be notified whenever
        the active ScriptPack changes.

        Parameters
        ----------
        callback:
            Callable invoked after the active ScriptPack
            changes.
        """

        self._listeners.append(callback)

    def _notify_listeners(self) -> None:
        """
        Notify every registered listener.
        """

        for callback in self._listeners:
            callback()

    def get_available_datasets(
        self,
    ) -> list[tuple[str, str]]:
        """
        Return the available datasets from the active ScriptPack.

        Returns
        -------
        list[tuple[str, str]]
            List of (internal_name, display_name).
        """

        scriptpack = self.get_active_scriptpack()

        if scriptpack is None:
            return []

        return scriptpack.get_available_datasets()

    def set_current_dataset(
        self,
        dataset_name: str,
    ) -> None:
        """
        Set the active learning dataset.

        Parameters
        ----------
        dataset_name:
            Internal dataset identifier.
        """

        scriptpack = self.get_active_scriptpack()

        if scriptpack is None:
            return

        scriptpack.set_current_dataset(
            dataset_name,
        )

    def get_current_dataset(
        self,
    ) -> str:
        """
        Return the active dataset identifier.
        """

        scriptpack = self.get_active_scriptpack()

        if scriptpack is None:
            return ""

        return scriptpack.get_current_dataset()

    def get_current_dataset_display_name(
        self,
    ) -> str:
        """
        Return the display name of the active dataset.
        """

        scriptpack = self.get_active_scriptpack()

        if scriptpack is None:
            return ""

        return scriptpack.get_dataset_display_name()
