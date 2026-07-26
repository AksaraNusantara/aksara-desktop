"""
Integration test for the Official Javanese ScriptPack.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.engine import CoreEngine


def main() -> None:
    """
    Run a simple integration test.

    Expected workflow:

        Core Engine
            ↓
        Load ScriptPack
            ↓
        Read Manifest
            ↓
        Load Character Data
            ↓
        Print First Character
    """

    root_directory = Path(__file__).resolve().parents[3]

    scriptpacks_directory = (
        root_directory
        / "scriptpacks"
    )

    engine = CoreEngine()

    print("=" * 70)
    print("Aksara Nusantara Integration Test")
    print("=" * 70)

    print()

    print(scriptpacks_directory)
    print("Loading ScriptPack...")
    engine.initialize(scriptpacks_directory)

    print("OK")

    print()

    script = engine.get("javanese")

    print(f"Identifier : {script.identifier}")
    print(f"Name       : {script.name}")
    print(f"Version    : {script.version}")

    print()

    characters = script.get_characters()

    print(f"Characters loaded : {len(characters)}")

    print()

    if characters:

        first = characters[0]

        print("First Character")

        print("----------------------------")

        print(f"Glyph     : {first['glyph']}")
        print(f"Latin     : {first['latin']}")
        print(f"Unicode   : {first['unicode']}")

    print()

    print("Integration Test PASSED")


if __name__ == "__main__":
    main()