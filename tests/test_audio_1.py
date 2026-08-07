from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.engine import CoreEngine
from core.services.audio_service_legacy import AudioService

engine = CoreEngine()

audio = AudioService(
    engine,
)

audio.play("Halo, selamat datang di Aksara Nusantara.")