"""
Google Text-to-Speech audio provider.

===============================================================================

Module:
    core.services.audio.gtts_provider

Module Type:
    Audio Provider

Purpose:
    Implements the Google Text-to-Speech
    provider.

Responsibilities:
    - Generate MP3 files.
    - Report provider availability.

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from gtts import gTTS

from .provider import AudioProvider


class GTTSProvider(AudioProvider):
    """
    Google Text-to-Speech provider.
    """

    @property
    def name(
        self,
    ) -> str:
        """
        Return provider name.

        Returns
        -------
        str
            Provider identifier.
        """

        return "gtts"

    def generate(
        self,
        text: str,
        destination: Path,
    ) -> Path:
        """
        Generate an MP3 file.

        Parameters
        ----------
        text:
            Text to synthesize.

        destination:
            Output MP3 path.

        Returns
        -------
        Path
            Generated MP3 file.
        """

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        speech = gTTS(
            text=text,
            lang="id",
        )

        speech.save(
            str(destination),
        )

        return destination

    def is_available(
        self,
    ) -> bool:
        """
        Return provider availability.

        Returns
        -------
        bool
            Always True when gTTS
            package is installed.
        """

        return True