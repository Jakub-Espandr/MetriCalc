import os
import sys
from PySide6.QtGui import QIcon, QFontDatabase
from pathlib import Path

def get_app_icon():
    """Gets the application icon QIcon object, preferring .icns on macOS."""
    try:
        # Correctly determine base_dir for MetriCalc
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_dir = Path(base_dir) / "assets"
        icon_path = None
        if sys.platform == "darwin":
            icon_path = assets_dir / "icons" / "icon.icns"
        else:
            # Prefer .ico for Windows, fallback to .png
            ico_path = assets_dir / "icons" / "icon.ico"
            png_path = assets_dir / "icons" / "icon.png"
            if ico_path.exists():
                icon_path = ico_path
            elif png_path.exists():
                icon_path = png_path

        if icon_path and icon_path.exists():
            return QIcon(str(icon_path))
        else:
            return None
    except Exception as e:
        print(f"Warning: Could not load application icon: {e}")
        return None

def load_custom_fonts():
    """Load all .ttf fonts from the assets/fonts directory."""
    assets_dir = Path(__file__).parent.parent / "assets"
    fonts_dir = assets_dir / "fonts"
    
    if not fonts_dir.exists():
        return

    font_families = set()
    for font_file in fonts_dir.glob("*.ttf"):
        font_id = QFontDatabase.addApplicationFont(str(font_file))
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                font_families.add(families[0])

    if font_families:
        print(f"Successfully loaded font families: {', '.join(font_families)}")
    else:
        print("Warning: No custom fonts loaded.")

    return font_families 