"""
Audio path resolver.

===============================================================================

Module:
    core.audio.resolver

Module Type:
    Audio Framework

Purpose:
    Resolve the best audio file
    for playback.

Responsibilities:
    - Prefer ScriptPack assets.
    - Fallback to generated cache.

Notes:
    This component never generates
    audio and never plays audio.

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from .cache import AudioCache


class AudioResolver:
    """
    Resolve audio file paths.
    """

    def __init__(
        self,
        asset_root: Path | None,
        cache: AudioCache,
    ) -> None:
        """
        Initialize resolver.
        """

        self._asset_root = asset_root
        self._cache = cache

    def resolve(
        self,
        text: str,
    ) -> Path | None:
        """
        Resolve audio path.

        Parameters
        ----------
        text:
            Audio text.

        Returns
        -------
        Path | None
            Best available audio.
        """

        if self._asset_root is not None:

            asset = (
                self._asset_root
                / f"{text}.mp3"
            )

            if asset.exists():

                return asset

        cache = self._cache.get_path(
            text,
        )

        if cache.exists():

            return cache

        return None