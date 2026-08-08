from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.engine import CoreEngine
from core.services.audio_service import AudioService

engine = CoreEngine()

#
# Initialize the Core Engine.
#

engine.initialize(
    PROJECT_ROOT / "scriptpacks",
)

#
# Activate the Javanese ScriptPack.
#

engine.activate(
    "javanese",
)

audio = AudioService(
    engine,
)

audio.play(".ha ")

result = audio._resolve_asset_audio(
    "ha",
)

print(result)