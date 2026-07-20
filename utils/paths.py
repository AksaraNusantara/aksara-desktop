from pathlib import Path

# Root proyek
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder utama
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
PROFILES_DIR = BASE_DIR / "profiles"

# Subfolder assets
FONTS_DIR = ASSETS_DIR / "fonts"
IMAGES_DIR = ASSETS_DIR / "images"
ICONS_DIR = ASSETS_DIR / "icons"
SOUNDS_DIR = ASSETS_DIR / "sounds"
THEMES_DIR = ASSETS_DIR / "themes"