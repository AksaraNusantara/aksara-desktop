"""
===============================================================================

Aksara Nusantara

Module:
    core.services.audio_service

Purpose:
    Shared text-to-speech service.

Description:
    AudioService provides a simple text-to-speech API for the
    application.

    Version 1.0 uses Microsoft Edge Neural Text-to-Speech and
    plays the generated audio using playsound3.

Responsibilities:
    - Convert text into speech.
    - Play synthesized audio.
    - Manage temporary audio files.

The AudioService SHALL NOT depend on any UI module.

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

from __future__ import annotations

import asyncio
import os
import tempfile
import uuid
from pathlib import Path

import edge_tts
from playsound3 import playsound

from core.exceptions import AudioServiceError


class AudioService:
    """
    Shared text-to-speech service.

    This service provides a simple synchronous API while using
    Edge TTS internally.
    """

    DEFAULT_VOICE = "id-ID-GadisNeural"

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
    ) -> None:
        """
        Initialize the Audio Service.
        """

        self._playing = False

        self._temporary_file: Path | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def play(
        self,
        text: str,
        voice: str | None = None,
    ) -> None:
        """
        Convert text into speech and play it.

        Parameters
        ----------
        text:
            Text to pronounce.

        voice:
            Edge TTS voice name.

        Raises
        ------
        AudioServiceError
            Raised when synthesis or playback fails.
        """

        text = text.strip()

        if not text:

            raise AudioServiceError(
                "Text must not be empty."
            )

        self.stop()

        self._playing = True

        voice = (
            voice
            or self.DEFAULT_VOICE
        )

        try:

            self._temporary_file = (
                Path(
                    tempfile.gettempdir()
                )
                / f"{uuid.uuid4().hex}.mp3"
            )

            asyncio.run(
                self._synthesize(
                    text=text,
                    voice=voice,
                    output=self._temporary_file,
                )
            )

            playsound(
                str(
                    self._temporary_file,
                )
            )

        except Exception as exc:

            raise AudioServiceError(
                f"Audio playback failed: {exc}"
            ) from exc

        finally:

            self._playing = False

            self._cleanup()

    def stop(
        self,
    ) -> None:
        """
        Stop audio playback.

        Notes
        -----
        Version 1.0 does not interrupt active playback.

        This method only resets the playback state and removes
        any temporary audio file.
        """

        self._playing = False

        self._cleanup()

    def is_playing(
        self,
    ) -> bool:
        """
        Return whether audio is currently being played.
        """

        return self._playing

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    async def _synthesize(
        self,
        text: str,
        voice: str,
        output: Path,
    ) -> None:
        """
        Generate speech using Microsoft Edge TTS.
        """

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
        )

        await communicate.save(
            str(output),
        )

    def _cleanup(
        self,
    ) -> None:
        """
        Remove the temporary audio file.
        """

        if self._temporary_file is None:
            return

        try:

            if self._temporary_file.exists():

                os.remove(
                    self._temporary_file,
                )

        except OSError:

            #
            # Ignore cleanup failures.
            #
            pass

        self._temporary_file = None

