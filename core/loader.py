"""
===============================================================================

Aksara Nusantara

Module:
    core.loader

Module Type:
    Core Service

Purpose:
    Loads validated ScriptPack implementations into the Core Engine.

Implements:
    AN-STD-001
    Section 13 — Script Loader

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

import importlib.util
import json
from pathlib import Path
from typing import Any

# =============================================================================
# Third-party Packages
# =============================================================================

# None

# =============================================================================
# Local Project Imports
# =============================================================================

from core.exceptions import LoaderError
from core.scriptpack import BaseScriptPack


class ScriptPackLoader:
    """
    Loads validated ScriptPack implementations.

    The ScriptPackLoader is responsible for importing a validated
    ScriptPack and creating an instance of its BaseScriptPack
    implementation.

    The loader SHALL NOT perform validation or registration.
    """

    def load(
        self,
        package_path: Path
    ) -> BaseScriptPack:
        """
        Load a validated ScriptPack.

        Parameters
        ----------
        package_path:
            Path to the ScriptPack directory.

        Returns
        -------
        BaseScriptPack
            Loaded ScriptPack implementation.

        Raises
        ------
        LoaderError
            If the ScriptPack cannot be loaded.
        """
        manifest = self._load_manifest(package_path)

        module = self._import_module(
            package_path,
            manifest,
        )

        return self._create_instance(module)

    def _load_manifest(
        self,
        package_path: Path
    ) -> dict[str, Any]:
        raise NotImplementedError

    def _import_module(
        self,
        package_path: Path,
        manifest: dict[str, Any]
    ):

    def _create_instance(
        self,
        module
    ) -> BaseScriptPack:
        raise NotImplementedError