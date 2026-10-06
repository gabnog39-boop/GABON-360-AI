#!/usr/bin/env python3
"""Repair known HTML script-boundary corruption in the consolidated Android UI.

A legacy consolidated base can contain the national-pages JavaScript without its
closing </script>. Later page-completeness HTML is then swallowed by that script
tag, making the whole block fail at runtime. This repair only fixes that exact
known boundary and is idempotent.
"""
from pathlib import Path

NATIONAL = "<!-- GABON360-NATIONAL-PAGES-V1 -->"
COMPLETENESS = "<!-- GABON360-PAGE-COMPLETENESS-V2 -->"

def repair(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    start = text.find(NATIONAL)
    marker = text.find(COMPLETENESS, start + len(NATIONAL))
    if start < 0 or marker < 0:
        return False

    between = text[start:marker]
    last_open = between.lower().rfind("<script")
    last_close = between.lower().rfind("</script>")
    if last_open < 0 or last_close > last_open:
        return False

    # Only repair when the completeness block is currently inside the
    # national-pages script. Insert a single closing tag immediately before it.
    text = text[:marker] + "</script>\n" + text[marker:]
    path.write_text(text, encoding="utf-8")
    return True

def main() -> None:
    candidates = sorted(
        Path("android_project").rglob("index.html"),
        key=lambda p: ("assets" not in p.parts, len(p.parts)),
    )
    if not candidates:
        raise SystemExit("SCRIPT-BOUNDARY-REPAIR FAIL: index.html introuvable")

    changed = 0
    for path in candidates:
        if repair(path):
            changed += 1
            print("SCRIPT-BOUNDARY-REPAIR: fixed", path)

    if changed == 0:
        print("SCRIPT-BOUNDARY-REPAIR: no change needed")
    else:
        print("SCRIPT-BOUNDARY-REPAIR: OK", changed, "file(s) repaired")

if __name__ == "__main__":
    main()
