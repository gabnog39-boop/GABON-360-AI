#!/usr/bin/env python3
"""Repair duplicated top-level V163 patrol block in the consolidated HTML.

The consolidated source can contain the V163 patrol block twice. Two copies in
one <script> scope redeclare const/let identifiers and prevent the whole script
from parsing on Android WebView. Keep the first complete V163 block and remove
only a later exact V163 block up to the V169 fusion section.
"""
from pathlib import Path

MARKER = '<!-- GABON360-FINAL-RUNTIME-DUPLICATE-REPAIR -->'
START = '// V163 — Centre de situation des patrouilles + IA terrain'
END = '// V169 — FUSION CARTE + VISION + PATROUILLE'


def repair(html: str):
    if MARKER in html:
        return html, 0
    first = html.find(START)
    if first < 0:
        return html + '\n' + MARKER + '\n', 0
    second = html.find(START, first + len(START))
    if second < 0:
        out = html.replace('</body>', MARKER + '\n</body>', 1) if '</body>' in html else html + '\n' + MARKER + '\n'
        return out, 0
    end = html.find(END, second)
    if end < 0:
        raise SystemExit('RUNTIME-DUPLICATE-REPAIR FAIL: fin V169 introuvable après second V163')
    out = html[:second] + html[end:]
    out = out.replace('</body>', MARKER + '\n</body>', 1) if '</body>' in out else out + '\n' + MARKER + '\n'
    return out, 1


def main():
    root = Path('android_project')
    htmls = sorted(root.rglob('index.html'), key=lambda p: len(p.parts))
    if not htmls:
        raise SystemExit('RUNTIME-DUPLICATE-REPAIR FAIL: index.html introuvable')
    path = htmls[0]
    html = path.read_text(encoding='utf-8', errors='ignore')
    repaired, removed = repair(html)
    if repaired != html:
        path.write_text(repaired, encoding='utf-8')
    print(f'RUNTIME-DUPLICATE-REPAIR: removed={removed}')


if __name__ == '__main__':
    main()
