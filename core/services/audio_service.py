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
from pathlib import Path

import edge_tts
from playsound3 import playsound

from core.engine import CoreEngine
from core.exceptions import EngineError
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
        engine: CoreEngine,
    ) -> None:
        """
        Initialize the Audio Service.

        Parameters
        ----------
        engine:
            Shared Core Engine instance.
        """

        self._engine = engine

        self._playing = False

    def _resolve_asset_audio(
        self,
        text: str,
    ) -> Path | None:
        """
        Resolve bundled audio from the active
        ScriptPack.

        Parameters
        ----------
        text:
            Spoken text.

        Returns
        -------
        Path | None
            Path to the bundled audio file if it
            exists, otherwise None.
        """

        audio_path = (
            self._engine.get_assets_path()
            / "audio"
            / f"{text}.mp3"
        )

        if audio_path.is_file():

            return audio_path

        return None

    def _resolve_generated_audio(
        self,
        text: str,
    ) -> Path | None:
        """
        Resolve generated audio from the active
        ScriptPack.

        Parameters
        ----------
        text:
            Spoken text.

        Returns
        -------
        Path | None
            Generated audio file if found,
            otherwise None.
        """

        try:

            audio_path = (
                self._engine.get_audio_generated_path()
                / f"{text}.mp3"
            )

        except EngineError:

            return None

        if audio_path.is_file():

            return audio_path

        return None

    def _get_generated_audio_path(
        self,
        text: str,
    ) -> Path:
        """
        Return the destination path for generated
        audio.

        Parameters
        ----------
        text:
            Spoken text.

        Returns
        -------
        Path
            Destination path of the generated
            audio file.
        """

        return (
            self._engine.get_audio_generated_path()
            / f"{text}.mp3"
        )

    def _generate_audio(
        self,
        text: str,
        voice: str,
        destination: Path,
    ) -> None:
        """
        Generate speech using Edge TTS.

        Parameters
        ----------
        text:
            Spoken text.

        voice:
            Edge TTS voice.

        destination:
            Output audio file.

        Raises
        ------
        AudioServiceError
            If speech generation fails.
        """

        print(f"Generating audio: {text}")

        try:

            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
            )

            asyncio.run(
                communicate.save(
                    str(destination),
                )
            )

        except Exception as exc:

            raise AudioServiceError(
                "Failed to generate speech."
            ) from exc

    def _play_file(
        self,
        audio_file: Path,
    ) -> None:
        """
        Play an existing audio file.

        Parameters
        ----------
        audio_file:
            Audio file to be played.
        """

        playsound(
            str(audio_file),
        )

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

        asset_audio = self._resolve_asset_audio(
            text,
        )

        if asset_audio is not None:

            self._play_file(
                asset_audio,
            )

            return

        generated_audio = (
            self._resolve_generated_audio(
                text,
            )
        )

        if generated_audio is not None:

            self._play_file(
                generated_audio,
            )

            return

        try:

            generated_audio = (
                self._get_generated_audio_path(
                    text,
                )
            )

            self._generate_audio(
                text=text,
                voice=voice,
                destination=generated_audio,
            )

            self._play_file(
                generated_audio,
            )

        except Exception as exc:

            raise AudioServiceError(
                f"Audio playback failed: {exc}"
            ) from exc

        finally:

            self._playing = False

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

    def is_playing(
        self,
    ) -> bool:
        """
        Return whether audio is currently being played.
        """

        return self._playing
