"""
===============================================================================

Aksara Nusantara

Module:
    scriptpacks.javanese.script

Module Type:
    ScriptPack Implementation

Purpose:
    Official implementation of the Javanese ScriptPack.

===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtGui import QFontDatabase

from core.scriptpack import BaseScriptPack


class JavaneseScriptPack(BaseScriptPack):
    """Official implementation of the Javanese ScriptPack."""

    def __init__(self) -> None:
        super().__init__()
        self._dataset_name: str = ""

    def get_characters(self) -> list[dict]:
        """Return character definitions from the current dataset(s)."""

        character_directory = (
            Path(__file__).parent
            / "assets"
            / "characters"
        )

        characters: list[dict] = []

        json_files = sorted(character_directory.glob("*.json"))

        if not json_files:
            raise FileNotFoundError(
                f"No character datasets found in: {character_directory}"
            )

        for json_file in json_files:

            self._dataset_name = json_file.stem

            with json_file.open(
                "r",
                encoding="utf-8",
            ) as fp:
                repository = json.load(fp)

            if not isinstance(repository, list):
                raise ValueError(
                    f"{json_file.name} must contain a JSON array."
                )

            characters.extend(repository)

        return characters

    def get_dataset_name(self) -> str:
        """Return the active dataset name."""

        return self._dataset_name

    def register_assets(self) -> None:
        """Register runtime assets required by this ScriptPack."""

        font_directory = (
            Path(__file__).parent
            / "assets"
            / "fonts"
        )

        if not font_directory.is_dir():
            raise FileNotFoundError(
                f"Font directory not found: {font_directory}"
            )

        for font_file in sorted(font_directory.glob("*.ttf")):

            font_id = QFontDatabase.addApplicationFont(
                str(font_file)
            )

            if font_id == -1:
                raise RuntimeError(
                    f"Failed to register font: {font_file.name}"
                )
