#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import tempfile

MARKER = "GABON360-JS-SYNTAX-REPAIR-V2"
REQUIRED = [
    "GABON360-UNIVERSAL-MODULE-PAGES-V1",
    "GABON360-PAGE-FUNCTIONALITY-V2",
    "GABON360-AI-OPTION-RUNTIME-V2",
    "GABON360-AVATAR-HOME-V1",
]

def node_check(src):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(src)
        name = f.name
    try:
        r = subprocess.run(["node", "--check", name], capture_output=True, text=True)
        return r.returncode == 0, (r.stderr or "")
    finally:
        Path(name).unlink(missing_ok=True)

def select_index():
    htmls = sorted(Path("android_project").rglob("index.html"), key=lambda p: (len(p.parts), str(p)))
    if not htmls:
        raise SystemExit("JS-SYNTAX-REPAIR FAIL: index.html introuvable")
    candidates = []
    for p in htmls:
        h = p.read_text(encoding="utf-8", errors="ignore")
        score = sum(x in h for x in REQUIRED)
        candidates.append((score, p, h))
    score, path, html = max(candidates, key=lambda x: (x[0], -len(x[1].parts), str(x[1])))
    if score < len(REQUIRED):
        raise SystemExit(f"JS-SYNTAX-REPAIR FAIL: mauvais index.html sélectionné score={score}/{len(REQUIRED)}")
    return path, html

def repair_script_block(block):
    ok, err = node_check(block)
    if ok:
        return block, False

    if "Unexpected token ')'" not in err and "Unexpected token ')' " not in err:
        return block, False

    # Node reports the source line and a caret for this class of syntax error.
    m = re.search(r"\.js:(\d+)", err)
    if not m:
        return block, False
    line_no = int(m.group(1))
    lines = block.splitlines(keepends=True)
    if not (1 <= line_no <= len(lines)):
        return block, False

    line = lines[line_no - 1]
    candidates = []
    for idx, ch in enumerate(line):
        if ch != ")":
            continue
        trial_line = line[:idx] + line[idx+1:]
        trial_lines = list(lines)
        trial_lines[line_no - 1] = trial_line
        trial = "".join(trial_lines)
        ok2, _ = node_check(trial)
        if ok2:
            candidates.append(trial)
            if len(candidates) > 1:
                return block, False

    if len(candidates) == 1:
        return candidates[0], True
    return block, False

def main():
    path, html = select_index()
    if MARKER in html:
        print("JS-SYNTAX-REPAIR: déjà présent")
        return

    pattern = re.compile(r"(<script(?:\s[^>]*)?>)(.*?)(</script>)", re.I | re.S)
    matches = list(pattern.finditer(html))
    out = []
    last = 0
    changes = 0

    for m in matches:
        out.append(html[last:m.start()])
        opening, body, closing = m.group(1), m.group(2), m.group(3)
        fixed, changed = repair_script_block(body)
        if changed:
            changes += 1
            print(f"JS-SYNTAX-REPAIR: correction sûre dans le bloc {len(out)}")
        out.append(opening + fixed + closing)
        last = m.end()
    out.append(html[last:])

    if changes:
        html = "".join(out)
        marker = f"<!-- {MARKER} -->\n"
        pos = html.lower().rfind("</body>")
        html = html[:pos] + marker + html[pos:] if pos >= 0 else html + "\n" + marker
        path.write_text(html, encoding="utf-8")
        print("JS-SYNTAX-REPAIR: corrected=", changes)
    else:
        print("JS-SYNTAX-REPAIR: aucune correction sûre")

if __name__ == "__main__":
    main()
