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
        package_path: Path,
    ) -> dict[str, Any]:
        """
        Load a ScriptPack manifest.

        Parameters
        ----------
        package_path:
            Path to the ScriptPack directory.

        Returns
        -------
        dict[str, Any]
            Parsed manifest.

        Raises
        ------
        LoaderError
            If the manifest cannot be loaded.
        """
        manifest_path = package_path / "manifest.json"

        try:
            with manifest_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except Exception as exc:
            raise LoaderError(
                f"Failed to load manifest: {manifest_path}"
            ) from exc

    def _import_module(
        self,
        package_path: Path,
        manifest: dict[str, Any],
    ):
        """
        Import the ScriptPack module.

        Parameters
        ----------
        package_path:
            Path to the ScriptPack directory.

        manifest:
            Parsed ScriptPack manifest.

        Returns
        -------
        module
            Imported Python module.

        Raises
        ------
        LoaderError
            If the module cannot be imported.
        """
        entry_point = manifest["entry_point"]

        module_path = package_path / entry_point

        try:
            spec = importlib.util.spec_from_file_location(
                module_path.stem,
                module_path,
            )

            if spec is None or spec.loader is None:
                raise LoaderError(
                    f"Unable to create import specification for '{entry_point}'."
                )

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            return module

        except Exception as exc:
            raise LoaderError(
                f"Failed to import ScriptPack module: '{entry_point}'."
            ) from exc

    def _create_instance(
        self,
        module,
    ) -> BaseScriptPack:
        """
        Create a ScriptPack instance from an imported module.

        Parameters
        ----------
        module:
            Imported ScriptPack module.

        Returns
        -------
        BaseScriptPack
            ScriptPack implementation instance.

        Raises
        ------
        LoaderError
            If no valid ScriptPack implementation is found.
        """
        try:
            for attribute in vars(module).values():

                if (
                    isinstance(attribute, type)
                    and issubclass(attribute, BaseScriptPack)
                    and attribute is not BaseScriptPack
                ):
                    return attribute()

            raise LoaderError(
                "No BaseScriptPack implementation found."
            )

        except LoaderError:
            raise

        except Exception as exc:
            raise LoaderError(
                "Failed to create ScriptPack instance."
            ) from exc