from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.services.audio_service import AudioService


def main() -> None:
    """
    Verify AudioService playback.
    """

    service = AudioService(
        cache_root=(
            PROJECT_ROOT
            / "cache"
            / "audio"
        )
    )

    service.play(
        "Halo dari Audio Framework versi dua."
    )

    print(
        "Playback completed."
    )


if __name__ == "__main__":
    main()