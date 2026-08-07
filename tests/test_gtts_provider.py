from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.audio import GTTSProvider


def main() -> None:
    """
    Verify GTTSProvider.
    """

    provider = GTTSProvider()

    print(
        "Provider:",
        provider.name,
    )

    print(
        "Available:",
        provider.is_available(),
    )

    output = (
        PROJECT_ROOT
        / "cache"
        / "provider_test.mp3"
    )

    provider.generate(
        "ha",
        output,
    )

    print(
        "Generated:",
        output.exists(),
    )

    print(
        output,
    )


if __name__ == "__main__":
    main()