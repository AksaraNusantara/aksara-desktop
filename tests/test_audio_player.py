from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.audio import AudioPlayer


def main() -> None:
    """
    Verify AudioPlayer.
    """

    player = AudioPlayer()

    audio = (
        PROJECT_ROOT
        / "cache"
        / "provider_test.mp3"
    )

    if not audio.exists():

        print(
            "Audio file not found.",
        )

        return

    print(
        "Playing:",
        audio,
    )

    player.play(
        audio,
    )

    print(
        "Playback finished.",
    )


if __name__ == "__main__":
    main()