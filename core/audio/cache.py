"""
Audio cache management.

===============================================================================

Module:
    core.audio.cache

Module Type:
    Audio Framework

Purpose:
    Manages runtime audio cache.

Responsibilities:
    - Create cache directory.
    - Generate cache file paths.
    - Check cached audio.
    - Clear cache.

Notes:
    This component is independent from
    CoreEngine, ScriptPack,
    providers, and playback.

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import hashlib
import shutil


class AudioCache:
    """
    Runtime audio cache.
    """

    def __init__(
        self,
        root: Path,
    ) -> None:
        """
        Initialize cache.
        """

        self._root = root

        self.ensure_directory()

    def ensure_directory(
        self,
    ) -> None:
        """
        Ensure cache directory exists.
        """

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def get_path(
        self,
        text: str,
        extension: str = ".mp3",
    ) -> Path:
        """
        Return cache file path.
        """

        filename = hashlib.sha256(
            text.encode(
                "utf-8",
            )
        ).hexdigest()

        return (
            self._root
            / f"{filename}{extension}"
        )

    def exists(
        self,
        text: str,
    ) -> bool:
        """
        Return whether cached audio exists.
        """

        return self.get_path(
            text,
        ).exists()

    def clear(
        self,
    ) -> None:
        """
        Remove all cached audio.
        """

        if self._root.exists():

            shutil.rmtree(
                self._root,
            )

        self.ensure_directory()