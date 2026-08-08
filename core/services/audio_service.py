"""
Audio service.

===============================================================================

Module:
    core.services.audio_service

Module Type:
    Service

Purpose:
    High-level audio orchestration.

Responsibilities:
    - Resolve audio.
    - Generate missing audio.
    - Play audio.

Notes:
    This service delegates all
    responsibilities to the Audio
    Framework components.

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""
from __future__ import annotations

from pathlib import Path

from core.audio import AudioCache
from core.audio import AudioPlayer
from core.audio import AudioResolver
from core.audio import GTTSProvider


class AudioService:
    """
    High-level audio service.
    """

    def __init__(
        self,
        cache_root: Path,
        asset_root: Path | None = None,
    ) -> None:
        """
        Initialize audio service.
        """
        self._cache = AudioCache(
            cache_root,
        )

        self._provider = GTTSProvider()

        self._player = AudioPlayer()

        self._resolver = AudioResolver(
            asset_root=asset_root,
            cache=self._cache,
        )

    def play(
        self,
        text: str,
    ) -> None:
        """
        Play audio.

        Parameters
        ----------
        text:
            Text to be spoken.

        Returns
        -------
        None
        """
        audio = self._resolver.resolve(text)

        if audio is None:
            if not self._provider.is_available():
                raise RuntimeError("Audio provider is unavailable.")

            audio = self._cache.get_path(text)

            self._provider.generate(
                text=text,
                destination=audio,
            )

        self._player.play(audio)