"""
Audio playback component.

===============================================================================

Module:
    core.audio.player

Module Type:
    Audio Framework

Purpose:
    Plays audio files.

Responsibilities:
    - Play an audio file.
    - Validate file existence.

Notes:
    This component is independent from
    providers, cache, ScriptPack,
    and CoreEngine.

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from playsound3 import playsound


class AudioPlayer:
    """
    Audio playback component.
    """

    def play(
        self,
        path: Path,
    ) -> None:
        """
        Play an audio file.

        Parameters
        ----------
        path:
            Audio file path.

        Returns
        -------
        None

        Raises
        ------
        FileNotFoundError
            If the audio file does not exist.
        """

        if not path.exists():

            raise FileNotFoundError(
                path,
            )

        playsound(
            str(path),
        )