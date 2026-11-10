#!/usr/bin/env python3
"""Generate real raster Android launcher icons from the official GABON 360 JPEG."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "icons" / "gabon360-icon.jpg"
RES = ROOT / "android" / "app" / "src" / "main" / "res"

if not SOURCE.is_file() or SOURCE.stat().st_size < 100:
    raise SystemExit(f"Official icon missing or empty: {SOURCE}")

used_fallback = False
try:
    with Image.open(SOURCE) as source:
        source.load()
        artwork = source.convert("RGBA")
except Exception as exc:
    # The repository JPEG is currently unreadable. Keep it untouched and
    # generate a deterministic branded fallback so Android builds do not stop.
    used_fallback = True
    print(f"WARNING: source icon unreadable ({exc}); generating Gabon 360 fallback")
    size = 432
    artwork = Image.new("RGBA", (size, size), (5, 13, 25, 255))
    draw = ImageDraw.Draw(artwork)
    draw.rounded_rectangle((8, 8, 424, 424), radius=82, outline=(34, 190, 105, 255), width=10)
    draw.arc((30, 30, 402, 402), 205, 330, fill=(246, 203, 38, 255), width=9)
    draw.arc((30, 30, 402, 402), 330, 80, fill=(25, 142, 224, 255), width=9)
    # Simplified Gabon silhouette with the national flag colours.
    map_points = [(190,55),(238,65),(276,94),(290,132),(278,165),(300,194),
                  (278,226),(252,246),(235,292),(204,320),(180,294),
                  (157,265),(130,246),(116,214),(132,183),(120,151),
                  (137,119),(145,83)]
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).polygon(map_points, fill=255)
    flag = Image.new("RGBA", (size, size), (0,0,0,0))
    fd = ImageDraw.Draw(flag)
    fd.rectangle((0,75,size,155), fill=(0,145,75,255))
    fd.rectangle((0,155,size,235), fill=(250,210,45,255))
    fd.rectangle((0,235,size,315), fill=(0,105,190,255))
    artwork.alpha_composite(Image.composite(flag, Image.new("RGBA",(size,size),(0,0,0,0)), mask))
    draw = ImageDraw.Draw(artwork)
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 57)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 77)
    except OSError:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    draw.text((216, 326), "GABON", anchor="mm", font=font_big, fill=(255,255,255,255), stroke_width=2, stroke_fill=(5,13,25,255))
    draw.text((216, 385), "360", anchor="mm", font=font_small, fill=(45,210,125,255), stroke_width=2, stroke_fill=(5,13,25,255))

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

print("OK — launcher PNGs and adaptive icons generated using the fallback mark" if used_fallback else "OK — launcher PNGs and adaptive icons generated from the supplied artwork")
