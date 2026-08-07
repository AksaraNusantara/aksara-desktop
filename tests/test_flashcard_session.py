from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.engine import CoreEngine
from application.learning.flashcard.flashcard_session import (
    FlashcardSession,
)


def main() -> None:
    """
    Verify that FlashcardSession can be created.
    """

    engine = CoreEngine()

    session = FlashcardSession(
        engine,
    )

    print("FlashcardSession created successfully.")
    print(session)


if __name__ == "__main__":
    main()