"""
===============================================================================

Aksara Nusantara

Module:
    core.scriptpack

Purpose:
    Defines the abstract base interface for all ScriptPack implementations.

Implements:
    AN-STD-001
    Section 11 - BaseScriptPack Interface

References:
    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md
    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from pathlib import Path


# -----------------------------------------------------------------------------
# Implements:
#
# AN-STD-001
# Section 11
# BaseScriptPack Interface
# -----------------------------------------------------------------------------
class BaseScriptPack(ABC):
    """
    Abstract base class for all ScriptPack implementations.

    Every ScriptPack SHALL inherit from this class and implement
    the required interface defined by the ScriptPack Specification.

    This class defines the minimum contract required by the
    Aksara Nusantara Core Engine.
    """
    @property
    def root_path(
        self,
    ) -> Path:
        """
        Return the root directory of the ScriptPack.

        Returns
        -------
        Path
            Absolute path to the ScriptPack root.
        """

        return self._root_path

    @property
    def data_path(
        self,
    ) -> Path:
        """
        Return the data directory.

        Returns
        -------
        Path
            Data directory.
        """

        return (
            self.root_path
            / "data"
        )

    @property
    def assets_path(
        self,
    ) -> Path:
        """
        Return the assets directory.

        Returns
        -------
        Path
            Assets directory.
        """

        return (
            self.root_path
            / "assets"
        )

    @property
    def generated_path(
        self,
    ) -> Path:
        """
        Return the generated runtime directory.

        This directory stores runtime-generated
        resources such as synthesized audio,
        thumbnails, indexes, and other cached
        artifacts.

        Returns
        -------
        Path
            Generated directory.
        """

        return (
            self.root_path
            / "generated"
        )

    @abstractmethod
    def get_characters(self) -> list[dict]:
        """
        Return the complete collection of characters provided
        by the ScriptPack.
        """
        raise NotImplementedError

    @abstractmethod
    def register_assets(self) -> None:
        """
        Register UI assets owned by this ScriptPack.

        This method is invoked by the application
        layer after the Core Engine has finished
        loading ScriptPacks.

        Typical assets include fonts, icons, and
        other GUI-related resources.

        Notes
        -----
        This method may depend on an active
        QApplication instance and therefore
        must not be called from the Core Engine.
        """
        raise NotImplementedError

    @abstractmethod
    def get_characters(self) -> list[dict]:
        """
        Return the characters provided by this ScriptPack.

        Returns
        -------
        list[dict]
            Character definitions currently exposed by the
            ScriptPack.
        """

        raise NotImplementedError

    @abstractmethod
    def get_dataset_name(self) -> str:
        """
        Return the name of the currently loaded character dataset.

        Returns
        -------
        str
            Dataset name without its file extension.

            Examples
            --------
            - nglegena
            - sandhangan
            - pasangan
        """

        raise NotImplementedError

    @abstractmethod
    def get_available_datasets(
        self,
    ) -> list[tuple[str, str]]:
        """
        Return all available datasets.

        Returns
        -------
        list[tuple[str, str]]
            List of (internal_name, display_name).
        """

        raise NotImplementedError


    @abstractmethod
    def set_current_dataset(
        self,
        dataset_name: str,
    ) -> None:
        """
        Set the active dataset.
        """

        raise NotImplementedError


    @abstractmethod
    def get_current_dataset(
        self,
    ) -> str:
        """
        Return the active dataset identifier.
        """

        raise NotImplementedError

    @property
    def metadata(self) -> dict[str, object]:
        """
        Return the ScriptPack metadata.

        Returns
        -------
        dict[str, object]
            Metadata loaded from the ScriptPack manifest.
        """
        return self._metadata

    @metadata.setter
    def metadata(
        self,
        metadata: dict[str, object],
    ) -> None:
        """
        Set the ScriptPack metadata.

        Parameters
        ----------
        metadata:
            Metadata loaded from the ScriptPack manifest.
        """
        self._metadata = metadata

    def get_dataset_name(
        self,
    ) -> str:
        """
        Internal dataset identifier.
        """

        raise NotImplementedError

    def get_dataset_display_name(
        self,
    ) -> str:
        """
        Human-readable dataset name.
        """

        raise NotImplementedError
