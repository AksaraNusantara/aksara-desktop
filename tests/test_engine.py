"""
===============================================================================

Aksara Nusantara

Foundation Validation Test

Purpose:
    Validate that the Core Engine can discover, load, and initialize
    multiple ScriptPacks using only the public Core Engine API.

===============================================================================
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.engine import CoreEngine


def main():

    print("=" * 70)
    print("Aksara Nusantara Foundation Validation")
    print("=" * 70)
    print()

    scriptpacks_dir = PROJECT_ROOT / "scriptpacks"

    print(f"ScriptPack Directory : {scriptpacks_dir}")
    print()

    print("Initializing Core Engine...")

    engine = CoreEngine()

    print("Loading ScriptPacks...")

    engine.initialize(scriptpacks_dir)

    print("OK")
    print()

    scriptpacks = engine.list()

    print(f"Registered ScriptPacks : {len(scriptpacks)}")
    print()

    for identifier in scriptpacks:

        scriptpack = engine.get(identifier)

        characters = scriptpack.get_characters()

        print("-" * 50)
        print(f"Identifier : {identifier}")
        print(f"Characters : {len(characters)}")

        if characters:

            first = characters[0]

            print("First Character")
            print("----------------------------")
            print(f"Glyph     : {first['glyph']}")
            print(f"Latin     : {first['latin']}")
            print(f"Unicode   : {first['unicode']}")

        print()

    print("=" * 70)
    print("FOUNDATION VALIDATION PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()