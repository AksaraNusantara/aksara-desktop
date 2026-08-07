from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.audio import AudioCache


def main() -> None:
    """
    Verify AudioCache.
    """

    cache = AudioCache(
        PROJECT_ROOT
        / "cache"
        / "audio"
    )

    path = cache.get_path(
        "ha",
    )

    print(
        "Cache path:",
        path,
    )

    print(
        "Exists:",
        cache.exists(
            "ha",
        ),
    )


if __name__ == "__main__":
    main()