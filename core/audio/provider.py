"""
Audio provider interface.

===============================================================================

Module:
    core.services.audio.provider

Module Type:
    Abstract Base Class

Purpose:
    Defines the interface implemented by all
    audio providers.

Responsibilities:
    - Generate audio files.
    - Report provider availability.

Notes:
    Audio providers SHALL remain independent
    from the user interface.

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from pathlib import Path


class AudioProvider(ABC):
    """
    Base class for all audio providers.
    """

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Return the provider name.
        """

    @abstractmethod
    def generate(
        self,
        text: str,
        destination: Path,
    ) -> Path:
        """
        Generate an audio file.

        Parameters
        ----------
        text:
            Text to synthesize.

        destination:
            Output audio file.

        Returns
        -------
        Path
            Generated audio file.
        """

    @abstractmethod
    def is_available(
        self,
    ) -> bool:
        """
        Return whether this provider
        is available.
        """