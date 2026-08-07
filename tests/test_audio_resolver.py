from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.audio import AudioCache
from core.audio import AudioResolver


def main() -> None:
    """
    Verify AudioResolver.
    """

    cache = AudioCache(
        PROJECT_ROOT
        / "cache"
        / "audio"
    )

    resolver = AudioResolver(
        asset_root=None,
        cache=cache,
    )

    result = resolver.resolve(
        "ha",
    )

    print(
        "Resolved:",
        result,
    )


if __name__ == "__main__":
    main()