"""
===============================================================================

Aksara Nusantara

Module:
    core.validator

Module Type:
    Core Service

Purpose:
    Provides ScriptPack validation services for the Core Engine.

Implements:
    AN-STD-001
    Section 14 — Script Validation

References:
    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md

    docs/standards/PYTHON_MODULE_TEMPLATE.md

    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

# =============================================================================
# Standard Library
# =============================================================================

import json
from pathlib import Path
from typing import Any
import importlib.util
import inspect

# =============================================================================
# Third-party Packages
# =============================================================================

# None

# =============================================================================
# Local Project Imports
# =============================================================================

from core.exceptions import ValidationError
from core.scriptpack import BaseScriptPack

REQUIRED_MANIFEST_FIELDS: tuple[str, ...] = (
    "identifier",
    "name",
    "version",
    "specification",
    "author",
    "entry_point",
)

class ScriptPackValidator:
    """
    Validates ScriptPack packages against AN-STD-001.
    """

    def validate(self, package_path: Path) -> bool:
        """
        Validate an entire ScriptPack package.

        Parameters
        ----------
        package_path:
            Path to the ScriptPack directory.

        Returns
        -------
        bool
            True if validation succeeds.

        Raises
        ------
        ValidationError
            If validation fails.
        """
        self._validate_directory(package_path)
        manifest = self._validate_manifest(package_path)
        self._validate_required_fields(manifest)
        self._validate_entry_point(
            package_path,
            manifest,
        )
        self._validate_interface(package_path)

        return True

    def _validate_directory(self, package_path: Path) -> None:
        """
        Validate the ScriptPack directory structure.

        Parameters
        ----------
        package_path:
            Path to the ScriptPack directory.

        Raises
        ------
        ValidationError
            If the directory structure is invalid.
        """
        if not package_path.exists():
            raise ValidationError(f"ScriptPack directory does not exist: {package_path}")

        if not package_path.is_dir():
            raise ValidationError(f"ScriptPack path is not a directory: {package_path}")

        required_files = (
            "manifest.json",
            "script.py",
        )

        for filename in required_files:
            if not (package_path / filename).exists():
                raise ValidationError(
                    f"Missing required file: {filename}"
                )

    def _validate_manifest(self, package_path: Path) -> dict[str, Any]:
        """
        Validate and load the ScriptPack manifest.

        Parameters
        ----------
        package_path:
            Path to the ScriptPack directory.

        Returns
        -------
        dict[str, Any]
            Parsed manifest data.

        Raises
        ------
        ValidationError
            If the manifest is missing or invalid.
        """
        manifest_path = package_path / "manifest.json"

        try:
            with manifest_path.open(
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except FileNotFoundError as exc:
            raise ValidationError(
                "Missing manifest.json."
            ) from exc

        except json.JSONDecodeError as exc:
            raise ValidationError(
                "Invalid manifest.json format."
            ) from exc

    def _validate_required_fields(
        self,
        manifest: dict[str, Any]
    ) -> None:
        """
        Validate required manifest fields.

        Parameters
        ----------
        manifest:
            Parsed manifest data.

        Raises
        ------
        ValidationError
            If any required field is missing.
        """
        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in manifest:
                raise ValidationError(
                    f"Missing required manifest field: '{field}'."
                )

    def _validate_entry_point(
        self,
        package_path: Path,
        manifest: dict,
    ) -> None:
        """
        Validate the ScriptPack entry point.
        """

        entry_point = package_path / manifest["entry_point"]

        if not entry_point.is_file():
            raise ValidationError(
                f"Entry point not found: '{manifest['entry_point']}'."
            )

    def _validate_interface(self, package_path: Path) -> None:
        """
        Validate the BaseScriptPack implementation.

        Parameters
        ----------
        package_path:
            Path to the ScriptPack directory.

        Raises
        ------
        ValidationError
            If the ScriptPack implementation is invalid.
        """
        script_path = package_path / "script.py"

        try:
            spec = importlib.util.spec_from_file_location(
                "scriptpack_module",
                script_path
            )

            if spec is None or spec.loader is None:
                raise ValidationError(
                    "Unable to create module specification."
                )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        except Exception as exc:
            raise ValidationError(
                f"Failed to import ScriptPack: {exc}"
            ) from exc

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, BaseScriptPack)
                and obj is not BaseScriptPack
            ):
                return

        raise ValidationError(
            "No BaseScriptPack implementation found."
        )