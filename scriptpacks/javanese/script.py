"""
===============================================================================

Aksara Nusantara

Module:
    scriptpacks.javanese.script

Module Type:
    ScriptPack Implementation

Purpose:
    Official implementation of the Javanese ScriptPack.

Implements:
    AN-STD-001
    Section 11 - BaseScriptPack Interface
    Section 17 - Transliteration

References:
    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from PySide6.QtGui import QFontDatabase

from core.scriptpack import BaseScriptPack
from core.transliteration import TransliterationDirection
from core.transliteration import TransliterationResult


_TRANSLITERATION_MODULE = "aksara_scriptpack_javanese_transliteration"


def _load_transliteration_module():
    """
    Load the sibling ``transliteration.py`` by path.

    The Loader imports this file through ``spec_from_file_location``, so
    the ScriptPack directory is not a regular package and relative imports
    are unavailable.
    """

    module = sys.modules.get(_TRANSLITERATION_MODULE)

    if module is not None:
        return module

    spec = importlib.util.spec_from_file_location(
        _TRANSLITERATION_MODULE,
        Path(__file__).with_name("transliteration.py"),
    )

    if spec is None or spec.loader is None:
        raise ImportError("Unable to load Javanese transliteration module.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[_TRANSLITERATION_MODULE] = module
    spec.loader.exec_module(module)

    return module


class JavaneseScriptPack(BaseScriptPack):
    """Official implementation of the Javanese ScriptPack."""

    def __init__(self) -> None:
        super().__init__()
        self._dataset_name = "nglegena"
        self._transliterator = None

    def supports_transliteration(self) -> bool:
        """The Javanese ScriptPack provides transliteration."""

        return True

    def transliterate(
        self,
        text: str,
        direction: TransliterationDirection,
    ) -> TransliterationResult:
        """Transliterate between Latin and Aksara Jawa."""

        if self._transliterator is None:
            module = _load_transliteration_module()

            self._transliterator = module.JavaneseTransliterator(
                Path(__file__).parent / "assets" / "characters"
            )

        return self._transliterator.transliterate(text, direction)

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

        json_file = (
            character_directory
            / f"{self._dataset_name}.json"
        )

        if not json_file.exists():
            raise FileNotFoundError(
                f"Dataset not found: {json_file.name}"
            )

        with json_file.open(
            "r",
            encoding="utf-8",
        ) as fp:
            repository = json.load(fp)

        if not isinstance(
            repository,
            list,
        ):
            raise ValueError(
                f"{json_file.name} must contain a JSON array."
            )

        return repository
#
#        return characters

    def get_dataset_name(self) -> str:
        """Return the active dataset name."""

        return self._dataset_name

    def get_available_datasets(
        self,
    ) -> list[tuple[str, str]]:
        """
        Return available learning datasets.
        """

        return [
            (
                "nglegena",
                "Nglegena",
            ),
            (
                "sandhangan_swara",
                "Sandhangan Swara",
            ),
            (
                "sandhangan_panyigeg",
                "Sandhangan Panyigeg Wanda",
            ),
            (
                "sandhangan_wyanjana",
                "Sandhangan Wyanjana",
            ),
            (
                "pasangan",
                "Pasangan",
            ),
            (
                "murda",
                "Murda",
            ),
            (
                "rekan",
                "Rekan",
            ),
            (
                "swara",
                "Swara",
            ),
            (
                "angka",
                "Angka",
            ),
            (
                "pada",
                "Pada",
            ),
        ]

    def set_current_dataset(
        self,
        dataset_name: str,
    ) -> None:
        """
        Set the active learning dataset.
        """

        available = {
            name
            for name, _
            in self.get_available_datasets()
        }

        if dataset_name not in available:
            raise ValueError(
                f"Unknown dataset: {dataset_name}"
            )

        self._dataset_name = dataset_name

    def get_current_dataset(
        self,
    ) -> str:
        """
        Return the active dataset.
        """

        return self._dataset_name

    def register_assets(self) -> None:
        """
        Register GUI assets used by the Javanese
        ScriptPack.

        This method registers bundled fonts into
        Qt's application font database.

        Notes
        -----
        This method requires an active
        QApplication instance.
        """

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

    def get_dataset_display_name(
        self,
    ) -> str:
        """
        Return the display name of the active dataset.
        """

        for (
            internal,
            display,
        ) in self.get_available_datasets():

            if internal == self._dataset_name:
                return display

        return self._dataset_name

#    def get_current_dataset_display_name(
#        self,
#    ) -> str:
#
#        return (
#            self.get_active_scriptpack()
#            .get_dataset_display_name()
#        )
#