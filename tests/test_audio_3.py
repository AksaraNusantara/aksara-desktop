"""Manual ScriptPack-aware AudioService smoke test.

This module is intentionally safe to import during unittest discovery.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.engine import CoreEngine
from core.services.audio_service import AudioService


if __name__ == "__main__":
    engine = CoreEngine()
    engine.initialize(PROJECT_ROOT / "scriptpacks")
    engine.activate("javanese")

    audio = AudioService(
        cache_root=PROJECT_ROOT / "cache" / "audio",
    )
    audio.play("ha")
