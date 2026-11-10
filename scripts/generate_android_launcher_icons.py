#!/usr/bin/env python3
"""Create Android launcher resources from the repository's official JPEG icon.
No image conversion is performed: the source artwork is copied byte-for-byte.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "icons" / "gabon360-icon.jpg"
RES = ROOT / "android" / "app" / "src" / "main" / "res"

if not SOURCE.is_file() or SOURCE.stat().st_size < 100:
    raise SystemExit(f"Official icon missing or empty: {SOURCE}")

data = SOURCE.read_bytes()
if not (data.startswith(bytes.fromhex("FFD8")) and data.endswith(bytes.fromhex("FFD9"))):
    raise SystemExit("Official icon is not a complete JPEG file")

drawable = RES / "drawable-nodpi"
drawable.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, drawable / "gabon360_icon.jpg")

# Density-qualified aliases use the original artwork without re-encoding it.
bitmap_xml = '''<?xml version="1.0" encoding="utf-8"?>
<bitmap xmlns:android="http://schemas.android.com/apk/res/android"
    android:src="@drawable/gabon360_icon"
    android:gravity="center" />
'''
for density in ("mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"):
    folder = RES / f"mipmap-{density}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "ic_launcher.xml").write_text(bitmap_xml, encoding="utf-8")
    (folder / "ic_launcher_round.xml").write_text(bitmap_xml, encoding="utf-8")

values = RES / "values"
values.mkdir(parents=True, exist_ok=True)
(values / "gabon360_icon_colors.xml").write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<resources><color name="gabon360_icon_background">#FFFFFF</color></resources>\n',
    encoding="utf-8",
)

adaptive = RES / "mipmap-anydpi-v26"
adaptive.mkdir(parents=True, exist_ok=True)
adaptive_xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/gabon360_icon_background" />
    <foreground android:drawable="@drawable/gabon360_icon" />
</adaptive-icon>
'''
(adaptive / "ic_launcher.xml").write_text(adaptive_xml, encoding="utf-8")
(adaptive / "ic_launcher_round.xml").write_text(adaptive_xml, encoding="utf-8")
print("OK — launcher resources generated; official JPEG copied without modification")
