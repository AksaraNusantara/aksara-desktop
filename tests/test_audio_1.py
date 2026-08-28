"""Manual AudioService smoke test.

This module is intentionally safe to import during unittest discovery.
Run it directly when interactive audio playback is desired.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.services.audio_service import AudioService


if __name__ == "__main__":
    audio = AudioService(
        cache_root=PROJECT_ROOT / "cache" / "audio",
    )
    audio.play("Halo, selamat datang di Aksara Nusantara.")
