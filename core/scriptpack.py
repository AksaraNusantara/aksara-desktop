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

SPDX-License-Identifier: MIT

===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


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
        Register all runtime assets required by this ScriptPack.

        This method is invoked by the Core Engine after the
        ScriptPack has been successfully loaded and registered.

        Implementations may register fonts, preload images,
        initialize audio resources, or perform any other
        runtime asset initialization required before use.
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
