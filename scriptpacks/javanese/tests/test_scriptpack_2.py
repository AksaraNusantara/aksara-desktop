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
    print("TEST START")

    root_directory = Path(__file__).resolve().parents[3]

    scriptpacks_directory = (
        root_directory
        / "scriptpacks"
    )

    print("1")
    engine = CoreEngine()

    print("2")
    engine.initialize(
        scriptpacks_directory,
    )
    scriptpacks = engine.list()

    assert len(scriptpacks) > 0

    print("Registered ScriptPacks:")

    for identifier in engine.list():

        print(
            f" - {identifier}",
        )

    print("3")
    engine.activate(
        "javanese",
    )

    print("4")
    print(
        engine.get_data_path(),
    )

    print(
        engine.get_assets_path(),
    )

    print(
        engine.get_generated_path(),
    )

    print(
        engine.get_audio_generated_path(),
    )

    print("TEST END")


if __name__ == "__main__":
    main()