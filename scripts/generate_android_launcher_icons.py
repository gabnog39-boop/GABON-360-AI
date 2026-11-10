#!/usr/bin/env python3
"""Generate Android legacy and adaptive launcher icons from the official GABON 360 image."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "icons" / "gabon360-icon.jpg"
RES = ROOT / "android" / "app" / "src" / "main" / "res"

if not SOURCE.is_file():
    raise SystemExit(f"Official icon missing: {SOURCE}")

with Image.open(SOURCE) as original:
    image = original.convert("RGBA")

# Android launcher legacy icons: exact density sizes, square, full official artwork.
density_sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}
for folder, size in density_sizes.items():
    target = RES / folder
    target.mkdir(parents=True, exist_ok=True)
    fitted = image.copy()
    fitted.thumbnail((int(size * 0.94), int(size * 0.94)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    canvas.alpha_composite(fitted, ((size - fitted.width) // 2, (size - fitted.height) // 2))
    canvas.save(target / "ic_launcher.png", optimize=True)
    canvas.save(target / "ic_launcher_round.png", optimize=True)

# Adaptive icon foreground: retain a safe margin for Android's circular/squircle masks.
foreground_dir = RES / "drawable-nodpi"
foreground_dir.mkdir(parents=True, exist_ok=True)
size = 432
foreground = Image.new("RGBA", (size, size), (0, 0, 0, 0))
fitted = image.copy()
fitted.thumbnail((int(size * 0.68), int(size * 0.68)), Image.Resampling.LANCZOS)
foreground.alpha_composite(fitted, ((size - fitted.width) // 2, (size - fitted.height) // 2))
foreground.save(foreground_dir / "gabon360_icon_foreground.png", optimize=True)

colors = RES / "values"
colors.mkdir(parents=True, exist_ok=True)
(colors / "gabon360_icon_colors.xml").write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<resources><color name="gabon360_icon_background">#FFFFFF</color></resources>\n',
    encoding="utf-8",
)

adaptive_dir = RES / "mipmap-anydpi-v26"
adaptive_dir.mkdir(parents=True, exist_ok=True)
adaptive_xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/gabon360_icon_background" />
    <foreground android:drawable="@drawable/gabon360_icon_foreground" />
</adaptive-icon>
'''
(adaptive_dir / "ic_launcher.xml").write_text(adaptive_xml, encoding="utf-8")
(adaptive_dir / "ic_launcher_round.xml").write_text(adaptive_xml, encoding="utf-8")
print("OK — official GABON 360 legacy and adaptive launcher icons generated")
