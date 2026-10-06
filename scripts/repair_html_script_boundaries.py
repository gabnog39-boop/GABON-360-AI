#!/usr/bin/env python3
"""Repair HTML script-boundary corruption in the consolidated Android UI.

Some legacy consolidated pages can lose a closing </script> between injected
sections. When that happens later HTML/CSS is swallowed by the previous script
and the Android WebView stops executing the page.

This repair is deliberately marker-based and idempotent: for every GABON360
HTML section marker, if the marker currently occurs while a <script> block is
open, a single </script> is inserted immediately before the marker.
"""
from pathlib import Path
import re

MARKER_RE = re.compile(r"<!--\s*GABON360-[A-Z0-9_-]+[^>]*-->", re.I)
TAG_RE = re.compile(r"</?script\b[^>]*>", re.I)

def repair(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    markers = list(MARKER_RE.finditer(text))
    if not markers:
        return 0

    insertions = []
    cursor = 0
    script_open = False

    # Walk the document in source order. Only script tags are stateful here;
    # markers are the stable section boundaries produced by our injectors.
    for match in re.finditer(r"</?script\b[^>]*>|<!--\s*GABON360-[A-Z0-9_-]+[^>]*-->", text, re.I):
        token = match.group(0)
        if token.lower().startswith("<script") and not token.lower().startswith("</script"):
            script_open = True
        elif token.lower().startswith("</script"):
            script_open = False
        elif script_open and token.lower().startswith("<!--"):
            insertions.append(match.start())

    if not insertions:
        return 0

    for pos in reversed(insertions):
        text = text[:pos] + "</script>\n" + text[pos:]
    path.write_text(text, encoding="utf-8")
    return len(insertions)

def main() -> None:
    candidates = sorted(Path("android_project").rglob("index.html"), key=lambda p: len(p.parts))
    if not candidates:
        raise SystemExit("SCRIPT-BOUNDARY-REPAIR FAIL: index.html introuvable")

    total = 0
    for path in candidates:
        fixed = repair(path)
        if fixed:
            total += fixed
            print(f"SCRIPT-BOUNDARY-REPAIR: fixed {fixed} boundary/boundaries in {path}")

    print("SCRIPT-BOUNDARY-REPAIR:", "OK" if total else "no change needed", total)

if __name__ == "__main__":
    main()
