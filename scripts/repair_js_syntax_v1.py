#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import tempfile

MARKER = "GABON360-JS-SYNTAX-REPAIR-V1"

def check(src):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(src)
        name = f.name
    try:
        return subprocess.run(["node", "--check", name], capture_output=True, text=True).returncode == 0
    finally:
        Path(name).unlink(missing_ok=True)

def repair_block(src):
    if check(src):
        return src, False
    # The observed build failure is: SyntaxError: Unexpected token ')'.
    # Try only a single-character removal of ')' and accept it only when the
    # resulting program parses uniquely. This avoids silently rewriting valid JS.
    if "Unexpected token ')'" not in run_error(src):
        return src, False
    candidates = []
    for i, ch in enumerate(src):
        if ch == ")":
            trial = src[:i] + src[i+1:]
            if check(trial):
                candidates.append(trial)
                if len(candidates) > 1:
                    return src, False
    if len(candidates) == 1:
        return candidates[0], True
    return src, False

def run_error(src):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(src)
        name = f.name
    try:
        r = subprocess.run(["node", "--check", name], capture_output=True, text=True)
        return r.stderr or ""
    finally:
        Path(name).unlink(missing_ok=True)

def main():
    root = Path("android_project")
    htmls = sorted(root.rglob("index.html"), key=lambda p: len(p.parts))
    if not htmls:
        raise SystemExit("JS-SYNTAX-REPAIR FAIL: index.html introuvable")
    path = htmls[0]
    html = path.read_text(encoding="utf-8", errors="ignore")
    if MARKER in html:
        print("JS-SYNTAX-REPAIR: déjà présent")
        return

    pattern = re.compile(r"(<script(?:\s[^>]*)?>)(.*?)(</script>)", re.I | re.S)
    matches = list(pattern.finditer(html))
    changes = 0
    parts = []
    last = 0
    for m in matches:
        parts.append(html[last:m.start()])
        opening, body, closing = m.group(1), m.group(2), m.group(3)
        fixed, changed = repair_block(body)
        if changed:
            changes += 1
            print("JS-SYNTAX-REPAIR: correction automatique d'un bloc JavaScript")
        parts.append(opening + fixed + closing)
        last = m.end()
    parts.append(html[last:])
    html = "".join(parts)
    if changes:
        pos = html.lower().rfind("</body>")
        marker = "<!-- " + MARKER + " -->\n"
        html = html[:pos] + marker + html[pos:] if pos >= 0 else html + "\n" + marker
        path.write_text(html, encoding="utf-8")
    else:
        print("JS-SYNTAX-REPAIR: aucune correction automatique sûre")
    print("JS-SYNTAX-REPAIR: changes=", changes)

if __name__ == "__main__":
    main()
