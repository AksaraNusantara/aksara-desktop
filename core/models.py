"""
===============================================================================

Aksara Nusantara

Module:
    core.models

Purpose:
    Shared data models used by the Core Engine.

===============================================================================
"""

from dataclasses import dataclass
from typing import Any

from core.scriptpack import BaseScriptPack


@dataclass(slots=True)
class LoadedScriptPack:
    """
    Represents a successfully loaded ScriptPack.
    """

    manifest: dict[str, Any]
    instance: BaseScriptPack