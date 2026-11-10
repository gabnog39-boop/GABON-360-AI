#!/usr/bin/env python3
"""Generate real raster Android launcher icons from the official GABON 360 JPEG."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "icons" / "gabon360-icon.jpg"
RES = ROOT / "android" / "app" / "src" / "main" / "res"

if not SOURCE.is_file() or SOURCE.stat().st_size < 100:
    raise SystemExit(f"Official icon missing or empty: {SOURCE}")

try:
    with Image.open(SOURCE) as source:
        source.load()
        artwork = source.convert("RGBA")
except Exception as exc:
    raise SystemExit(f"Cannot read official JPEG: {exc}")

# Keep the original image intact; derive launcher-sized PNGs from a copy.
if artwork.width < 64 or artwork.height < 64:
    raise SystemExit("Official icon image is unexpectedly small")

def fit_square(image, size, inset=0):
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    available = size - 2 * inset
    thumb = image.copy()
    thumb.thumbnail((available, available), Image.Resampling.LANCZOS)
    canvas.alpha_composite(thumb, ((size-thumb.width)//2, (size-thumb.height)//2))
    return canvas

# Legacy launcher icons: actual PNG bitmaps in Android mipmap resource folders.
for density, px in (("mdpi",48),("hdpi",72),("xhdpi",96),("xxhdpi",144),("xxxhdpi",192)):
    folder = RES / f"mipmap-{density}"
    folder.mkdir(parents=True, exist_ok=True)
    icon = fit_square(artwork, px, max(1, px//16))
    icon.save(folder / "ic_launcher.png", format="PNG", optimize=True)
    icon.save(folder / "ic_launcher_round.png", format="PNG", optimize=True)
    # Remove old XML aliases which could shadow bitmap resources.
    for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
        stale = folder / name
        if stale.exists():
            stale.unlink()

# Adaptive icon foreground respects Android's central safe zone.
foreground_dir = RES / "drawable-nodpi"
foreground_dir.mkdir(parents=True, exist_ok=True)
fit_square(artwork, 432, 54).save(foreground_dir / "gabon360_icon_foreground.png", format="PNG", optimize=True)
(RES / "values").mkdir(parents=True, exist_ok=True)
(RES / "values" / "gabon360_icon_colors.xml").write_text(
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
for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
    (adaptive_dir / name).write_text(adaptive_xml, encoding="utf-8")

print("OK — real PNG launcher icons and adaptive icons generated from the official artwork")
